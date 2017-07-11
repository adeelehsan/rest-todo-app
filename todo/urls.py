from django.conf.urls import url
from django.conf.urls import include
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import views as auth_views
from todo import views

urlpatterns = format_suffix_patterns([
    url(r'^register/$', views.RegistrationView.as_view()),
    url(r'^summary/$', views.SummaryView.as_view()),
    url(r'^$', views.api_root),
    url(r'^todo/$',
        views.TaskList.as_view(),
        name='task-list'),
    url(r'^todo/(?P<pk>[0-9]+)/$',
        views.TaskDetail.as_view(),
        name='task-detail'),
    # url(r'^snippets/(?P<pk>[0-9]+)/highlight/$',
    #     views.SnippetHighlight.as_view(),
    #     name='snippet-highlight'),
    url(r'^users/$',
        views.UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        views.UserDetail.as_view(),
        name='user-detail')
])

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    # url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
]