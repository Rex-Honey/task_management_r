from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from authentication.models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from drf_yasg import openapi


api_body = {
    'user_type': openapi.Schema(type=openapi.TYPE_STRING, example="Manager"),
    'mobile': openapi.Schema(type=openapi.TYPE_STRING, example="9876543210"),
    'first_name': openapi.Schema(type=openapi.TYPE_STRING, example="Jass"),
    'last_name': openapi.Schema(type=openapi.TYPE_STRING, example="Singh"),
    'username': openapi.Schema(type=openapi.TYPE_STRING, example="user3"),
}
response_schema_dict = {
        201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Success'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='User Registered successfully'),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    ),
}
@csrf_exempt
@swagger_auto_schema(tags=["Authentication"], operation_description="POST API to create user", operation_id="Create User", method='post', request_body=openapi.Schema(type=openapi.TYPE_OBJECT,properties=api_body),responses=response_schema_dict)
@api_view(['POST'])
def Create_user(request):
    try:
        if request.method!='POST':
            response = {'status':'Error','message': 'invalid method', 'data': {}}
            return JsonResponse(response, safe=False)
        
        response_data = json.loads(request.body.decode('utf-8'), strict=False)

        if len(response_data) > 5:
            response = {'status':'Error','message': 'Invalid request parameter length', 'data': {}}
            return JsonResponse(response, safe=False)

        for x in ('user_type','mobile','first_name','last_name','username'):
            if x not in response_data:
                response = {'status':'Error','message': "Parameter '"+x+"' missing", 'data': {}}
                return JsonResponse(response, safe=False)

            if not response_data[x]:
                response = {'status':'Error','message': "Value is missing for parameter '"+x+"'", 'data': {}}
                return JsonResponse(response, safe=False)
            
            if "str" not in str(type(response_data[x])):
                response = {'status':'Error','message': "invalid value type for '"+x+"' as only string is accepted", 'data': {}}
                return JsonResponse(response, safe=False)
            
        username=response_data['username']
        if CustomUser.objects.filter(username=username).exists():
            response = {'status':'Error','message': 'Username already exist', 'data': {}}
            return JsonResponse(response, safe=False)
        f_name=response_data['first_name']
        l_name=response_data['last_name']
        mobile=response_data['mobile']
        user_type=response_data['user_type']
        if user_type not in ('Manager','Developer'):
            response = {'status':'Error','message': 'Invalid user_type value, Valid are Manager or Developer', 'data': {}}
            return JsonResponse(response, safe=False)
        CustomUser.objects.create(username=username,user_type=user_type,first_name=f_name,last_name=l_name,mobile=mobile)
        response = {'status':'Success','message': "User Registered successfully", 'data': {}}
        return JsonResponse(response)        
    except Exception as ex:
        response = {'status':'Error','message': str(ex), 'data': {}}
        return JsonResponse(response)