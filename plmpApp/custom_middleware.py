from rest_framework.response import Response
from django.http import JsonResponse
from .global_service import DatabaseModel
from .models import ignore_calls
from plmp_backend.env import SIMPLE_JWT

def check_ignore_authentication_for_url(request):
    path = request.path.split("/")
    try:
        action = path[2] 
    except IndexError:
        return False 
    print(action)
    result_obj = DatabaseModel.get_document(ignore_calls.objects, {"name": action})
    return result_obj is not None  

def skip_for_paths():
    """
    Decorator for skipping middleware based on path
    """
    def decorator(f):
        def check_if_health(self, request):
            if check_ignore_authentication_for_url(request): 
                return self.get_response(request)  
            return f(self, request) 
        return check_if_health
    return decorator

def createJsonResponse1(message='success', status=True, data=None):
    """Create a JSON response with a message, status, and additional data."""
    response_data = {
        'data': data,
            'message': message,
            'status': status
    }
    return JsonResponse(response_data, content_type='application/json', status=200)
def createJsonResponse(request, token = None):
    c1 = ''
    if token:
        header,payload1,signature = str(token).split(".")
        c1 = header+'.'+payload1
    else:
        data_map = dict()
        data_map['data'] = dict()
        response = Response(content_type = 'application/json') 
        response.data = data_map
        response.data['emessage'] = 'success'
        response.data['estatus'] = True
        # response.data['_c1'] = c1
        response.status_code = 200
        return response
        c1=request.COOKIES.get('_c1')
    data_map = dict()
    data_map['data'] = dict()
    response = Response(content_type = 'application/json') 
    response.data = data_map
    response.data['emessage'] = 'success'
    response.data['estatus'] = True
    response.data['_c1'] = c1
    response.status_code = 200
    return response

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @skip_for_paths()
    def __call__(self, request):
        res = self.get_response(request) 
        if isinstance(res, JsonResponse):
            return res
        
        # return createJsonResponse(res)
        if isinstance(res, dict):
            return createJsonResponse1(data=res)
        elif isinstance(res, str):
            return createJsonResponse1(message=res)
        elif isinstance(res, list):
            return createJsonResponse1(data=res)
        else:
            return createJsonResponse1(message='Unexpected response type', status=False)



def createCookies(token,response):
    header,payload,signature = str(token).split(".")
    response.set_cookie(
        key = "_c1",
        value = header+"."+payload,
        max_age = SIMPLE_JWT['SESSION_COOKIE_MAX_AGE'],
        secure = SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly = False,
        samesite = SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        domain = SIMPLE_JWT['SESSION_COOKIE_DOMAIN'],
    )
    response.set_cookie(
        key = "_c2",
        value = signature,
        expires = SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure = SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly = True,
        samesite = SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
        domain = SIMPLE_JWT['SESSION_COOKIE_DOMAIN'],
    )