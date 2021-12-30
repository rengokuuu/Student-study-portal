from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('notes/', notes, name='notes'),
    path('notes/notes/<int:pk>', delete_note, name='delete-note'),
    path('notes/note_detail/<int:pk>',
         NoteDetailView.as_view(), name='note-detail'),

    path('homework/', homework, name='homework'),
    path('homework/delete_homework/<int:pk>',
         delete_homework, name='delete-homework'),
    path('homework/update_homework/<int:pk>',
         update_homework, name='update-homework'),

    path('todo/', todo, name='todo'),
    path('todo/delete_todo/<int:pk>', delete_todo, name='delete-todo'),
    path('path/update_todo/<int:pk>', update_todo, name='update-todo'),

    path('books/', books, name='books'),

    path('dictionary/', dictionary, name='dictionary'),

    path('wiki/', wiki, name='wiki')

]
