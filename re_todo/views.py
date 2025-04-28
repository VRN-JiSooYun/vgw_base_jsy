from django.shortcuts import render
from re_todo.functions import *
from re_group.functions import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

@login_required(login_url='/security/login/')
def list_page(request) :
    print("list_page :", request.user.id)
    context = {}
    return render(request, "todo_list.html", context)

@login_required(login_url='/security/login/')
def history_page(request) :
    print("history_page :", request.user.id)
    tree = getGroupByMemberId(request)
    if not tree:
        tree = ""
    else :
        tree = json.loads(tree.toJSON())
    context = {
        "tree": tree
    }
    return render(request, "todo_history.html", context)

@csrf_exempt
def create_todo(request) :
    print("create_todo :", request.user.id)
    if request.method == "POST":
        process = createTodo(request)
        return JsonResponse(process, safe=False)

@csrf_exempt
def get_today_todos(request) :
    print("get_today_todos :", request.user.id)
    return JsonResponse(list(getTodayTodos(request.user.id).values()), safe=False)

@csrf_exempt
def get_todos(request) :
    print("get_todos :", request.user.id)
    return JsonResponse(getTodos(request), safe=False)

@csrf_exempt
def get_todo(request, todoKey) :
    print("get_todo :", request.user.id, todoKey)
    return JsonResponse(model_to_dict(getTodo(todoKey)), safe=False)

@csrf_exempt
def update_todo(request, todoKey) :
    print("update_todo :", request.user.id, todoKey)
    if request.method == "POST":
        process = updateTodo(request, todoKey)
        return JsonResponse(process, safe=False)

@csrf_exempt
def update_check_done(request, todoKey) :
    print("update_check_done :", request.user.id, todoKey)
    if request.method == "POST":
        process = updateCheckDone(request, todoKey)
        return JsonResponse(process, safe=False)

@csrf_exempt
def delete_todo(request, todoKey) :
    print("delete_todo :", request.user.id, todoKey)
    if request.method == "POST":
        process = deleteTodo(todoKey)
        return JsonResponse(process, safe=False)
