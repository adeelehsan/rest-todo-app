from rest_framework import serializers
from django.contrib.auth.models import User
from todo.models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ('url', 'id', 'user', 'title',
                  'description', 'creation_date', 'completion_date', 'log', 'status_choices')


class UserSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Task.objects.all())

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'tasks', 'joining_date')