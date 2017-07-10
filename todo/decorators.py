# from .models import Task
#
# def user_has_perm(function):
#     def wrap(request):
#         if request.user.has_perm('todo.can_view'):
#             task = Task.objects.all()
#             return function(request, task)
#         else:
#             task = Task.objects.filter(user=request.user)
#             return function(request, task)
#     return wrap