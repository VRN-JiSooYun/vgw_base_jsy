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
from django.db.models import Max, Q, Count, F, Value
from django.views.generic import *
# from program.models import *
from django.apps import apps
from member.models import *
from django.db.models import F
from .models import *
from django.db.models import Case, When
from .functions import *
# from .core import *
from .forms import *
from django.views.decorators.csrf import csrf_exempt

@login_required(login_url='/security/login/')
@csrf_exempt
def getInquiryPage(request):
    print("request:", request.user.username)
    
    # app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    context = {
        "inquiry_category_list": inquiry_category.objects.annotate(page_name=F('page__page_name')).filter(page__isnull = False).filter(page__page_name=page_name),
        "user_id": request.user.id,
        "check_superuser": Profile.objects.get(member_id=Member.objects.get(user_id=request.user.id)).check_freepass,
    }

    post_list = inquiry_post.objects.all()

    if 'category' in request.GET:
        category = request.GET['category']

        post_list = inquiry_post.objects\
        .annotate(member_name=F('member__member_name'), category_name=F('category__category')).annotate(comments=Count('inquiry_post_comment__id'))\
        .annotate(best_comments=Count('inquiry_post_comment__id', filter=Q(inquiry_post_comment__check_best_comment=True)))\
        .annotate(latest_comment_create_date=Max('inquiry_post_comment__create_date'))\
        .filter(member__isnull=False).filter(**{'category__isnull':False}).filter(Q(category__page__page_name=page_name) & Q(category__category=category))\
        .values('id', 'category_name', 'title', 'title_en', 'content', 'member_id', 'member_name', 'create_date', 'comments', 'best_comments', 'latest_comment_create_date')\
        .order_by(
            Case(When(category_name='notice', then=0), default=1),
            '-create_date'
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
            '-create_date',
        )
    
    context['post_list_len'] = len(post_list)

    if 'on' in request.GET:
        page_num = request.GET['on']
        print('on:', page_num)
        paginator = Paginator(post_list, 20)
        post_list = paginator.get_page(page_num)
    else:
        print('off:', 1)
        paginator = Paginator(post_list, 20)
        post_list = paginator.get_page(1)

    context["pagesToLoad"] = ["inquiry-post-list"]

    post = inquiry_post.objects.none()
    if 'post' in request.GET:
        post_id = request.GET['post']
        print("request user id:", request.user.id)
        print('post_id:', post_id)

        if inquiry_post.objects.filter(id=post_id).exists():

            # print("post_list:", post_list)

            # post_list = post_list.order_by(
            #     Case(When(id=post_id, then=0), default=1),
            # )
            # context["post_list"] = post_list

            post = inquiry_post\
            .objects.annotate(member_name=F('member__member_name'), category_name=F('category__category'))\
            .filter(id=post_id).filter(**{'member__isnull':False}).filter(**{'category__isnull':False})\
            .values('id', 'category_name', 'title', 'title_en', 'content', 'member_id', 'member_name', 'create_date')[0]

            print("post:::",len(post))
            # post_list = post_list.filter(category_name=post['category_name'])

            # print("context:", context)

            #============================================================================================
            # comments
            #============================================================================================
            if inquiry_post_comment.objects.filter(**{'post_id':post_id}).exists():
                comments = inquiry_post_comment.objects.filter(**{'post_id':post_id})\
                .values('id', 'post_id', 'parent_comment_id', 'parent_reply_id', 'member_id', 'member__member_name', 'content', 'create_date', 'modify_date', 'is_reply', 'check_best_comment')\
                .order_by('create_date')

            else:
                comments = inquiry_post_comment.objects.none()

            context["inquiry_post"] = post
            context["inquiry_post_comment"] = comments
            context["pagesToLoad"].append("inquiry-post")

        else:
            context["pagesToLoad"].append("inquiry-post-form")
    else:
        context["pagesToLoad"].append("inquiry-post-form")
    
    context['post_list'] = post_list
    context["quill_form"] = QuillFieldForm()

    #================================================================================================
    # sort by similarity
    #================================================================================================
    # if 'post' in request.GET and socket.gethostname() == 'Voronoi':
    #     try:
    #         x = requests.post(
    #             'http://127.0.0.1:59500/nlp/get/',
    #             data={
    #                 'query_post': json.dumps(post),
    #                 'post_list': json.dumps(list(post_list)),
    #             },
    #         )
    #         post_list = json.loads(x.text)['post_list']
    #         context['post_list'] = list(post_list)
    #         print("nlp model is working")
    #     except:
    #         print("nlp model is not working")

    auth = get_authority_status(request, page_name)
    print("auth:", auth)

    context['is_p'] = 1 if auth.get('P') else 0
    context['is_r'] = 1 if auth.get('R') else 0
    context['is_v'] = 1 if auth.get('V') else 0
    context['is_d'] = 1 if auth.get('D') else 0

    return render(request, page_name + '/inquiry_module.html', context)

