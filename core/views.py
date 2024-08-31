from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Project, Issue
from .forms import ProjectForm, IssueForm
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404
from .models import Project, Issue
from django.http import JsonResponse
from .forms import IssueForm
from .models import Project, Issue

def home(request):
    return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password2']

        if password != password_confirm:
            return render(request, 'core/register.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'core/register.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password)
        return redirect('login')  # Redirect to the login page after successful registration

    return render(request, 'core/register.html')
@login_required
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'core/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.creator = request.user
            project.save()
            return redirect('project-list')
    else:
        form = ProjectForm()
    return render(request, 'core/project_form.html', {'form': form})


def project_detail(request, pk):
    project = Project.objects.get(pk=pk)
    issues_open = project.issues.filter(status='OPEN')
    issues_in_progress = project.issues.filter(status='IN_PROGRESS')
    issues_closed = project.issues.filter(status='CLOSED')
    
    context = {
        'project': project,
        'issues_open': issues_open,
        'issues_in_progress': issues_in_progress,
        'issues_closed': issues_closed,
    }
    return render(request, 'core/project_detail.html', context)

@csrf_exempt
@require_POST
def update_issue_status(request):
    data = json.loads(request.body)
    issue_id = data.get('issue_id')
    new_status = data.get('new_status')
    issue = Issue.objects.get(id=issue_id)
    issue.status = new_status
    issue.save()
    return JsonResponse({'status': 'success', 'issue_id': issue_id, 'new_status': new_status})
@login_required
def user_profile(request):
    return render(request, 'core/profile.html', {'user': request.user})

@login_required
def project_list(request):
    query = request.GET.get('q', '')  # Retrieve search query if present
    if query:
        projects = Project.objects.filter(name__icontains=query)
    else:
        projects = Project.objects.all()
    return render(request, 'core/project_list.html', {'projects': projects})

@require_POST  # Ensures that only POST requests can access this view
def custom_logout(request):
    logout(request)
    return redirect('home')  # Redirect to a homepage or login page

def create_issue(request, project_id):
    if request.method == 'POST':
        form = IssueForm(request.POST, request.FILES)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.project = Project.objects.get(id=project_id)
            issue.save()
            return JsonResponse({
                'status': 'success',
                'issue_id': issue.id,
                'title': issue.title,
                'description': issue.description,
                'issue_status': issue.status  
            }, status=200)
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors.as_json()}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
