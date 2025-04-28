from django import template
from django.db.models import *
from hr.models import *
from django.contrib.auth.models import User
from hr.functions import initiate_authority_for_superuser

register = template.Library()

@register.filter(name='authMenu')
def authMenu(value, req):
    if req.user.id != None :
        returnVal = False
        p = False
        r = False
        v = False
        d = False
        authInfo = initiate_authority_for_superuser(req)
        value_p = "auth_"+value
        value_r = "auth_"+value+"_register"
        value_v = "auth_"+value+"_validation"
        value_d = "auth_"+value+"_design"
        auth_p = authInfo._meta.get_field(value_p)
        auth_p_value = auth_p.value_from_object(authInfo)
        if auth_p_value is not None :
            if req.user.member.id in auth_p_value :
                p = True
        else :
            p = False
        auth_r = authInfo._meta.get_field(value_r)
        auth_r_value = auth_r.value_from_object(authInfo)
        if auth_r_value is not None :
            if req.user.member.id in auth_r_value :
                r = True
        else :
            r = False
        auth_v = authInfo._meta.get_field(value_v)
        auth_v_value = auth_v.value_from_object(authInfo)
        if auth_v_value is not None :
            if req.user.member.id in auth_v_value :
                v = True
        else :
            v = False
        auth_d = authInfo._meta.get_field(value_d)
        auth_d_value = auth_d.value_from_object(authInfo)
        if auth_d_value is not None :
            if req.user.member.id in auth_d_value :
                d = True
        else :
            d = False

        if p or r or v or d :
            returnVal = True

        if req.user.is_superuser :
            # p = True
            # r = True
            # d = True
            # v = True
            returnVal = True

        return returnVal
    else :
        return False

@register.filter(name='authSubMenu')
def authSubMenu(value, req):
    if req.user.id != None :
        returnVal = False
        p = False
        r = False
        v = False
        d = False
        authInfo = initiate_authority_for_superuser(req)
        value_p = "auth_"+value
        value_r = "auth_"+value+"_register"
        value_v = "auth_"+value+"_validation"
        value_d = "auth_"+value+"_design"

        auth_p = authInfo._meta.get_field(value_p)
        auth_p_value = auth_p.value_from_object(authInfo)
        if auth_p_value is not None :
            if req.user.member.id in auth_p_value :
                p = True
        else :
            p = False

        auth_r = authInfo._meta.get_field(value_r)
        auth_r_value = auth_r.value_from_object(authInfo)        
        if auth_r_value is not None :
            if req.user.member.id in auth_r_value :
                r = True
        else :
            r = False

        auth_v = authInfo._meta.get_field(value_v)
        auth_v_value = auth_v.value_from_object(authInfo)
        if auth_v_value is not None :
            if req.user.member.id in auth_v_value :
                v = True
        else :
            v = False

        auth_d = authInfo._meta.get_field(value_d)
        auth_d_value = auth_d.value_from_object(authInfo)
        if auth_d_value is not None :
            if req.user.member.id in auth_d_value :
                d = True
        else :
            d = False

        if p or r or v or d :
            returnVal = p, r, v, d, False

        if req.user.is_superuser :
            returnVal = True, True, True, True, True

        return returnVal
    else :
        return False, False, False, False, False
