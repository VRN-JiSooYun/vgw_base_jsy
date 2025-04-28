import datetime
import sys
import json
import base64
import itertools
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, Count, F, Value, Case, When, IntegerField
from django.views.generic import *
# from program.models import *
from django.apps import apps
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, AllChem, rdDepictor, MolsFromPNGString
from rdkit.Chem.Draw import MolsToImage, MolsToGridImage, MolToFile, rdMolDraw2D, MolToImageFile
from django.db import connection
from django.core import serializers
from member.models import *
from django.db.models import F
from .models import *
from datetime import datetime
from .forms import QuillFieldForm
from .functions import *

@login_required(login_url='/security/login/')
def inquiryHowToUse(request):
    if request.method == 'GET':
        page_name = request.GET['page']

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id

        inquiry_how_tos = inquiry_how_to.objects.filter(inquiry_page_id=inquiry_page_id)\
            .values('id', 'parent_how_to_id', 'title', 'content', 'order_value')\
            .annotate(custom_order=Case(
                When(parent_how_to_id=None, then=Value(1)),
                default=Value(2),
            ))\
            .order_by('custom_order', 'parent_how_to_id', 'order_value')

        # auth = ai_authority(request)
        auth = get_authority_status(request, page_name)
        print("auth:", auth)

        context = {
            'form': QuillFieldForm(),
            "pagesToLoad": ["inquiry-how-to-use"],
            "inquiry_how_tos": inquiry_how_tos,
            "check_superuser": Profile.objects.get(member_id=Member.objects.get(user_id=request.user.id)).check_freepass,
            'is_p': 1 if auth.get('P') else 0,
            'is_r': 1 if auth.get('R') else 0,
            'is_v': 1 if auth.get('V') else 0,
            'is_d': 1 if auth.get('D') else 0,
        }

        return render(request, page_name + '/inquiry_module.html', context)

def inquiryAddHowToUse(request):
    if request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        id_for_parent = request.GET['slide']
        title = request.POST['title']
        content = json.loads(request.POST['content'])['html']

        for k in request.POST:
            print('key:', k, ', value:', request.POST[k])

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id

        inquiry_how_to.objects.create(**{
            "inquiry_page_id": inquiry_page_id,
            "parent_how_to_id": None if id_for_parent == "null" or id_for_parent == "undefined" else id_for_parent,
            "title": title,
            "content": content,
        })
        
        # return render(request, 'inquiry/inquiry_module.html', context)
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries/how-to-use', 'pk':'', 'inquiry_type':'', 'page_name': page_name})

def inquiryModifyHowToUse(request):
    if request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        title = request.POST['title']
        content = json.loads(request.POST['content'])['html']
        how_to_id = request.GET['slide']
        parent_how_to_id = request.GET['parent']

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id

        if inquiry_how_to.objects.filter(inquiry_page_id=inquiry_page_id).exists():
            inquiry_how_to.objects.filter(id=int(how_to_id)).update(**{
                "inquiry_page_id": inquiry_page_id,
                "parent_how_to_id": None if parent_how_to_id == "null" or parent_how_to_id == "undefined" else int(parent_how_to_id),
                "title": title,
                "content": content,
            })
        
        # return render(request, 'inquiry/inquiry_module.html', context)
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries/how-to-use', 'pk':'', 'inquiry_type':'', 'page_name': page_name})

def inquiryDeleteHowToUse(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']
    slide = request.GET['slide']

    if inquiry_page.objects.filter(page_name=page_name).exists():
        inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
    else:
        inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id
    
    inquiry_how_to.objects.filter(Q(inquiry_page_id=inquiry_page_id) & Q(id=slide)).delete()
    
    return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries/how-to-use', 'pk':'', 'inquiry_type':'', 'page_name': page_name})

def resetInquiryHowToUse(request):
    if request.method == 'GET':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id
        
        inquiry_how_to.objects.filter(inquiry_page_id=inquiry_page_id).delete()
        
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries/how-to-use', 'pk':'', 'inquiry_type':'', 'page_name': page_name})

def sortInquiryHowToUse(request):
    if request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id

        idList = list(map(int, json.loads(request.POST['id-list'])))
        parentList = json.loads(request.POST['parent-list'])
        sortingIndexList = list(map(int, json.loads(request.POST['sorting-index-list'])))

        i = 0
        for id in idList:
            inquiry_how_to.objects.filter(id=id).update(**{
                'parent_how_to_id': int(parentList[i]) if parentList[i] != None else None,
                'order_value': int(sortingIndexList[i]),
            })
            i += 1

        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries/how-to-use', 'pk':'', 'inquiry_type':'', 'page_name': page_name})
