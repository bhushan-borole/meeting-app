from django.urls import path

from .views import login, dashboard, all_meetings, delete_meeting, \
                   add_meeting, edit_meeting, add_task, assign_task, \
                   all_tasks, delete_task, edit_task


urlpatterns = [
    path('', login, name='login'),
    path('dashboard/', dashboard),
    path('all_meetings/', all_meetings),
    path('delete_meeting/<int:id>/', delete_meeting),
    path('add_meeting/', add_meeting),
    path('edit_meeting/<int:id>/', edit_meeting),
    path('add_task/', add_task),
    path('assign_task/<int:mid>/', assign_task),
    path('all_tasks/', all_tasks),
    path('delete_task/<int:id>/', delete_task),
    path('edit_task/<int:id>/', edit_task)
]
