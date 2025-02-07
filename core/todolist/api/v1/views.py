from rest_framework import viewsets
from todolist.models import Task
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskModelSerializer
from .paginations import TaskPaginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter
from accounts.models import Profile
from django.shortcuts import redirect

class TasktModelsViewSet(viewsets.ModelViewSet):
    model = Task
    permission_classes = [IsAuthenticated]
    serializer_class = TaskModelSerializer
    pagination_class = TaskPaginator
    filter_backends = [DjangoFilterBackend , SearchFilter,OrderingFilter]
    filterset_fields = ['completed','user']
    search_fields = ['title']
    ordering_fields = ['created_date']
    def get_queryset(self):
        user = Profile.objects.get(user__id = self.request.user.id)
        queryset = Task.objects.filter(user__id = user.id)
        return queryset
