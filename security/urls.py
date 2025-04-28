from django.urls import path, include
from security.views import *


urlpatterns = [
    # path('login/', login_form_sms),
    path('login/', login_form_default),
]
