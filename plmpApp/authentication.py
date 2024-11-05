from .custom_middleware import createJsonResponse
from .custom_middleware import createCookies
from rest_framework.parsers import JSONParser
from .global_service import DatabaseModel
from plmp_backend.env import SIMPLE_JWT
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.middleware import csrf
from .models import user

from rest_framework.parsers import JSONParser
import jwt
from rest_framework.decorators import api_view

@api_view(('GET', 'POST'))
@csrf_exempt
def loginUser(request):
    jsonRequest = JSONParser().parse(request)
    user_data_obj = DatabaseModel.get_document(user.objects, jsonRequest)
    token = ''
    if user_data_obj == None:
        response = createJsonResponse(request)
        valid = False
    else:
        role_name = user_data_obj.role
        payload = {
            'id': str(user_data_obj.id),
            'first_name': user_data_obj.name,
            'email': user_data_obj.email,
            'role_name': role_name.lower().replace(' ', '_'),
            'max_age': SIMPLE_JWT['SESSION_COOKIE_MAX_AGE']
        }
        token = jwt.encode(payload=payload, key=SIMPLE_JWT['SIGNING_KEY'], algorithm=SIMPLE_JWT['ALGORITHM'])
        # token = token.decode('utf-8')
        valid = True
        response = createJsonResponse(request, token)
        createCookies(token, response)
        csrf.get_token(request)
    response.data['data']['valid'] = valid
    return response


@api_view(('GET', 'POST'))
def logout(request):
    response = createJsonResponse(request)
    response.data['data']['status'] = 'logged out'
    return response