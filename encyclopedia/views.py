import random
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from re import search
from django.contrib import messages
import markdown2

from . import util

class NewEntryForm(forms.Form):
    entryName = forms.CharField(label="New Entry Name")
    entryContent = forms.CharField(label="New Entry Content", help_text="", widget=forms.Textarea())


def index(request):
    if request.method == "GET" and 'q' in request.GET:
        entryName = request.GET["q"]
        entry = util.get_entry(entryName) 
        if entry:
            entry_htm = markdown2.markdown(entry)
            return render(request, "encyclopedia/entry.html", {
            "entryName": entryName,
            "entry_content": entry_htm
            })
        else:
            list = util.list_entries()
            res = []
            for word in list:
                temp = word.lower()
                if search(entryName, temp):
                    res.append(word)
            if res:        
                return render(request, "encyclopedia/search.html", {
                "results": res
                })
            else:
                return HttpResponse("There's no entry matching your search query :(")
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })



def getEntry(request, entryName):
    entry = util.get_entry(entryName)
    if entry:
        entry_htm = markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "entryName": entryName,
            "entry_content": entry_htm
        })
    else:
        return render(request, "encyclopedia/error.html")

def editEntry(request, editEntryName):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_name = form.cleaned_data["entryName"]
            entry_content = form.cleaned_data["entryContent"]
            entry_htm = markdown2.markdown(entry_content)
            util.save_entry(entry_name, entry_content)
            return render(request, "encyclopedia/entry.html", {
            "entryName": entry_name,
            "entry_content": entry_htm
            })
        else:
            messages.error(request, "Invalid Form Data")
            return render(request, "encyclopedia/newpage.html", {
                    "form" : form,
                    "enName" : editEntryName
                })
    else: 
        editEntry = util.get_entry(editEntryName)
        form = NewEntryForm(initial={'entryName' : editEntryName, 'entryContent': editEntry })
        return render(request, "encyclopedia/editpage.html", {
        "form" : form,
        "enName" : editEntryName
        })
    

def newPage(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            list = util.list_entries()
            entry_name = form.cleaned_data["entryName"]
            entry_content = form.cleaned_data["entryContent"]
            if entry_name not in list:
                util.save_entry(entry_name, entry_content)
                return HttpResponseRedirect(reverse("getEntry", kwargs={'entryName':entry_name}))
            else:
                messages.error(request, "Entry already in encyclopedia.")
                return render(request, "encyclopedia/newpage.html", {
                    "form" : form
                })
    else:    
        return render(request, "encyclopedia/newpage.html", {
        "form" : NewEntryForm()
        })
    
def randomPage(request):
    list = util.list_entries()
    randEntry = random.choice(list)
    randEntry_cont = util.get_entry(randEntry)
    rand_htm = markdown2.markdown(randEntry_cont)
    return render(request, "encyclopedia/entry.html", {
        "entryName": randEntry,
        "entry_content": rand_htm
    })








