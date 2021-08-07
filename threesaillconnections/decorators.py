from django.shortcuts import redirect


def addillcon_authentication(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.filter(name='salesperson').exists() or request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')

    return wrapper_func
