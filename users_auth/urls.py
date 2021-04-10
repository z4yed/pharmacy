from django.urls import path
from . import views

app_name = 'users_auth'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_url'),
    path('register', views.RegistrationView.as_view(), name='registration'),
    path('users_list', views.UserList.as_view(), name='users_list'),
    path('update-user/<int:profile_id>', views.UpdateUser.as_view(), name='update_user'),
    path('remove-user/<int:profile_id>', views.RemoveUser.as_view(), name='remove_user'),
]
