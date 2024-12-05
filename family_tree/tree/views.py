from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Страница приложения tree")

def person_tree(request, person_id):
    return HttpResponse(f"<h1>Дерево для человека с id - </h1>{person_id}</p>")
