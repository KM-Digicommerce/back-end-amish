from rest_framework.response import Response
from django.http import JsonResponse
from .global_service import DatabaseModel
from .models import ignore_calls

def check_ignore_authentication_for_url(request):
    path = request.path.split("/")
    try:
        action = path[2] 
    except IndexError:
        return False 

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

def createJsonResponse(message='success', status=True, data=None):
    """Create a JSON response with a message, status, and additional data."""
    response_data = {
        'data': data,
            'message': message,
            'status': status
        
    }
    return JsonResponse(response_data, content_type='application/json', status=200)

class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @skip_for_paths()
    def __call__(self, request):
        res = self.get_response(request) 
        if isinstance(res, JsonResponse):
            return res

        if isinstance(res, dict):
            return createJsonResponse(data=res)
        elif isinstance(res, str):
            return createJsonResponse(message=res)
        elif isinstance(res, list):
            return createJsonResponse(data=res)
        else:
            return createJsonResponse(message='Unexpected response type', status=False)
