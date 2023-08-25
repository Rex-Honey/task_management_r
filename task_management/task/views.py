from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from authentication.models import *
from task.models import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view

api_body = {
    'task_title': openapi.Schema(type=openapi.TYPE_STRING, example="Test task3"),
    'task_description': openapi.Schema(type=openapi.TYPE_STRING, example="This is description3"),
    'assignee_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=8),
    'created_by_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=9),
}
response_schema_dict = {
        201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Success'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Task created successfully'),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    ),
}
@csrf_exempt
@swagger_auto_schema(tags=["Task"], operation_description="POST API to create task", operation_id="Create Task", method='post', request_body=openapi.Schema(type=openapi.TYPE_OBJECT,properties=api_body),responses=response_schema_dict)
@api_view(['POST'])
def Create_task(request):
    try:
        if request.method!='POST':
            response = {'status':'Error','message': 'invalid method', 'data': {}}
            return JsonResponse(response, safe=False)
        
        response_data = json.loads(request.body.decode('utf-8'), strict=False)

        if len(response_data) > 4:
            response = {'status':'Error','message': 'Invalid request parameter length', 'data': {}}
            return JsonResponse(response, safe=False)

        for x in ('created_by_id','assignee_id','task_title','task_description'):
            if x not in response_data:
                response = {'status':'Error','message': "Parameter '"+x+"' missing", 'data': {}}
                return JsonResponse(response, safe=False)

            if not response_data[x]:
                response = {'status':'Error','message': "Value is missing for parameter '"+x+"'", 'data': {}}
                return JsonResponse(response, safe=False)
            
        for x in ('task_title','task_description'):
            if "str" not in str(type(response_data[x])):
                response = {'status':'Error','message': "invalid value type for '"+x+"' as only string is accepted", 'data': {}}
                return JsonResponse(response, safe=False)
            
        for x in ('created_by_id','assignee_id'):
            if "int" not in str(type(response_data[x])) or response_data[x] < 1:
                response = {'status':'Error', 'message': "invalid value for '"+x+"' as only positive integer value is accepted", 'data': ''}
                return JsonResponse(response, safe=False)
            
        created_by_id=response_data['created_by_id']
        assignee_id=response_data['assignee_id']
        task_title=response_data['task_title']
        task_description=response_data['task_description']
        
        created_by=CustomUser.objects.filter(id=created_by_id).first()
        if created_by.user_type=="Developer":
            response = {'status':'Error','message': "Invalid created_by_id, Developer can't create task", 'data': {}}
            return JsonResponse(response)            
        assignee=CustomUser.objects.filter(id=assignee_id).first()
        if assignee.user_type!="Developer":
            response = {'status':'Error','message': "Invalid assignee_id, Task can only assign to developer", 'data': {}}
            return JsonResponse(response)
        Task_data.objects.create(task_title=task_title,task_description=task_description,assignee=assignee,created_by=created_by)
        response = {'status':'Success','message': "Task created successfully", 'data': {}}
        return JsonResponse(response)        
    except Exception as ex:
        response = {'status':'Error','message': str(ex), 'data': {}}
        return JsonResponse(response)

api_body = {
    'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=10),
    'modified_by_id': openapi.Schema(type=openapi.TYPE_INTEGER, example=8),
    'status': openapi.Schema(type=openapi.TYPE_STRING, example="Done"),
}
response_schema_dict = {
        201: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Success'),
            'message': openapi.Schema(type=openapi.TYPE_STRING, description='Task updated successfully'),
            'data': openapi.Schema(type=openapi.TYPE_OBJECT),
        }
    ),
}
@csrf_exempt
@swagger_auto_schema(tags=["Task"], operation_description="POST API to update task", operation_id="Update Task", method='post', request_body=openapi.Schema(type=openapi.TYPE_OBJECT,properties=api_body),responses=response_schema_dict)
@api_view(['POST'])
def Update_task(request):
    try:
        if request.method!='POST':
            response = {'status':'Error','message': 'invalid method', 'data': {}}
            return JsonResponse(response, safe=False)
        
        response_data = json.loads(request.body.decode('utf-8'), strict=False)

        if len(response_data) > 3:
            response = {'status':'Error','message': 'Invalid request parameter length', 'data': {}}
            return JsonResponse(response, safe=False)

        for x in ('task_id','modified_by_id','status'):
            if x not in response_data:
                response = {'status':'Error','message': "Parameter '"+x+"' missing", 'data': {}}
                return JsonResponse(response, safe=False)

            if not response_data[x]:
                response = {'status':'Error','message': "Value is missing for parameter '"+x+"'", 'data': {}}
                return JsonResponse(response, safe=False)
            
        if "str" not in str(type(response_data['status'])):
            response = {'status':'Error','message': "invalid value type for 'status' as only string is accepted", 'data': {}}
            return JsonResponse(response, safe=False)
            
        for x in ('task_id','modified_by_id'):
            if "int" not in str(type(response_data[x])) or response_data[x] < 1:
                response = {'status':'Error', 'message': "invalid value for '"+x+"' as only positive integer value is accepted", 'data': ''}
                return JsonResponse(response, safe=False)

        task_id=response_data['task_id']
        status=response_data['status']
        modified_by_id=response_data['modified_by_id']

        if Task_data.objects.filter(id=task_id).exists():
            task_obj=Task_data.objects.filter(id=task_id).first()
        else:
            response = {'status':'Error','message': 'invalid task_id', 'data': {}}
            return JsonResponse(response, safe=False)    

        if CustomUser.objects.filter(id=modified_by_id).exists():
            modified_by=CustomUser.objects.filter(id=modified_by_id).first()
        else:
            response = {'status':'Error','message': 'invalid modify_by_id as id does not exist', 'data': {}}
            return JsonResponse(response, safe=False)
        
        if status not in ('ToDo','In progress', 'Done'):
            response = {'status':'Error','message': 'Invalid status value as valid types are ToDo, In progress, Done', 'data': {}}
            return JsonResponse(response, safe=False)
        
        task_obj.modified_by=modified_by
        task_obj.status=status
        task_obj.save()

        response = {'status':'Success','message': "Task updated successfully", 'data': {}}
        return JsonResponse(response)        
    except Exception as ex:
        response = {'status':'Error','message': str(ex), 'data': {}}
        return JsonResponse(response)