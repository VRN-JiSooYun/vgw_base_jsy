from django.shortcuts import render
from re_auth.functions import *
# from project.views import authority
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/security/login/')
def view_page(request) :
    print("view_page :", request.user.id)
    # auth = authority("hr", request)
    auth = False
    if auth["D"] == True :
        context = {
            "tree": json.loads(getGroupTree().toJSON())
        }
        return render(request, "auth_view.html", context)
    else :
        return render(request, "auth_access_auth.html")

@csrf_exempt
def get_auth(request) :
    print("get_auth :", request.user.id)
    if request.method == "GET":
        authority = getAuth()
        return JsonResponse(model_to_dict(authority), safe=False)

@csrf_exempt
def get_targets(request) :
    print("get_targets :", request.user.id)
    return JsonResponse(getTargets(), safe=False)

@csrf_exempt
def update_auth(request) :
    print("update_auth :", request.user.id)
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        process = updateAuth(data["auths"], request.user.id)
        return JsonResponse(process, safe=False)