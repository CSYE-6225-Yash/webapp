from django.urls import path, re_path
from . import views

urlpatterns = [
    path('healthz', views.insert_record),
    re_path('.*', views.not_found)
]