from django.urls import path 
from .views import *
app_name = 'todolist'
urlpatterns = [
    path('',TaskListView.as_view(),name='tasklist'),
    path('create/',TaskCreateView.as_view(),name='taskcreate'),
    path('<int:pk>/delete/',TaskDeleteView.as_view(),name='taskdelete'),
    path('<int:pk>/complete/',TaskCompleteView.as_view(),name='taskcomplete'),
    path('<int:pk>/reset/',TaskResetView.as_view(),name='taskreset'),
    path('<int:pk>/edit/',TaskEditView.as_view(),name='taskedit'),
]