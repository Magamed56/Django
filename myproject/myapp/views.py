from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, LoginForm, DocumentForm
from .models import Topic, Document
from django.http import HttpResponse, Http404
from django.conf import settings
import os
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic

@login_required
def download_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)

    # Проверяем, что файл существует
    if os.path.exists(document.zip_file.path):
        with open(document.zip_file.path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.zip_file.path)}"'
            return response
    else:
        raise Http404("Файл не найден.")
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    # Если пользователь авторизован, показываем доступные темы и выбранную тему
    if request.user.is_authenticated:
        topics = Topic.objects.filter(selected_by__isnull=True)
        selected_topic = Topic.objects.filter(selected_by=request.user).first()
        return render(request, 'home.html', {
            'topics': topics,
            'selected_topic': selected_topic,
            'user': request.user,
        })
    else:
        # Если пользователь не авторизован, показываем только кнопки регистрации и авторизации
        return render(request, 'home.html', {'user': request.user})



@login_required
def select_topic(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)

    # Освобождаем старую тему, если она была выбрана
    old_topic = Topic.objects.filter(selected_by=request.user).exclude(id=topic_id)
    if old_topic.exists():
        old_topic.update(selected_by=None)

    # Выбираем новую тему
    topic.selected_by = request.user
    topic.save()

    return redirect('home')

@login_required
def upload_document(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.topic = topic
            document.user = request.user
            document.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'upload.html', {'form': form, 'topic': topic})

@login_required
def view_documents(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    documents = Document.objects.filter(topic=topic)
    return render(request, 'documents.html', {'documents': documents})