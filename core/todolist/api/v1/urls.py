from django.urls import path , include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'api-v1'

router = DefaultRouter()
router.register('task',views.TasktModelsViewSet,basename='tasks')
urlpatterns = router.urls