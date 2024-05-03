from django import forms
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
import markdown2
import re
import random
from . import util

class NewTaskForms(forms.Form):
    task = forms.CharField(label="Entry")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page_content = util.get_entry(title)
    if page_content:
        return render(request, "encyclopedia/entry.html",{
            "title" : title,
            "content" : markdown2.markdown(page_content)
        })
    else:
        raise Http404("Entry not found")
    
def search(request):
    if request.method == "POST":
        title = request.POST.get("q")
        entrys = util.list_entries()
        for entry in entrys:
            if title.lower() == entry.lower():
                return redirect(f"wiki/{title}")
        matches = []
        for entry in entrys:
            if title.lower() in entry.lower():
                matches.append(entry)
                
        return render(request, "encyclopedia/search.html",{
            "matches" : matches
        })
    
    elif request.method == "GET":
        return redirect("/")
    

def new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    elif request.method == "POST":
        content = request.POST.get("new_entry")
        title = re.search(r"^\s*#\s+(.*)\n", content)
        if title == None:
            return render(request, "encyclopedia/new_page.html")
        entrys = util.list_entries()
        title = (title.group(1))[:-1]
        for entry in entrys:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/page_already_exist.html")
        util.save_entry(title,content)
        return redirect(f"/wiki/{title}")
    
    
def edit_entry(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        if content == None:
            return Http404
        return render(request, "encyclopedia/edit_entry.html",{
            "title" : title,
            "content" : content
        })
    elif request.method == "POST":
        content = request.POST.get("edit_entry")
        title2 = re.search(r"^\s*#\s+(.*)\n", content)
        print(content)
        print(title2)
        if title2 == None:
            return HttpResponse("Format not allowed")
        if title != (title2.group(1))[:-1]:
            return HttpResponse("Title not allowed")
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")
        
        
def random_page(request):
    entrys = util.list_entries()
    entry = random.choice(entrys)
    return redirect(f"/wiki/{entry}")