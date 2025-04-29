import os
from django.db.models import Q, Count, F, Value
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.urls import reverse
from home.functions import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from home.code_singleton import Code





#################################################################################
#################################################################################
#################################################################################
#
#                                  Home
#
#################################################################################
#################################################################################
#################################################################################

@login_required(login_url='/security/login/')
def home_view(request):
    # redirect dashboard
    update_active_hrlayout_to_home_mysettings_and_list_up_my_hrlayout_to_member(request)

    # if 'voronoi.app' in request._current_scheme_host :
    #     return redirect('dashboard-home')
    # else :
    #     return redirect('my-home')

    # return redirect('my-home')
    return redirect('utilities-home')

    template = 'home/home.html'
    if request.method == 'GET':
        context = home_function(request)
        return render(request, template, context)

@login_required(login_url='/security/login/')
def re_home_view(request):
    # return redirect('re-home')
    return redirect('utilities-home')

@csrf_exempt
def get_codes(request) :
    return JsonResponse({"codes" : Code().getCodes()}, safe=False)

@csrf_exempt
def get_code_dtls(request) :
    return JsonResponse({"codeDtls" : Code().getCodeDtls()}, safe=False)