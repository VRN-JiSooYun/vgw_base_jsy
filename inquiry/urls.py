from django.urls import path, include
# from compoundpatentability.views import *
from django.conf import settings
from . import views, views_post_list, views_category, views_modify, views_howto, views_blind
import os
urlpatterns = [
    path('inquiries', views.getInquiryPage, name='get-inquiry-page'),

    path('inquiries/get-post-list', views_post_list.getPostList, name='get-post-list'),
    
    path('inquiries/add-category', views_category.addInquiryCategory, name='inquiries-add-category'),

    path('inquiries/write-question', views.writeInquiryPost, name='inquiries-write-question'),
    path('inquiries/write-comment', views.writeInquiryComment, name='inquiries-write-comment'),
    path('inquiries/write-reply', views.writeInquiryReply, name='inquiries-write-reply'),
    path('inquiries/delete-post', views.deleteInquiryPost, name='inquiries-delete-post'),
    path('inquiries/delete-comment', views.deleteInquiryComment, name='inquiries-delete-comment'),
    path('inquiries/cancel-best-comment', views.cancelBestComment, name='cancel-best-comment'),
    path('inquiries/check-best-comment', views.checkBestComment, name='check-best-comment'),
    path('inquiries/select-best-comment', views.selectBestComment, name='select-best-comment'),

    path('inquiries/modify-question', views_modify.modifyInquiryPost, name='inquiries-modify-question'),
    path('inquiries/modify-comment', views_modify.modifyInquiryComment, name='inquiries-modify-comment'),

    path('inquiries/how-to-use', views_howto.inquiryHowToUse, name='inquiries-how-to-use'),
    path('inquiries/add-how-to-use', views_howto.inquiryAddHowToUse),
    path('inquiries/modify-how-to-use', views_howto.inquiryModifyHowToUse),
    path('inquiries/delete-how-to-use', views_howto.inquiryDeleteHowToUse),
    path('inquiries/reset-how-to-use', views_howto.resetInquiryHowToUse),
    path('inquiries/sort-how-to-use', views_howto.sortInquiryHowToUse),

    path('blind', views_blind.getInquiryPage, name='get-blind-page'),
    path('blind/get-post-list', views_blind.getPostList, name='blind-get-post-list'),
    path('blind/write-question', views_blind.writeInquiryPost, name='blind-write-question'),
    path('blind/write-comment', views_blind.writeInquiryComment, name='blind-write-comment'),
    path('blind/write-reply', views_blind.writeInquiryReply, name='blind-write-reply'),
    path('blind/delete-post', views_blind.deleteInquiryPost, name='blind-delete-post'),
    path('blind/delete-comment', views_blind.deleteInquiryComment, name='blind-delete-comment'),
    path('blind/cancel-best-comment', views_blind.cancelBestComment, name='blind-cancel-best-comment'),
    path('blind/check-best-comment', views_blind.checkBestComment, name='blind-check-best-comment'),
    path('blind/select-best-comment', views_blind.selectBestComment, name='blind-select-best-comment'),

    path('blind/modify-question', views_blind.modifyInquiryPost, name='inquiries-modify-question'),
    path('blind/modify-comment', views_blind.modifyInquiryComment, name='inquiries-modify-comment'),

]
settings.STATICFILES_DIRS.append(os.path.join(settings.BASE_DIR, 'inquiry', 'static'))
