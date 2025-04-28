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

@login_required(login_url='/security/login/')
def getInquiryPage(request):
    print("request:", request.user.username)

    category = request.GET.get('category')
    if category == 'open':
        category = 'AND post.check_hide == 0'
    elif category == 'close':
        category = 'AND post.check_hide == 1'
    else:
        category = ''
    
    context = {
        "inquiry_category_list": blind_category.objects.all(),
        "user_id": request.user.id,
        "check_superuser": Profile.objects.get(member_id=Member.objects.get(user_id=request.user.id)).check_freepass,
    }

    post_list = blind_post.objects.raw(f"""
        SELECT
            post.id, post.title, post.content, post.member_id, post.create_date, member.member_name, category.category AS category_name, COUNT(comment.id) AS comments, post.check_hide,
            COUNT(comment.id) FILTER (WHERE comment.check_best_comment) AS "best_comments", 
            MAX(comment.create_date) AS latest_comment_create_date
        FROM inquiry_blind_post post
        LEFT JOIN member_member member ON post.member_id = member.id
        LEFT JOIN inquiry_blind_category category ON post.category_id = category.id
        LEFT OUTER JOIN inquiry_blind_post_comment comment ON post.id = comment.post_id AND comment.check_discard=False
        WHERE post.check_discard=False {category}
        GROUP BY post.id, member.member_name, category.category 
        ORDER BY post.create_date DESC
    """)
    
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

    post = blind_post.objects.none()
    if 'post' in request.GET:
        post_id = request.GET['post']
        print("request user id:", request.user.id)
        print('post_id:', post_id)

        if blind_post.objects.filter(id=post_id).exists():

            post = blind_post.objects.annotate(member_name=F('member__member_name'))\
            .filter(id=post_id).filter(**{'member__isnull':False})\
            .values('id', 'title', 'content', 'member_id', 'member_name', 'create_date', 'check_hide')[0]

            print("post:::",len(post))
            # post_list = post_list.filter(category_name=post['category_name'])

            # print("context:", context)

            #============================================================================================
            # comments
            #============================================================================================
            if blind_post_comment.objects.filter(**{'post_id':post_id}).exists():
                comments = blind_post_comment.objects.filter(**{'post_id':post_id}).filter(check_discard=False)\
                .values('id', 'post_id', 'parent_comment_id', 'parent_reply_id', 'member_id', 'member__member_name', 'content', 'create_date', 'modify_date', 'is_reply', 'check_best_comment', 'check_anonymity')\
                .order_by('create_date')

            else:
                comments = blind_post_comment.objects.none()

            context["inquiry_post"] = post
            context["inquiry_post_comment"] = comments
            context["pagesToLoad"].append("inquiry-post")

        else:
            context["pagesToLoad"].append("inquiry-post-form")
    else:
        context["pagesToLoad"].append("inquiry-post-form")
    
    context['post_list'] = post_list
    context["quill_form"] = QuillFieldForm()

    # auth = get_authority_status(request, page_name)
    # print("auth:", auth)

    context['is_p'] = 1 if request.user.email == 'jaeheon12@voronoi.io' or request.user.email == 'hong@voronoi.io' or request.user.email == 'boram@voronoi.io' else 0
    context['is_r'] = 1 if request.user.email == 'jaeheon12@voronoi.io' or request.user.email == 'hong@voronoi.io' or request.user.email == 'boram@voronoi.io' else 0
    context['is_v'] = 1 if request.user.email == 'jaeheon12@voronoi.io' or request.user.email == 'hong@voronoi.io' or request.user.email == 'boram@voronoi.io' else 0
    context['is_d'] = 0

    return render(request, 'inquiry/blind_page.html', context)

