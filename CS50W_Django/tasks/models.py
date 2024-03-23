from django.db import models
from django import forms
# Create your models here.

class Task(models.Model):
    name = models.CharField(max_length=64)
    priority = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.priority})"
    
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    # priority = forms.IntegerField(label="Priority", min_value=1, max_value=5)
