from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django import forms
from . import models



# Create your views here.
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {'tasks': request.session["tasks"]})

def add(request):

    tasks = request.session["tasks"] or []
    if request.method == "POST":
        form = models.NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            # priority = form.cleaned_data["priority"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": models.NewTaskForm()
    })




