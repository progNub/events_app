from django.contrib import admin
from django.urls import path, include

from accounts.api import views

app_name = 'api'

urlpatterns = [
    path('users/', views.ListUserApiView.as_view(), name='api-list-users'),
]
