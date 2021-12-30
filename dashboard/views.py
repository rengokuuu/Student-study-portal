from django import contrib
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import DetailView
import requests
import wikipedia
from .models import *
from .forms import *
# Create your views here.

# Notes section begin here


def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):

    # by doing this will get notes of particular user rather than all of the notes created by all users
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(
                user=request.user, title=request.POST['title'], description=request.POST['description'])
            notes.save()
        messages.success(
            request, f"{request.user.username} notes added successfully.")
    else:
        form = NotesForm()
    # this step is going to get all the notes created by that login user
    notes = Notes.objects.filter(user=request.user)
    context = {
        'notes': notes,
        'form': form
    }
    return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')


class NoteDetailView(DetailView):
    model = Notes

# Homework sections begin here


def homework(request):
    homework = Homework.objects.filter(user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False

    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            homeworks = Homework(user=request.user,
                                 subject=request.POST['subject'],
                                 title=request.POST['title'],
                                 description=request.POST['description'],
                                 due=request.POST['due'],
                                 is_finished=finished)
            homeworks.save()
            messages.success(request, f'Homework added successfully.')
    else:
        form = HomeworkForm()

    context = {
        'homeworks': homework,
        'homework_done': homework_done,
        'form': form,
    }
    return render(request, 'dashboard/homework.html', context)


def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')


def update_homework(request, pk):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')

# todo app starts


def todo(request):
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        todo_done = True
    else:
        todo_done = False

    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(user=request.user,
                         title=request.POST['title'],
                         is_finished=finished)
            todos.save()
            messages.success(request, f'todo added successfully.')
    else:
        form = TodoForm()

    context = {
        'todos': todo,
        'todo_done': todo_done,
        'form': form,
    }
    return render(request, 'dashboard/todo.html', context)


def update_todo(request, pk):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')


def delete_todo(request, pk):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')

# Books app start here


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q='+text
        r = requests.get(url)
        ans = r.json()
        result_list = []
        for i in range(10):
            result_dict = {
                'title': ans['items'][i]['volumeInfo']['title'],
                'subtitle': ans['items'][i]['volumeInfo'].get('subtitle'),
                'description': ans['items'][i]['volumeInfo'].get('description'),
                'count': ans['items'][i]['volumeInfo'].get('pageCount'),
                'categories': ans['items'][i]['volumeInfo'].get('categories'),
                'rating': ans['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': ans['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': ans['items'][i]['volumeInfo'].get('previewLink'),
            }
            result_list.append(result_dict)
            context = {
                'form': form,
                'results': result_list
            }
        return render(request, 'dashboard/books.html', context)
    form = DashboardForm()
    context = {
        'form': form
    }
    return render(request, 'dashboard/books.html', context)


def dictionary(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/'+text
        r = requests.get(url)
        ans = r.json()
        try:
            phonetics = ans[0]['phonetics'][0]['text']
            audio = ans[0]['phonetics'][0]['audio']
            definition = ans[0]['meanings'][0]['definitions'][0]['definition']
            example = ans[0]['meanings'][0]['definitions'][0]['example']
            synonyms = ans[0]['meanings'][0]['definitions'][0]['synonyms']

            context = {
                'form': form,
                'input': text,
                'phonetics': phonetics,
                'audio': audio,
                'definition': definition,
                'example': example,
                'synonyms': synonyms
            }
        except:
            context = {
                'form': form,
                'input': ''
            }
        return render(request, 'dashboard/dictionary.html', context)

    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        search = wikipedia.page(text)
        context = {
            'form': form,
            'title': search.title,
            'link': search.url,
            'details': search.summary
        }
        return render(request, 'dashboard/wiki.html', context)
    else:
        form = DashboardForm()
        context = {
            'form': form
        }
    return render(request, 'dashboard/wiki.html', context)
