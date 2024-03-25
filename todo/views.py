from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse, HttpResponseNotFound
from django.core.handlers.wsgi import WSGIRequest
from .models import Todo
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
import json

@require_GET
def todo(request: WSGIRequest):
    todos = Todo.objects.all()
    todos_list = []
    for t in todos:
        todos_list.append(model_to_dict(t))
    
    return JsonResponse(data=todos_list, safe=False)

@require_GET
def get_todo(request: WSGIRequest, number):
    
    todos = Todo.objects.filter(id=number)
    
    todos_list = []
    for t in todos:
        todos_list.append(model_to_dict(t))
        
        
    return JsonResponse(data=todos_list, safe=False)

@require_POST
@csrf_exempt
def create_todo(request: WSGIRequest):
    body = json.loads(request.body.decode("utf-8"))
    
    name = body.get("name")
    is_done = body.get("is_done")
    
    new_todo = Todo(name=name, is_done=is_done)
    
    new_todo.save()
    
    return JsonResponse(data=model_to_dict(new_todo))

@require_http_methods("PATCH")
@csrf_exempt
def edit_todo(request: WSGIRequest, id: int):
    body = json.loads(request.body.decode("utf-8"))
    
    name = body.get("name")
    is_done = body.get("is_done")
    
    editing_todo = Todo.objects.get(id=id)
    
    if name is not None:
        editing_todo.name = name
    
    if is_done is not None:
        editing_todo.is_done = is_done
        
    editing_todo.save()
    
    return JsonResponse(data=model_to_dict(editing_todo))

@require_http_methods("DELETE")
@csrf_exempt
def delete_todo(request: WSGIRequest, id: int):
    
    deleting_todo = Todo.objects.get(id=id)
    
    deleting_todo.delete()
    
    return HttpResponse(f"Todo with id {id} is deleted.")