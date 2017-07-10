from todo.models import Task, User
from todo.serializers import UserSerializer
from todo.serializers import TaskSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import render
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
    # renderer_classes = [TemplateHTMLRenderer]
    # template_name = 'templates/todo/index.html'

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        if user.has_perm('todo.can_view'):
            #return Task.objects.all()
            todo_list = Task.objects.all()
            return Response({'todo_list': todo_list})
        else:
            #return Task.objects.filter(user=user)
            todo_list = Task.objects.filter(user=user)
            return Response({'todo_list': todo_list})

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


class RegistrationView(APIView):
    """ Allow registration of new users. """
    permission_classes = ()

    def post(self, request):
        serializer = TaskSerializer(data=request.data, context={'request': request})

        # Check format and unique constraint
        if not serializer.is_valid():
            return JsonResponse(serializer.errors,\
                            status=status.HTTP_400_BAD_REQUEST)
        data = request.data

        u = User.objects.create(username=data.pop('username'))
        u.set_password(data.pop('password'))
        u.save()
        serializer.save(user=u)
        return JsonResponse(serializer.data, status=201)
