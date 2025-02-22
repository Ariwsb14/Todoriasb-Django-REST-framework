from django.urls import path , include
from .views import LoginPageView ,  CreateUserView , LogoutView

app_name = 'accounts'
urlpatterns = [
    path('signup/',CreateUserView.as_view(),name='signup'),
    path('login/',LoginPageView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('api/v1/',include('accounts.api.v1.urls'))

]