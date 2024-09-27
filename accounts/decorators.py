from django.shortcuts import redirect


def auth_check(fun):
    def wrapper(request, *args, **kwargs):

        if not request.user.id:
            return fun(request, *args, **kwargs)
        else:
            return redirect('/')
    return wrapper