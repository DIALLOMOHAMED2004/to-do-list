from django.urls import path
from .views import TaskCreateView,TaskListView,TaskUpdateView, TaskDeleteView,TaskCompleteView,TaskExportView,TaskImportView

urlpatterns = [
    path('create/', TaskCreateView.as_view(), name='task-create'),
    path('list/', TaskListView.as_view(), name='task-list'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task-delete'),
    path('<int:pk>/complete/', TaskCompleteView.as_view(), name='task-complete'),
    path('export/', TaskExportView.as_view(), name='task-export'),
    path('import/', TaskImportView.as_view(), name='task-import'),
]
