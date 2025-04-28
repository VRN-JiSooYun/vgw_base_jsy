from django.urls import path, include
from re_auth.views import *

urlpatterns = [
    # page
    path('auth-view', view_page, name='re-auth-home'),

    # api
    path('getAuth', get_auth, name='get-auth'),
    path('getTargets', get_targets, name='get-targets'),
    path('updateAuth', update_auth, name='get-auth'),
]

