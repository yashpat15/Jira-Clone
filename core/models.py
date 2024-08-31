#models.py
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Issue(models.Model):
    STATUS_CHOICES = [
    ('to_do', 'To Do'),
    ('in_progress', 'In Progress'),
    ('done', 'Done'),
]
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default='to_do')
    assigned_to =  models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