@csrf_exempt
def writeInquiryPost(request):
    if request.method == 'GET':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        
        # print(type(inquiry_category))
        context = {
            "inquiry_category_list": inquiry_category.objects.annotate(page_name=F('page__page_name')).filter(page__isnull = False).filter(page__page_name=page_name),
            "user_id": request.user.id,
            "check_superuser": Profile.objects.get(member_id=Member.objects.get(user_id=request.user.id)).check_freepass,
            "pagesToLoad": ["inquiry-post-form"]
        }
        return render(request, page_name + '/inquiry_module.html', context)
    elif request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        category = request.POST['inquiry-category']
        inquiry_title = request.POST['write-inquiry-post-title']
        # inquiry_content = request.POST['write-inquiry-post-content']
        inquiry_content = json.loads(request.POST['content'])['html']

        if inquiry_page.objects.filter(page_name=page_name).exists():
            inquiry_page_id = inquiry_page.objects.filter(page_name=page_name)[0].id
        else:
            inquiry_page_id = inquiry_page.objects.create(**{'page_name': page_name}).id

        # inquiry_category.objects.filter(page__isnull = False).filter(Q(page__page_name=page_name) & Q(category="general"))

        if inquiry_category.objects.filter(Q(page_id=inquiry_page_id) & Q(category=category)).exists():
            inquiry_category_id = inquiry_category.objects.filter(Q(page_id=inquiry_page_id) & Q(category=category))[0].id
        else:
            inquiry_category_id = inquiry_category.objects.create(**{
                'page_id': inquiry_page_id,
                'category': category
            }).id

        n = inquiry_post.objects.create(**{
            'page_id': inquiry_page_id,
            'category_id': inquiry_category_id,
            'member': Member.objects.get(user_id=request.user.id),
            'title': inquiry_title,
            # 'title_en': translate(inquiry_title),
            'title_en': '',
            'content': inquiry_content,
        })

        writer = User.objects.get(id=request.user.id)

        try :
            with transaction.atomic() :
                user_list = User.objects.all()
                receiverEmail = ''

                for user in user_list:
                    request.user = user
                    # print(request.user)

                    if '@' not in request.user.email:
                        continue

                    auth = get_authority_status(request, page_name)

                    if ':8000' in request.build_absolute_uri(''):
                        if user.email == writer.email:
                            receiverEmail += request.user.email + ('' if user == user_list[len(user_list) - 1] else ',')
                    elif auth.get('D') or user.email == 'jhchoi@voronoi.io' or user.email == 'hsk@voronoi.io' or user.email == 'k3363@voronoi.io' or user.email == 'jaeheon12@voronoi.io':
                        receiverEmail += request.user.email + ('' if user == user_list[len(user_list) - 1] else ',')
                
                index = 0
                while index <= 100:
                    if receiverEmail[-1] == ',':
                        receiverEmail = receiverEmail[:-1]
                    else:
                        break
                    index += 1
                
                origin_path = request.build_absolute_uri('')
                # urlToPost = origin_path[:origin_path.rfind('/')] + '?page=' + page_name + '&post=' + str(n.id)
                urlToPost = origin_path.replace('/write-question', '') + '?page=' + page_name + '&post=' + str(n.id)
                print("urlToPost:", urlToPost)
                print("page_name:", page_name)
                print("receiverEmail:", receiverEmail)

                emailTitle = '[' + page_name + '] 문의 게시판에 새 글이 등록되었습니다.'
                emailContents = '<h3>안녕하세요. VORONOI GROUPWARE에서 알립니다.</h3><br>'+ \
                                '작성자: ' + Member.objects.get(user_id=writer.id).member_name + '<br><br>' + \
                                '제목: <a href="' + urlToPost + '">' + inquiry_title + '</a><br><br>'

                email_service = gmail_authenticate()
                message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
                send_message(email_service, "me", message)
                # 의뢰등록 메일 발송 E
        except Exception as e:
            print("Exception::", e)

        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':n.id, 'page_name': page_name})

