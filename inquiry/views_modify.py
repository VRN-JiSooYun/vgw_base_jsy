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
from django.db.models import Q, Count, F, Value
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

def modifyInquiryPost(request):
    if request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        post_id = request.POST['inquiry-post-id']
        category = request.POST['inquiry-category']
        inquiry_title = request.POST['write-inquiry-post-title-to-modify']
        # inquiry_content = request.POST['write-inquiry-post-content-to-modify']
        inquiry_content = json.loads(request.POST['content'])['html']

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id

        # inquiry_category.objects.filter(page__isnull = False).filter(Q(page__page_name=page_name) & Q(category="general"))

        if inquiry_category.objects.filter(Q(page_id=inquiry_page_id) & Q(category=category)).exists():
            inquiry_category_id = inquiry_category.objects.filter(category=category)[0].id
        else:
            inquiry_category_id = inquiry_category.objects.create(**{
                'page_id': inquiry_page_id,
                'category': category
            }).id

        n = inquiry_post.objects.filter(id=post_id).update(**{
            'page_id': inquiry_page_id,
            'category_id': inquiry_category_id,
            'member': Member.objects.get(user_id=request.user.id),
            'title': inquiry_title,
            'content': inquiry_content,
            'modify_date': datetime.now()
        })

        # return redirect('/inquiry/inquiries?posts=' + inquiryType + '&post=' + str(n.id))
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})


def modifyInquiryComment(request):
    if request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        post_id = request.POST['inquiry-post-id']
        comment_id = request.POST['inquiry-comment-id']
        content = request.POST['inquiry-comment-content']
        print('comment_id:', comment_id)
        print('content:', content)

        n = inquiry_post_comment.objects.filter(id=comment_id).update(**{
            'member': Member.objects.get(user_id=request.user.id),
            'content': content,
            'modify_date': datetime.now()
        })

        # inquiry_post.objects.filter(id=post_id).update(check_comment=True)
        
        # return redirect('/inquiry/inquiries?posts=' + inquiryType + '&post=' + post_id)
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})
