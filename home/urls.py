from django.urls import path, include
from home.views import *

urlpatterns = [
    # path('', home_view, name='home'),
    path('', re_home_view, name='home'),

    # code
    path('getCodes', get_codes, name='re-get-codes'),
    path('getCodeDtls', get_code_dtls, name='re-get-code-dtls'),
]