def writeInquiryPost(request):
    if request.method == 'GET':
        # print(type(inquiry_category))
        context = {
            "inquiry_category_list": blind_category.objects.all(),
            "user_id": request.user.id,
            "check_superuser": Profile.objects.get(member_id=Member.objects.get(user_id=request.user.id)).check_freepass,
            "pagesToLoad": ["inquiry-post-form"]
        }
        return render(request, 'inquiry/blind_page.html', context)
    elif request.method == 'POST':
        category = request.POST['inquiry-category']
        password = request.POST['post-password']
        inquiry_title = request.POST['write-inquiry-post-title']
        # inquiry_content = request.POST['write-inquiry-post-content']
        inquiry_content = json.loads(request.POST['content'])['html']

        n = blind_post.objects.create(**{
            'member': Member.objects.get(user_id=request.user.id),
            'title': inquiry_title,
            'content': inquiry_content,
            'check_hide': True if category == 'close' else False
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

                    if ':8000' in request.build_absolute_uri('') or ':30080' in request.build_absolute_uri('') or 'localhost' in request.build_absolute_uri('') or '127.0.0.1' in request.build_absolute_uri(''):
                        if user.email == writer.email:
                            # receiverEmail += request.user.email + ('' if user == user_list[len(user_list) - 1] else ',')
                            pass
                    else:
                        receiverEmail += 'hong@voronoi.io,boram@voronoi.io,jaeheon12@voronoi.io'

                        origin_path = request.build_absolute_uri('')
                        # urlToPost = origin_path[:origin_path.rfind('/')] + '?page=' + page_name + '&post=' + str(n.id)
                        urlToPost = origin_path.replace('/write-question', '') + '&post=' + str(n.id)
                        print("urlToPost:", urlToPost)
                        print("receiverEmail:", receiverEmail)

                        emailTitle = '[Blind] 문의 게시판에 새 글이 등록되었습니다.'
                        emailContents = '<h3>안녕하세요. VORONOI GROUPWARE에서 알립니다.</h3><br>'+ \
                                        '작성자: ' + Member.objects.get(user_id=writer.id).member_name + '<br><br>' + \
                                        '제목: <a href="' + urlToPost + '">' + inquiry_title + '</a><br><br>'

                        email_service = gmail_authenticate()
                        message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
                        send_message(email_service, "me", message)
                        # 의뢰등록 메일 발송 E
        except Exception as e:
            print("Exception::", e)

        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':n.id})

def writeInquiryComment(request):
    if request.method == 'POST':
        post_id = request.POST['inquiry-post-id']
        content = request.POST['write-inquiry-post-comment']
        anonymous = request.POST['anonymous']
        print('post_id:', post_id)
        print('anonymous:', anonymous)

        n = blind_post_comment.objects.create(**{
            'post_id': post_id,
            'member': Member.objects.get(user_id=request.user.id),
            'content': content,
            'is_reply': False,
            'check_anonymity': 1 if anonymous == 'true' else 0
        })

        blind_post.objects.filter(id=post_id).update(check_comment=True)
        writer = blind_post.objects.filter(id=post_id)[0].member.user
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

                    if ':8000' in request.build_absolute_uri('') or ':30080' in request.build_absolute_uri('') or 'localhost' in request.build_absolute_uri('') or '127.0.0.1' in request.build_absolute_uri(''):
                        if user.email == writer.email:
                            receiverEmail += request.user.email + ('' if user == user_list[len(user_list) - 1] else ',')
                    else:
                        receiverEmail += 'hong@voronoi.io'
                
                origin_path = request.build_absolute_uri('')
                # urlToPost = origin_path[:origin_path.rfind('/')] + '?page=' + page_name + '&post=' + str(post_id)
                urlToPost = origin_path.replace('/write-comment', '') + '?post=' + str(post_id)
                print("urlToPost:", urlToPost)

                print("receiverEmail:", receiverEmail)

                emailTitle = '[Blind] 문의 게시판에 댓글이 등록되었습니다.'
                emailContents = '<h3>안녕하세요. VORONOI GROUPWARE에서 알립니다.</h3><br>'+ \
                                '작성자: ' + Member.objects.get(user_id=comment_writer.id).member_name + '<br><br>' + \
                                '<a href="' + urlToPost + '">게시글로 이동</a><br><br>'

                # email_service = gmail_authenticate()
                # message = create_message("vgw@voronoi.io", receiverEmail, emailTitle, emailContents)
                # send_message(email_service, "me", message)
                # 의뢰등록 메일 발송 E
        except Exception as e:
            print("Exception::", e)

        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})

