from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Permission
from .models import *



def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_active:
            return redirect('account')
            
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        

    return wrapper_function

def staff_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('notFound')

    return wrapper_function