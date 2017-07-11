from rest_framework.views import APIView

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
from todo.permissions import IsOwnerOrReadOnly
from django.db.models import Count
from datetime import date, timedelta


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
    serializer_class = UserSerializer

    # def perform_create(self, serializer):
    #
    #     if not serializer.is_valid():
    #         return JsonResponse(serializer.errors,\
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     user = User(username=self.request.data['username'],
    #                                            password=self.request.data['password'])
    #     user.save()
    #     serializer.save(user=user)
    #     return JsonResponse(serializer.data, status=201)


class SummaryView(APIView):

    def get(self, request):
        user_count = int(request.data.get('user_count', 3))
        start_date = request.data.get('start_date', '2017-01-01')
        start_date = start_date.split('-')
        start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = request.data.get('end_date')
        if end_date:
            end_date = end_date.split('-')
            end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        else:
            end_date = date.today()
        users = User.objects.filter(tasks__status='complete', tasks__completion_date__range=(start_date, end_date)).\
            annotate(count=Count('tasks')).order_by('-count')
        userinfo = ['%s has completed %s Tasks' % (user.username, user.count) for user in users[:user_count]]
        return Response(userinfo)
