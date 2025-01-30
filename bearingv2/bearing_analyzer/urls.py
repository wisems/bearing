from django.contrib import admin
from django.urls import path
from analyzer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('create-directory/', views.create_directory, name='create_directory'),
    path('capture-images/<int:dir_id>/', views.capture_images, name='capture_images'),
    path('run-analysis/<int:dir_id>/', views.run_analysis, name='run_analysis'),
]