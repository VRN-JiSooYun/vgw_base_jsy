import datetime
import sys
import json
import requests
import socket
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator

from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, Count, F, Value, Max
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
from django.db.models import Case, When
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.forms.models import model_to_dict
from .functions import *

from multiprocessing import Process, Pool, Manager
from math import ceil
from .forms import QuillFieldForm

def getPostList(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    print("page_name:", page_name)

    pagesToLoad = []

    context = {
        'operation':'success', 
        'user_id': request.user.id,
        'url': '/' + app_name + '/inquiries', 
        'pk':'', 
        'page_name': page_name,
    }

    if 'order_by' in request.GET:
        order_by = request.GET['order_by']
    else:
        order_by = '-create_date'

    if 'category' in request.GET:
        category = request.GET['category']
        print("category:", category)

        post_list = inquiry_post.objects\
        .annotate(member_name=F('member__member_name'), category_name=F('category__category')).annotate(comments=Count('inquiry_post_comment__id'))\
        .annotate(best_comments=Count('inquiry_post_comment__id', filter=Q(inquiry_post_comment__check_best_comment=True)))\
        .annotate(latest_comment_create_date=Max('inquiry_post_comment__create_date'))\
        .filter(member__isnull=False).filter(**{'category__isnull':False}).filter(Q(category__page__page_name=page_name) & Q(category__category=category))\
        .values('id', 'category_name', 'title', 'title_en', 'content', 'member_id', 'member_name', 'create_date', 'comments', 'best_comments', 'latest_comment_create_date')\
        .order_by(
            Case(When(category_name='notice', then=0), default=1),
            order_by
        )

    else:
        post_list = inquiry_post.objects\
        .annotate(member_name=F('member__member_name'), category_name=F('category__category')).annotate(comments=Count('inquiry_post_comment__id'))\
        .annotate(best_comments=Count('inquiry_post_comment__id', filter=Q(inquiry_post_comment__check_best_comment=True)))\
        .annotate(latest_comment_create_date=Max('inquiry_post_comment__create_date'))\
        .filter(page__page_name=page_name).filter(member__isnull=False).filter(**{'category__isnull':False}).filter(**{'page__isnull':False})\
        .values('id', 'category_name', 'title', 'title_en', 'content', 'member_id', 'member_name', 'create_date', 'comments', 'best_comments', 'latest_comment_create_date')\
        .order_by(
            Case(When(category_name='notice', then=0), default=1),
            order_by
        )

    context['post_list_len'] = len(post_list)
    
    if 'post' in request.GET:
        post_id = request.GET['post']
        print("request user id:", request.user.id)
        print('post_id:', post_id)

        post = inquiry_post\
        .objects.annotate(member_name=F('member__member_name'), category_name=F('category__category'))\
        .filter(id=post_id).filter(**{'member__isnull':False}).filter(**{'category__isnull':False})\
        .values('id', 'category_name', 'title', 'title_en', 'content', 'member_id', 'member_name', 'create_date')

        # post_list = post_list.filter(category_name=post[0]['category_name'])

        if inquiry_post_comment.objects.filter(**{'post_id':post_id}).exists():
            comments = inquiry_post_comment.objects.filter(**{'post_id':post_id})\
            .values('id', 'post_id', 'parent_comment_id', 'parent_reply_id', 'member_id', 'member__member_name', 'content', 'create_date', 'modify_date', 'is_reply', 'check_best_comment')\
            .order_by('create_date')
        else:
            comments = inquiry_post_comment.objects.none()
        
        context['post'] = list(post)
        context['comments'] = list(comments.annotate(member_name=F('member__member_name')).values())

        pagesToLoad.append("inquiry-post")
    else:
        pagesToLoad.append("inquiry-post-form")
        categories = inquiry_category.objects.annotate(page_name=F('page__page_name')).filter(page__isnull = False).filter(page__page_name=page_name).values()
        context['categories'] = list(categories)
    
    ################################################################################################################
    ################################################################################################################
    # sort by 연관 키워드
    ################################################################################################################
    ################################################################################################################
    if 'inquiry-post-keyword' in request.POST:
        keyword_category = request.POST['inquiry-post-keyword-category']
        inquiry_keyword = request.POST['inquiry-post-keyword']
        print("keyword_category:", keyword_category)
        print("inquiry_keyword:", inquiry_keyword)

        if keyword_category == 'title':
            post_list = post_list.filter(title__icontains=inquiry_keyword)
        elif keyword_category == 'content':
            post_list = post_list.filter(content__icontains=inquiry_keyword)
        elif keyword_category == 'writer':
            post_list = post_list.filter(member__member_name__icontains=inquiry_keyword)

    if 'on' in request.GET:
        page_num = request.GET['on']
        # page_num = 1
        paginator = Paginator(post_list, 20)
        post_list = paginator.get_page(page_num)
        print("page_num on:", page_num)
    else:
        paginator = Paginator(post_list, 20)
        post_list = paginator.get_page(1)
        print("page_num off:", 1)

    context['paginator'] = {'number': post_list.number, 'num_pages': paginator.num_pages, 'start_index': post_list.start_index(), 'end_index': post_list.end_index()}
    context["pagesToLoad"] = pagesToLoad
    context['data'] = list(post_list)

    ################################################################################################################
    ################################################################################################################
    # sort by similarity
    ################################################################################################################
    ################################################################################################################
    # if 'post' in request.GET and socket.gethostname() == 'Voronoi':
    #     try:        
    #         x = requests.post(
    #             'http://127.0.0.1:59500/nlp/get/',
    #             data={
    #                 'query_post': json.dumps(post[0]),
    #                 'post_list': json.dumps(list(post_list)),
    #             },
    #         )
    #         post_list = json.loads(x.text)['post_list']
    #         context['data'] = list(post_list)
    #         print("nlp model is working")
    #     except:
    #         print("nlp model is not working")

    auth = get_authority_status(request, page_name)
    print("auth:", auth)

    context['is_p'] = 1 if auth.get('P') else 0
    context['is_r'] = 1 if auth.get('R') else 0
    context['is_v'] = 1 if auth.get('V') else 0
    context['is_d'] = 1 if auth.get('D') else 0
        
    return JsonResponse(context)
