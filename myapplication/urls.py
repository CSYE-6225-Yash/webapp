from django.urls import path, re_path
from . import views

urlpatterns = [
    path('healthz', views.insert_record),
    path('v1/file/<str:id>', views.handle_user_file),
    path('v1/file', views.handle_add_user_file),
    path('cicd', views.insert_record),
    re_path('.*', views.not_found, name="not found")
]