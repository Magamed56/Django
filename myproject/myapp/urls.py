from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.home, name='home'),
    path('select_topic/<int:topic_id>/', views.select_topic, name='select_topic'),
    path('upload/<int:topic_id>/', views.upload_document, name='upload'),
    path('documents/<int:topic_id>/', views.view_documents, name='view_documents'),
    path('download/<int:document_id>/', views.download_document, name='download_document'),
]