def writeInquiryReply(request):
    if request.method == 'POST':
        post_id = request.POST['inquiry-post-id']
        parent_comment_id = request.POST['inquiry-parent-comment-id']
        content = request.POST['write-inquiry-comment-reply']
        anonymous = request.POST['anonymous']

        n = blind_post_comment.objects.create(**{
            'post_id': post_id,
            'parent_comment_id': parent_comment_id,
            'member': Member.objects.get(user_id=request.user.id),
            'content': content,
            'is_reply': True,
            'check_anonymity': 1 if anonymous == 'true' else 0
        })
        
        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})

def deleteInquiryPost(request):
    if request.method == 'GET':
        post_id = request.GET['post']

        # blind_post_comment.objects.filter(post_id=post_id).delete()
        # blind_post.objects.filter(id=post_id).delete()
        blind_post.objects.filter(id=post_id).update(**{'check_discard': True})

        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk': ''})

def deleteInquiryComment(request):
    if request.method == 'GET':
        post_id = request.GET['post']
        comment_id = request.GET['comment']

        # blind_post_comment.objects.filter(id=comment_id).delete()
        blind_post_comment.objects.filter(id=comment_id).update(**{'check_discard': True})

        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})

def cancelBestComment(request):
    if request.method == 'GET':
        post_id = request.GET['post']
        comment_id = request.GET['comment']

        blind_post_comment.objects.filter(id=comment_id).update(**{
            'check_best_comment': False
        })

        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})

def checkBestComment(request):
    if request.method == 'GET':
        post_id = request.GET['post']
        exits = blind_post_comment.objects.filter(Q(post_id=post_id) & Q(check_best_comment=True)).exists()
        
        return JsonResponse({'operation':'success', 'best_comment': exits})

def selectBestComment(request):
    if request.method == 'GET':
        post_id = request.GET['post']
        comment_id = request.GET['comment']
        
        blind_post_comment.objects.filter(post_id=post_id).update(**{
            'check_best_comment': False
        })

        blind_post_comment.objects.filter(id=comment_id).update(**{
            'check_best_comment': True
        })

        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})

