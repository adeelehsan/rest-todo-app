from django.core.management.base import BaseCommand, CommandError
from todo.models import Task, User
from todo.serializers import UserSerializer


class Command(BaseCommand):
    help = 'Add users and there tasks'
    # users = [
    #     {'username': 'N', "password": 'neo123', 'tasks'
    #     : [{'title': 'Learning Django', 'description': 'Learning to Change Team', 'status': 'inprogress'}]}
    # ]
    users = [
        User(username='fury1', password='fury123', tasks=
        [Task(title='Learning Django', description='Learning to Change Team', status='inprogress')])
    ]

    def handle(self, *args, **options):
        for user_data in self.users:
            try:
                user = User.objects.create(username=user_data['username'],
                                           password=user_data['password'])
                user.save()
                for task_data in user_data['tasks']:
                    task = Task(title=task_data['title'], description=
                                task_data['description'], status=task_data['status'], user=user)
                    task.save()
            except:
                raise CommandError('Unable to create user')
            self.stdout.write(self.style.SUCCESS("Successfully User's data was entered"))


        # try:
        #       User.objects.bulk_create(self.users)
        # except:
        #     raise CommandError('Unable to create user')
        # self.stdout.write(self.style.SUCCESS("Successfully User's data was entered"))

