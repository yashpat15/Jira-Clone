from django.urls import path
from .views import (project_list, project_create, project_detail, register,
                    update_issue_status, user_profile, create_issue, custom_logout)
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', LoginView.as_view(template_name='core/login.html'), name='login'),
    path('projects/', project_list, name='project-list'),
    path('projects/new/', project_create, name='project-create'),
    path('projects/<int:pk>/', project_detail, name='project-detail'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('update_issue_status/', update_issue_status, name='update-issue-status'),
    path('profile/', user_profile, name='user-profile'),
    path('api/project/<int:project_id>/create_issue/', create_issue, name='create_issue_api'),
]

