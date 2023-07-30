from django.urls import path
from .views import task_list_view, task_detail_view, task_create_view


app_name = 'api'

urlpatterns = [
    path('', task_list_view, name='task_list'),
    path('create/', task_create_view, name='task_create'),
    path('<int:pk>/', task_detail_view, name='task_detail')
]