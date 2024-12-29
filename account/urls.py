from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('user-panel/', views.user_panel, name='user_panel'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('delete-account/', views.account_delete_view, name='delete_account'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
