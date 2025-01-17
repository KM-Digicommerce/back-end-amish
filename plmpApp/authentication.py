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
        if user_data_obj.role == 'super-admin':
            # _thread_locals.login_client_id = str("super-admin")
            client_id = ""
        else:
            # _thread_locals.login_client_id = str(user_data_obj.client_id.id)
            client_id = str(user_data_obj.client_id.id)
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
        user_data_obj.is_active = True
        # user_data_obj.save()
        response = createJsonResponse(request, token)
        createCookies(token, response)
        response.data['data']['user_login_id'] = str(user_data_obj.id)
        response.data['data']['user_role'] = str(user_data_obj.role)
        response.data['data']['client_id'] = str(client_id)
        csrf.get_token(request)
    response.data['data']['valid'] = valid
    return response


@api_view(('GET', 'POST'))
def logout(request):
    response = createJsonResponse(request)
    response.data['data']['status'] = 'logged out'
    return response


import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import email_otp 

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))  

@csrf_exempt
def sendOtp(request):
    json_req = JSONParser().parse(request)
    data = dict()
    data['status'] = False
    email = json_req.get('email')
    if not email:
        return  data
    otp = generate_otp()
    email_otp_obj = DatabaseModel.get_document(email_otp.objects,{'email':email})
    if email_otp_obj:
        DatabaseModel.delete_documents(email_otp.objects,{'email':email})
    otp_record = email_otp.objects.create(
        email=email,
        otp=otp,
        expires_at=datetime.now() + timedelta(minutes=5)
    )
    send_mail(
        'Your OTP for password reset',
        f'Your OTP is: {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    data['status'] = True
    return JsonResponse(data,safe=False)

@csrf_exempt

def resetPassword(request):
    json_req = JSONParser().parse(request)
    otp = json_req.get('otp')
    email = json_req.get('email')
    new_password = json_req.get('newPassword')
    otp_record = DatabaseModel.get_document(email_otp.objects,{'email':email,'otp':otp})
    if otp_record:
        if datetime.now() > otp_record.expires_at:
            return JsonResponse({'error': 'OTP has expired'},safe=True)
        otp_record.delete()
        DatabaseModel.update_documents(user.objects,{'email':email},{'password':new_password})
        return JsonResponse({'success': 'Password updated successfully'}, safe=True)
    return JsonResponse({'error': 'Invalid OTP'},safe=True)