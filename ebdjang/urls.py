
from django.contrib import admin
from django.urls import path,include
from core.views import TestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('data/',TestView.as_view(),name='deen')
]
