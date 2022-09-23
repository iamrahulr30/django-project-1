from django.http import HttpResponse


def sellerpages(view_func):
    def wrapperfunc(request,*args,**kwargs):
        if request.user.is_anonymous:
            return HttpResponse("you are anonymous,login to access this page")
        elif  request.user.is_seller:
            return view_func(request, *args, **kwargs)
        else :
            return HttpResponse("you are not a seller,update your account to seller to access this page")
    
    
    return wrapperfunc