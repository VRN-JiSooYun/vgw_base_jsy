from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
# from kpviewer.functions import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from json import dumps
from django.views.decorators.csrf import csrf_exempt

import csv
import os
import base64
from PIL import Image
import io

import rdkit
from rdkit import Chem
from rdkit import DataStructs
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw

from django.db import connection, transaction
import django.db as db
import inspect

import requests
from datetime import date
import datetime
import json
# from program.models import *
# from compoundbank.models import *
from django.core import serializers
from itertools import chain
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login


# Create your views here.
def login_form_default(request):
    if request.method == 'POST':
        print("UserName::", request.POST.get('username'))
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("login_form_default::user:", user)
            return JsonResponse({'result' : 'success', 'next': request.POST.get('next'), 'form': 'default',}, json_dumps_params = {'ensure_ascii': True})
    else:
        form = AuthenticationForm()
        return render(request, 'member/login.html', {'form': form})

def login_form_sms(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return JsonResponse({'result' : 'success', 'form': 'sms',}, json_dumps_params = {'ensure_ascii': True})
        else:
            return JsonResponse({'result' : 'failed', 'form': 'sms',}, json_dumps_params = {'ensure_ascii': True})
    else:
        form = AuthenticationForm()
        return render(request, 'member/login.html', {'form': form})