@csrf_exempt
def writeInquiryComment(request):
    if request.method == 'POST':
        app_name = request.path.split('/')[1]
        page_name = request.GET['page']
        post_id = request.POST['inquiry-post-id']
        content = request.POST['write-inquiry-post-comment']
        print('post_id:', post_id)

        n = inquiry_post_comment.objects.create(**{
            'post_id': post_id,
            'member': Member.objects.get(user_id=request.user.id),
            'content': content,
            'is_reply': False
        })

        inquiry_post.objects.filter(id=post_id).update(check_comment=True)
        writer = inquiry_post.objects.filter(id=post_id)[0].member.user
        comment_writer = User.objects.get(id=request.user.id)

        try :
            with transaction.atomic() :
                user_list = User.objects.all()
                receiverEmail = ''

                for user in user_list:
                    request.user = user
                    # print(request.user)

                    if '@' not in request.user.email:
                        continue

                    auth = get_authority_status(request, page_name)

                    if ':8000' in request.build_absolute_uri(''):
                        if user.email == writer.email:
                            receiverEmail += request.user.email + ('' if user == user_list[len(user_list) - 1] else ',')
                    elif auth.get('D') or user.email == writer.email or user.email == 'jhchoi@voronoi.io' or user.email == 'hsk@voronoi.io' or user.email == 'k3363@voronoi.io' or user.email == 'jaeheon12@voronoi.io':
                        receiverEmail += request.user.email + ('' if user == user_list[len(user_list) - 1] else ',')
                
                index = 0
                while index <= 100:
                    if receiverEmail[-1] == ',':
                        receiverEmail = receiverEmail[:-1]
                    else:
                        break
                    index += 1
                
                origin_path = request.build_absolute_uri('')
                # urlToPost = origin_path[:origin_path.rfind('/')] + '?page=' + page_name + '&post=' + str(post_id)
                urlToPost = origin_path.replace('/write-comment', '') + '?page=' + page_name + '&post=' + str(post_id)
                print("urlToPost:", urlToPost)
                print("page_name:", page_name)
                print("receiverEmail:", receiverEmail)

                emailTitle = '[' + page_name + '] 문의 게시판에 댓글이 등록되었습니다.'
                emailContents = '<h3>안녕하세요. VORONOI GROUPWARE에서 알립니다.</h3><br>'+ \
                                '작성자: ' + Member.objects.get(user_id=comment_writer.id).member_name + '<br><br>' + \
                                '<a href="' + urlToPost + '">게시글로 이동</a><br><br>'

                email_service = gmail_authenticate()
                message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
                send_message(email_service, "me", message)
                # 의뢰등록 메일 발송 E
        except Exception as e:
            print("Exception::", e)

        
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})

def writeInquiryReply(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    if request.method == 'POST':
        post_id = request.POST['inquiry-post-id']
        parent_comment_id = request.POST['inquiry-parent-comment-id']
        content = request.POST['write-inquiry-comment-reply']

        n = inquiry_post_comment.objects.create(**{
            'post_id': post_id,
            'parent_comment_id': parent_comment_id,
            'member': Member.objects.get(user_id=request.user.id),
            'content': content,
            'is_reply': True
        })
        
        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})

def deleteInquiryPost(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    if request.method == 'GET':
        post_id = request.GET['post']

        inquiry_post_comment.objects.filter(post_id=post_id).delete()
        inquiry_post.objects.filter(id=post_id).delete()

        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk': '', 'page_name': page_name})

def deleteInquiryComment(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    if request.method == 'GET':
        post_id = request.GET['post']
        comment_id = request.GET['comment']

        inquiry_post_comment.objects.filter(id=comment_id).delete()

        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})

def cancelBestComment(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    if request.method == 'GET':
        post_id = request.GET['post']
        comment_id = request.GET['comment']

        inquiry_post_comment.objects.filter(id=comment_id).update(**{
            'check_best_comment': False
        })

        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})

def checkBestComment(request):
    if request.method == 'GET':
        post_id = request.GET['post']
        exits = inquiry_post_comment.objects.filter(Q(post_id=post_id) & Q(check_best_comment=True)).exists()
        
        return JsonResponse({'operation':'success', 'best_comment': exits})

def selectBestComment(request):
    app_name = request.path.split('/')[1]
    page_name = request.GET['page']

    if request.method == 'GET':
        post_id = request.GET['post']
        comment_id = request.GET['comment']
        
        inquiry_post_comment.objects.filter(post_id=post_id).update(**{
            'check_best_comment': False
        })

        inquiry_post_comment.objects.filter(id=comment_id).update(**{
            'check_best_comment': True
        })

        return JsonResponse({'operation':'success', 'url': '/' + app_name + '/inquiries', 'pk':post_id, 'page_name': page_name})
    