from django.http import HttpResponse, HttpResponseRedirect
from http.client import HTTPResponse
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import Markdown
from random import randint

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="New Entry")
    textarea = forms.CharField(widget=forms.Textarea)

class EditEntryForm(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea)

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    if util.get_entry(name) is None:
        return render(request, "encyclopedia/error.html", {
            "error": "Entry does not exist"
        })
    else:
        parsed_content = markdowner.convert(util.get_entry(name))
        return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": parsed_content
        })

def search(request):
    q = request.GET["q"]

    if util.get_entry(q):
        parsed_content = markdowner.convert(util.get_entry(q))
        return render(request, "encyclopedia/entry.html", {
            "name": util.get_entry(q),
            "entry": parsed_content
        })

    matchedEntries = []
    for entry in util.list_entries():
        if q in entry:
            matchedEntries.append(entry)

    if matchedEntries:
        return render(request, "encyclopedia/search.html", {
            "entries": matchedEntries
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "error": "This entry does not exist"
        })

def add(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                "error": "This entry already exists"
                })
            else:
                # f = open(f"./entries/{title}.md", "a")
                # f.write(textarea)
                util.save_entry(title, textarea)
                parsed_content = markdowner.convert(textarea)
                return render(request, "encyclopedia/entry.html", {
                "name": title,
                "entry": parsed_content
                })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })

def edit(request, name):
    if request.method == "GET":
        my_entry = util.get_entry(name)
        return render(request, "encyclopedia/edit.html", {
            'form': EditEntryForm(initial={'textarea': my_entry}),
            'name': name
        })

    else:
        form = EditEntryForm(request.POST)
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(name, textarea)
            my_entry = util.get_entry(name)
            parsed_content = markdowner.convert(textarea)
            return render(request, "encyclopedia/entry.html", {
            "name": name,
            "entry": parsed_content
            })
        else:
            return render(request, "encyclopedia/edit.html")

def random(request):
    entries = util.list_entries()
    n = randint(0, len(entries) -1)
    name = entries[n]
    parsed_content = markdowner.convert(util.get_entry(name))
    return render(request, "encyclopedia/entry.html", {
    "name": name,
    "entry": parsed_content
    })

