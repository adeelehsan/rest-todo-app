from __future__ import unicode_literals

from django.db import models
from django.db.models import Count
from django.conf import settings
from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    creation_date = models.DateField(auto_now=True)
    completion_date = models.DateField(null=True, blank=True)
    log = models.CharField(max_length=200, null=True)
    status_choices = (
        ('inprogress', 'In Progress'),
        ('complete', 'Complete'),
    )
    status = models.CharField(max_length=200, null=True, choices=status_choices, default=status_choices[0])

    class Meta:
        permissions = (('can_view', 'can view all task'),)

    def __str__(self):
        return self.title


class User(AbstractUser):
    joining_date = models.DateField(null=True)


class TaskManager(models.Manager):

    def with_counts(self):
        comp_count = User.objects.filter(task__status='complete').annotate(count=Count('task')).order_by('-count')
        ipor_count = User.objects.filter(task__status='inprogress').annotate(count=Count('task')).order_by('-count')
        prev = date.today().replace(day=1) - timedelta(days=1)
        last_month_comp = User.objects.filter(task__status='complete', task__completion_date__month=prev.month) \
            .annotate(count=Count('task')).order_by('-count')
        s_info = {}

        s_info['inprogress'] = (ipor_count[0].username, ipor_count[0].count) if ipor_count else ()
        s_info['complete'] = (comp_count[0].username, comp_count[0].count) if comp_count else ()
        s_info['last_month_complete'] = (
            last_month_comp[0].username, last_month_comp[0].count) if last_month_comp else ()
        return s_info
