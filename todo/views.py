import json

from todo.models import Task, User
from todo.serializers import UserSerializer
from todo.serializers import TaskSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from todo.permissions import IsOwnerOrReadOnly


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format)
    })


class TaskList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user.has_perm('todo.can_view'):
            todo_list = Task.objects.all()
            return todo_list
        else:
            todo_list = Task.objects.filter(user=user)
            return todo_list

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RegistrationView(generics.CreateAPIView):
    """ Allow registration of new users. """
    permission_classes = ()
    # serializer_class = TaskSerializer

    def get_serializer_class(self, **kwargs):
        if kwargs.get('user'):
            return UserSerializer
        return TaskSerializer

    def perform_create(self, serializer):

        if not serializer.is_valid():
            return JsonResponse(serializer.errors,\
                            status=status.HTTP_400_BAD_REQUEST)

        # user = User(username=self.request.data['username'],
        #                                        password=self.request.data['password'])
        # user.save()
        self.get_serializer_class(user=True)
        user = serializer.save()
        # user_serializer = UserSerializer(data=self.request.data, many=True)
        # if serializer.is_valid():
        #     user = serializer.save()
        self.get_serializer_class()
        serializer.save(user=user)
        return JsonResponse(serializer.data, status=201)