def getPostList(request):
    pagesToLoad = []

    category = request.GET.get('category')

    context = {
        'operation':'success', 
        'user_id': request.user.id,
        'url': '/inquiry/blind', 
        'pk':'', 
    }

    if 'order_by' in request.GET:
        order_by = request.GET['order_by']
    else:
        order_by = '-create_date'
    
    # results = Table1.objects.annotate(table2_count=Count('table2', filter=Q(table2__column2=True))).filter(table2_count__gt=0)

    post_list = blind_post.objects.filter(check_discard=False)\
        .annotate(member_name=F('member__member_name'), category_name=F('category__category')).annotate(comments=Count('blind_post_comment__id', filter=Q(blind_post_comment__check_discard=False)))\
        .annotate(best_comments=Count('blind_post_comment__id', filter=Q(blind_post_comment__check_best_comment=True)))\
        .annotate(latest_comment_create_date=Max('blind_post_comment__create_date')).filter(member__isnull=False)\
        .values('id', 'category_name', 'title', 'content', 'member_id', 'member_name', 'create_date', 'check_hide', 'comments', 'best_comments', 'latest_comment_create_date')\
        .order_by(
            Case(When(category_name='notice', then=0), default=1),
            order_by
        )
    
    print(post_list.query)
    
    if category == 'open':
        post_list = post_list.filter(check_hide=0)
    elif category == 'close':
        post_list = post_list.filter(check_hide=1)

    context['post_list_len'] = len(post_list)
    
    if 'post' in request.GET:
        post_id = request.GET['post']
        print("request user id:", request.user.id)
        print('post_id:', post_id)

        post = blind_post\
        .objects.annotate(member_name=F('member__member_name'))\
        .filter(id=post_id).filter(**{'member__isnull':False})\
        .values('id', 'title', 'content', 'member_id', 'member_name', 'create_date', 'check_hide')

        # post_list = post_list.filter(category_name=post[0]['category_name'])

        if blind_post_comment.objects.filter(**{'post_id':post_id}).exists():
            comments = blind_post_comment.objects.filter(**{'post_id':post_id}).filter(check_discard=False)\
            .values('id', 'post_id', 'parent_comment_id', 'parent_reply_id', 'member_id', 'member__member_name', 'content', 'create_date', 'modify_date', 'is_reply', 'check_best_comment', 'check_anonymity')\
            .order_by('create_date')
        else:
            comments = blind_post_comment.objects.none()
        
        context['post'] = list(post)
        context['comments'] = list(comments.annotate(member_name=F('member__member_name')).values())

        pagesToLoad.append("inquiry-post")
    else:
        pagesToLoad.append("inquiry-post-form")
        categories = blind_category.objects.all().values()
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

    # auth = get_authority_status(request, page_name)
    # print("auth:", auth)

    # context['is_p'] = 1 if auth.get('P') else 0
    # context['is_r'] = 1 if auth.get('R') else 0
    # context['is_v'] = 1 if auth.get('V') else 0
    # context['is_d'] = 1 if auth.get('D') else 0
    context['is_p'] = 1 if request.user.email == 'jaeheon12@voronoi.io' or request.user.email == 'hong@voronoi.io' or request.user.email == 'boram@voronoi.io' else 0
    context['is_r'] = 1 if request.user.email == 'jaeheon12@voronoi.io' or request.user.email == 'hong@voronoi.io' or request.user.email == 'boram@voronoi.io' else 0
    context['is_v'] = 1 if request.user.email == 'jaeheon12@voronoi.io' or request.user.email == 'hong@voronoi.io' or request.user.email == 'boram@voronoi.io' else 0
    context['is_d'] = 0
        
    return JsonResponse(context)

def modifyInquiryPost(request):
    if request.method == 'POST':
        post_id = request.POST['inquiry-post-id']
        category = request.POST['inquiry-category']
        inquiry_title = request.POST['write-inquiry-post-title-to-modify']
        # inquiry_content = request.POST['write-inquiry-post-content-to-modify']
        inquiry_content = json.loads(request.POST['content'])['html']

        n = blind_post.objects.filter(id=post_id).update(**{
            'member': Member.objects.get(user_id=request.user.id),
            'title': inquiry_title,
            'content': inquiry_content,
            'modify_date': datetime.datetime.now(),
            'check_hide': True if category == 'close' else False
        })

        # return redirect('/inquiry/inquiries?posts=' + inquiryType + '&post=' + str(n.id))
        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})

def modifyInquiryComment(request):
    if request.method == 'POST':
        post_id = request.POST['inquiry-post-id']
        comment_id = request.POST['inquiry-comment-id']
        content = request.POST['inquiry-comment-content']
        print('comment_id:', comment_id)
        print('content:', content)

        n = blind_post_comment.objects.filter(id=comment_id).update(**{
            'member': Member.objects.get(user_id=request.user.id),
            'content': content,
            'modify_date': datetime.datetime.now()
        })

        # inquiry_post.objects.filter(id=post_id).update(check_comment=True)
        
        # return redirect('/inquiry/inquiries?posts=' + inquiryType + '&post=' + post_id)
        return JsonResponse({'operation':'success', 'url': '/inquiry/blind', 'pk':post_id})
