from functools import wraps
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages

def admin_only(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_staff:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Only administrators can perform this action.'
                })
            return render(request, 'unauthorized.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
