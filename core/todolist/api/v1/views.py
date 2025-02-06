from rest_framework import viewsets
from todolist.models import Task
from rest_framework.permissions import IsAuthenticated
from .serializers import TaskModelSerializer
from .paginations import TaskPaginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter , OrderingFilter


class TasktModelsViewSet(viewsets.ModelViewSet):
    model = Task
    def get_queryset(self):
        queryset = Task.objects.filter(user__id = self.request.user.id)
        
        return queryset
   
    permissions_classes = [IsAuthenticated]
    serializer_class = TaskModelSerializer
    pagination_class = TaskPaginator
    filter_backends = [DjangoFilterBackend , SearchFilter,OrderingFilter]
    filterset_fields = ['completed','user']
    search_fields = ['title']
    ordering_fields = ['created_date']
