from django.shortcuts import render, redirect
import markdown2
import random
from django.contrib import messages
from .models import WikiPage
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()})


def page(request, title):
    entries = [item.lower() for item in util.list_entries()]
    if title.lower() in entries:
        body = util.get_entry(title)
        html = markdown2.markdown(body)
        return render(request, "encyclopedia/wikipage.html", context={"title":title ,"body":html})
    return render(request, "encyclopedia/notfound.html")

def search(request):
    if request.method == "POST":
        query = request.POST["query"]
        entries = [item.lower() for item in util.list_entries()]
        if query in entries:
            body = util.get_entry(query)
            html = markdown2.markdown(body)
            return render(request, "encyclopedia/wikipage.html", context={"title":query ,"body":html})
        result = []
        for entry in entries:
            if query in entry:
                result.append(entry)

        return render(request, "encyclopedia/search.html", {"query":query, "result":result})

def create_new_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        if title not in util.list_entries():
            util.save_entry(title, content)
            WikiPage(title=title, content=content).save()
            return redirect('wiki-page', title=title)    
        
        else :
            messages.warning(request, "Page with this title already exists.")
            return render(request, "encyclopedia/newpage.html", context={"title": title, "body": content})
    
    return render(request, "encyclopedia/newpage.html", context={"title":"", "body": ""})

def edit_page(request, title):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        util.save_entry(title, content)
        page = WikiPage.objects.get(title=title)
        page.content = content
        page.save() 
        return redirect('wiki-page', title=title) 

    body = util.get_entry(title)
    return render (request, "encyclopedia/newpage.html", context={"title":title, "body": body})

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    body = util.get_entry(title)
    html = markdown2.markdown(body)
    return render(request, "encyclopedia/wikipage.html", context={"title":title ,"body":html})