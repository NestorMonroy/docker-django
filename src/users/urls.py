
from django.urls import path
from src.users.views import users as users_views

app_name = 'users'

urlpatterns = [
    path('signup/', users_views.SingupView.as_view() , name='signup'),
    path('login/', users_views.LoginView.as_view() , name='login'),
]
