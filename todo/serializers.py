from rest_framework import serializers
from django.contrib.auth.models import User
from todo.models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    #status = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ('url', 'id', 'user', 'title',
                  'description', 'creation_date', 'completion_date', 'log', 'status_choices', 'status')

    # def get_status(self, obj):
    #     return obj.get_status_display()


class UserSerializer(serializers.ModelSerializer):
    # tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'tasks', 'joining_date')

    def create(self, validated_data):
        tasks_data = validated_data.pop('tasks')
        user = User.objects.create(**validated_data)
        for task_data in tasks_data:
            Task.objects.create(user=user, **task_data)
        return user