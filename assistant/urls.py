from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('success/', views.post_success, name='post_success'),
    path('settings/', views.settings_menu, name='settings_menu'),
]