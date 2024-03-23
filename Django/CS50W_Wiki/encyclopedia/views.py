from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from random import choice
from django import forms
from django.urls import reverse
from numpy import size
from . import util
import markdown2


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": "40", "rows": "3"}), label="Content")

class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": "40", "rows": "3"}), label="Content")



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title in util.list_entries():
        content = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return HttpResponseNotFound(render(request, "encyclopedia/404.html", {
            "title": title
        }))
    
def random(request):
    title = choice(util.list_entries())
    # Generate the URL for the 'entry' URL pattern dynamically
    url = reverse('entry', kwargs={'title': title})
    return HttpResponseRedirect(url)


def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "title": "Create New Page",
                    "error": "The title already exists."  # Add the error message to the render context
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form,
                "title": "Create New Page"
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "form": NewEntryForm(),
            "title": "Create New Page",
        })
    
def edit(request, title):
    try:
        content = util.get_entry(title)
    except FileNotFoundError:
        return HttpResponseNotFound(render(request, "encyclopedia/404.html", {
            "title": title
        }))
    
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data["content"]
            util.save_entry(title, new_content)
            return HttpResponseRedirect(reverse("entry", kwargs={'title': title}))
    else:
        form = EditEntryForm(initial={"content": content})
    
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": form,
    })


def search(request):
    query = request.GET.get('q', '')
    if query in util.list_entries():
        return HttpResponseRedirect(reverse("entry", kwargs={'title': query}))
    else:
        entries = util.list_entries()
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })