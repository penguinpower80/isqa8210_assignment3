from django.urls import path

from . import views
app_name = 'tech'

urlpatterns = [
                  path('', views.home, name='home'),
    ]