
from django.urls import path
from .views import users as users_views

app_name = 'users'

urlpatterns = [
    path('signup/', users_views.SingupView.as_view() , name='signup'),
]
