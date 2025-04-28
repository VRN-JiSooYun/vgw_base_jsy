from django.urls import path, include
from re_todo.views import *

urlpatterns = [
    # page
    path('todo-view', list_page, name='re-todo-home'),
    path('todo-history-view', history_page, name='re-todo-history'),

    # api
    path('createTodo', create_todo, name='create-todo'),
    path('getTodayTodos', get_today_todos, name='get-today-todos'),
    path('getTodos', get_todos, name='get-todos'),
    path('getTodo/<int:todoKey>', get_todo, name='get-todo'),

    path('updateTodo/<int:todoKey>', update_todo, name='update-todo'),
    path('updateCheckDone/<int:todoKey>', update_check_done, name='update-check-done'),

    path('deleteTodo/<int:todoKey>', delete_todo, name='delete-todo'),
]