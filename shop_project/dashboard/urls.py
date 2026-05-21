from django.urls import path
from .views import dashboard_view

app_name = 'dashboard'
urlpattenrs = [
    path('', dashboard_view, name='dashboard'),
]