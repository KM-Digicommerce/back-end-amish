from django.http import JsonResponse
from .models import products
from .models import varient_option
from .models import category
from .models import level_one_category
from .models import level_two_category
from .models import level_three_category
from .models import level_four_category
from .models import level_five_category
from .models import product_category_config
from .models import product_varient_option
from .models import product_varient
from .models import category_log
from .models import product_log
from .models import product_varient_log
from .models import category_varient_option_log
from .models import category_varient
from .models import user
from .models import type_name
from .models import type_value
from .models import price_log
from .models import xl_mapping
from .models import brand
from .models import client
from .models import brand_category_price
from .models import radial_price_log
from .models import revert_varient_retail_price

from plmp_backend.env import MONGODB_COURSE_DB_NAME
from django.http import HttpResponse
from openpyxl import Workbook
import pandas as pd
from io import BytesIO
from rest_framework.parsers import JSONParser
import json
from .global_service import DatabaseModel
from bson import ObjectId
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO
import pandas as pd
import pdfplumber
import math
import shutil
from django.core.files.storage import FileSystemStorage
import os
import re
from .view_utils import getCategoryLevelOrder
from django.views.decorators.csrf import csrf_exempt
from django.core.management.utils import get_random_secret_key
from pytz import timezone
from django.utils.timezone import is_naive, make_aware
from .custom_middleware import get_current_user,get_current_client
def v1(request):
    print(get_random_secret_key())
    return JsonResponse({"PLMP_API":"v2"},safe=False)
def create_user(request):
    json_request = json.loads(request.body)
    categories_data = json_request.get('categories')

    for category_data in categories_data:
        name = category_data.get('name')
        if name:
            category_obj = category(name=name,section_list = [])
            category_obj.save()
    return JsonResponse({'status': 'User created'})


@csrf_exempt
def createCategory(request):
    client_id = get_current_client()
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    category_obj = DatabaseModel.get_document(category.objects,{'name':name,'client_id':ObjectId(client_id)})
    data = dict()
    if category_obj :
        data['is_created'] = False
        data['error'] = "Category Already Exists In Our Database"
        return data
    else:
        category_obj = DatabaseModel.save_documents(category,{'name':name})
    logForCategory(category_obj.id,"create",user_login_id,'level-1')
    data['is_created'] = True
    return data


@csrf_exempt
def createCategory1(request):
    client_id = get_current_client()
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    category_id = json_req.get("category_id")
    level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'name':name,'client_id':ObjectId(client_id)})
    data = dict()
    if level_one_category_obj :
        category_obj = DatabaseModel.get_document(category.objects,{'level_one_category_list__in':level_one_category_obj.id})
        if category_obj:
            data['is_created'] = False
            data['error'] = "Category Already Exists In Our Database"
            return data
    else:
        level_one_category_obj = DatabaseModel.save_documents(level_one_category,{'name':name})
    DatabaseModel.update_documents(category.objects,{"id":category_id},{'add_to_set__level_one_category_list':level_one_category_obj.id})
    logForCategory(level_one_category_obj.id,"create",user_login_id,'level-2')
    data['is_created'] = True
    return data


@csrf_exempt
def createCategory2(request):
    client_id = get_current_client()
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    category_id = json_req.get("category_id")
    level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'name':name,'client_id':ObjectId(client_id)})
    data = dict()
    if level_two_category_obj :
        category_obj = DatabaseModel.get_document(category.objects,{'level_two_category_list__in':level_two_category_obj.id})
        if category_obj:
            data['is_created'] = False
            data['error'] = "Category Already Exists In Our Database"
            return data
    else:
        level_two_category_obj = DatabaseModel.save_documents(level_two_category,{'name':name})
    DatabaseModel.update_documents(level_one_category.objects,{"id":category_id},{'add_to_set__level_two_category_list':level_two_category_obj.id})
    logForCategory(level_two_category_obj.id,"create",user_login_id,'level-3')
    data['is_created'] = True
    return data


@csrf_exempt
def createCategory3(request):
    client_id = get_current_client()
    
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    section_id = json_req.get("category_id")
    level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'name':name,'client_id':ObjectId(client_id)})
    data = dict()
    if level_three_category_obj :
        category_obj = DatabaseModel.get_document(category.objects,{'level_three_category_list__in':level_three_category_obj.id})
        if category_obj:
            data['is_created'] = False
            data['error'] = "Category Already Exists In Our Database"
            return data
    else:
        level_three_category_obj = DatabaseModel.save_documents(level_three_category,{'name':name})
    DatabaseModel.update_documents(level_two_category.objects,{"id":section_id},{'add_to_set__level_three_category_list':level_three_category_obj.id})
    logForCategory(level_three_category_obj.id,"create",user_login_id,'level-4')
    data['is_created'] = True
    return data


@csrf_exempt
def createCategory4(request):
    client_id = get_current_client()
    
    json_req = JSONParser().parse(request)
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    name = json_req.get("name").title()
    section_id = json_req.get("category_id")
    level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'name':name,'client_id':ObjectId(client_id)})
    data = dict()
    if level_four_category_obj :
        category_obj = DatabaseModel.get_document(category.objects,{'level_four_category_list__in':level_four_category_obj.id})
        if category_obj:
            data['is_created'] = False
            data['error'] = "Category Already Exists In Our Database"
            return data
    else:
        level_four_category_obj = DatabaseModel.save_documents(level_four_category,{'name':name})
    DatabaseModel.update_documents(level_three_category.objects,{"id":section_id},{'add_to_set__level_four_category_list':level_four_category_obj.id})
    logForCategory(level_four_category_obj.id,"create",user_login_id,'level-5')
    data['is_created'] = True
    return data


@csrf_exempt
def createCategory5(request):
    client_id = get_current_client()
    
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    section_id = json_req.get("category_id")
    level_five_category_obj = DatabaseModel.get_document(level_five_category.objects,{'name':name,'client_id':ObjectId(client_id)})
    data = dict()
    if level_five_category_obj :
        category_obj = DatabaseModel.get_document(category.objects,{'level_five_category_list__in':level_five_category_obj.id})
        if category_obj:
            data['is_created'] = False
            data['error'] = "Category Already Exists In Our Database"
            return data
    else:
        level_five_category_obj = DatabaseModel.save_documents(level_five_category,{'name':name})
    DatabaseModel.update_documents(level_four_category.objects,{"id":section_id},{'add_to_set__level_five_category_list':level_five_category_obj.id})
    logForCategory(level_five_category_obj.id,"create",user_login_id,'level-6')
    data = dict()
    data['is_created'] = True
    return data


@csrf_exempt
def createProduct(request):
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    client_id = get_current_client()
    
    product_obj = json_req.get("product_obj")
    category_id = product_obj["category_id"]
    category_name = product_obj["category_name"]
    products_obj = DatabaseModel.get_document(products.objects,{'model':product_obj['model'],'mpn':product_obj['mpn'],'client_id':client_id})
    if products_obj:
        data = dict()
        data['status'] = False
        data['error'] = "Product Already Created"
        return data
    product_obj_save = {
        "model" :product_obj['model'],
        "upc_ean" :product_obj['upc_ean'],
        "mpn" :product_obj['mpn'],     
        "breadcrumb":product_obj['breadcrumb'],
        "brand_id":ObjectId(product_obj['brand_id']),
        "product_name":product_obj['product_name'],
        "long_description":product_obj['long_description'],
        "short_description":product_obj['short_description'],
        "features":product_obj['features'],
        "attributes":product_obj['attributes'],
        "tags":product_obj['tags'],
        # "msrp":str(product_obj['msrp']),
        # "base_price":str(product_obj['base_price']),
        "key_features":product_obj['key_features']
    }
    products_obj_1 = DatabaseModel.save_documents(products,product_obj_save)
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':ObjectId(category_id),'brand_id':ObjectId(products_obj_1.brand_id.id),'is_active':True})
    cat_retail_price = 1
    if brand_category_price_obj:
        cat_retail_price = brand_category_price_obj.price
    for z in product_obj['varients']:
        retail_price = str(z['retail_price']) 
        product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":z['sku_number'],"finished_price":str(z['finished_price']),"un_finished_price":str(z['un_finished_price']),"quantity":z['quantity'],'retail_price':retail_price})
        createradial_price_log(product_varient_obj.id,"0",retail_price,user_login_id,client_id)
        logForCreateProductVarient(product_varient_obj.id,user_login_id,"create")
        for i in z['options']:
            product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":i['option_name_id'],"option_value_id":i['option_value_id']})
            DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
        DatabaseModel.update_documents(products.objects,{"id":products_obj_1.id},{"add_to_set__options":product_varient_obj.id})
    products_obj = DatabaseModel.save_documents(product_category_config,{'product_id':products_obj_1.id,'category_level':category_name,"category_id":category_id})
    logForCreateProduct(products_obj_1.id,user_login_id,"create")
    data = dict()
    data['status'] = True
    return data


#delete
@csrf_exempt
def deleteCategory(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    category_name = json_req.get("category_name")
    data = dict()
    if category_name == "level-1":
        category_obj = DatabaseModel.get_document(category.objects,{'id':id})
        if len(category_obj.level_one_category_list)>0:
            data['error'] = "level two category is added so category cannot be deleted"
        else:
            product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'category_id':id})
            if product_category_config_obj:
                data['error'] = "product  is added so category cannot be deleted"
            else:
                DatabaseModel.delete_documents(category.objects,{'id':id})

    elif category_name == "level-2":
        category_id = json_req.get("category_id")
        category_obj = DatabaseModel.get_document(level_one_category.objects,{'id':id})
        if len(category_obj.level_two_category_list)>0:
            data['error'] = "level three category is added so category cannot be deleted"
        else:
            product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'category_id':id})
            if product_category_config_obj:
                data['error'] = "product  is added so category cannot be deleted"
            else:
                DatabaseModel.delete_documents(level_one_category.objects,{'id':id})
                DatabaseModel.update_documents(category.objects,{"id":category_id},{'pull__level_one_category_list':id})
    elif category_name == "level-3":
        category_id = json_req.get("category_id")
        category_obj = DatabaseModel.get_document(level_two_category.objects,{'id':id})
        if len(category_obj.level_three_category_list)>0:
            data['error'] = "level four category is added so category cannot be deleted"
        else:
            product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'category_id':id})
            if product_category_config_obj:
                data['error'] = "product  is added so category cannot be deleted"
            else:
                DatabaseModel.delete_documents(level_two_category.objects,{'id':id})
                DatabaseModel.update_documents(category.objects,{"id":category_id},{'pull__level_two_category_list':id})
    elif category_name == "level-4":
        category_id = json_req.get("category_id")
        category_obj = DatabaseModel.get_document(level_three_category.objects,{'id':id})
        if len(category_obj.level_four_category_list)>0:
            data['error'] = "level five category is added so category cannot be deleted"
        else:
            product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'category_id':id})
            if product_category_config_obj:
                data['error'] = "product  is added so category cannot be deleted"
            else:
                DatabaseModel.delete_documents(level_three_category.objects,{'id':id})
                DatabaseModel.update_documents(category.objects,{"id":category_id},{'pull__level_three_category_list':id})
    elif category_name == "level-5":
        category_id = json_req.get("category_id")
        category_obj = DatabaseModel.get_document(level_four_category.objects,{'id':id})
        if len(category_obj.level_five_category_list)>0:
            data['error'] = "level six category is added so category cannot be deleted"
        else:
            product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'category_id':id})
            if product_category_config_obj:
                data['error'] = "product  is added so category cannot be deleted"
            else:
                DatabaseModel.delete_documents(level_four_category.objects,{'id':id})
                DatabaseModel.update_documents(category.objects,{"id":category_id},{'pull__level_four_category_list':id})
    elif category_name == "level-6":
        category_id = json_req.get("category_id")
        product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'category_id':id})
        if product_category_config_obj:
            data['error'] = "product  is added so category cannot be deleted"
        else:
            DatabaseModel.delete_documents(level_five_category.objects,{'id':id})
            DatabaseModel.update_documents(category.objects,{"id":category_id},{'pull__level_five_category_list':id})
    data = dict()
    data['is_deleted'] = True
    return data


#update
@csrf_exempt
def updateCategory(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    name = json_req.get("name").title()
    category_name = json_req.get("category_name")
    if category_name == "level-1":
        DatabaseModel.update_documents(category.objects,{'id':id},{'name':name})
    elif category_name == "level-2":
        DatabaseModel.update_documents(level_one_category.objects,{'id':id},{'name':name})
    elif category_name == "level-3":
        DatabaseModel.update_documents(level_two_category.objects,{'id':id},{'name':name})
    elif category_name == "level-4":
        DatabaseModel.update_documents(level_three_category.objects,{'id':id},{'name':name})
    elif category_name == "level-5":
        DatabaseModel.update_documents(level_four_category.objects,{'id':id},{'name':name})
    elif category_name == "level-6":
        DatabaseModel.update_documents(level_five_category.objects,{'id':id},{'name':name})
    data = dict()
    data['is_updated'] = True
    return data


def convert_object_ids_to_strings(data):
    if isinstance(data, list):
        for item in data:
            convert_object_ids_to_strings(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if key == '_id' and isinstance(value, ObjectId):
                data[key] = str(value)
            else:
                convert_object_ids_to_strings(value)


def obtainCategoryAndSections(request):
    client_id = get_current_client()
    pipeline = [
         {
            '$match':{'client_id':ObjectId(client_id)}
        },
    {
        '$lookup': {
            'from': 'level_one_category',
            'localField': 'level_one_category_list',
            'foreignField': '_id',
            'as': 'level_one_category'
        }
    },
    {
        '$lookup': {
            'from': 'level_two_category',
            'localField': 'level_one_category.level_two_category_list',
            'foreignField': '_id',
            'as': 'level_two_category'
        }
    },
    {   
        '$lookup': {
            'from': 'level_three_category',
            'localField': 'level_two_category.level_three_category_list',
            'foreignField': '_id',
            'as': 'level_three_category'
        }
    },
    {
        '$lookup': {
            'from': 'level_four_category',
            'localField': 'level_three_category.level_four_category_list',
            'foreignField': '_id',
            'as': 'level_four_category'
        }
    },
    {
        '$lookup': {
            'from': 'level_five_category',
            'localField': 'level_four_category.level_five_category_list',
            'foreignField': '_id',
            'as': 'level_five_category'
        }
    }]
    flat_result = list(category.objects.aggregate(*pipeline))
    transformed_result = [] 
    for entry in flat_result:  
        category_entry = {
            "_id": entry['_id'],
            "name": entry['name'],
            "level_one_category_list": [] ,
            "level_one_category_count": 0
        }
        level_two_map = {level_two['_id']: level_two for level_two in entry.get('level_two_category', [])}
        for level_one in entry.get('level_one_category', []):
            level_one_entry = {
                "_id": level_one['_id'],
                "name": level_one['name'],
                "level_two_category_list": [] ,
                "level_two_category_count": 0 
            }
            for level_two_id in level_one.get('level_two_category_list', []):
                level_two = level_two_map.get(level_two_id)
                if level_two:
                    level_two_entry = {
                        "_id": level_two['_id'],
                        "name": level_two['name'],
                        "level_three_category_list": [],
                        "level_three_category_count": 0 
                    }
                    level_three_map = {level_three['_id']: level_three for level_three in entry.get('level_three_category', [])}
                    for level_three_id in level_two.get('level_three_category_list', []):
                        level_three = level_three_map.get(level_three_id)
                        if level_three:
                            level_three_entry = {
                                "_id": level_three['_id'],
                                "name": level_three['name'],
                                "level_four_category_list": [] ,
                                "level_four_category_count": 0 
                            }
                            level_four_map = {level_four['_id']: level_four for level_four in entry.get('level_four_category', [])}
                            for level_four_id in level_three.get('level_four_category_list', []):
                                level_four = level_four_map.get(level_four_id)
                                if level_four:
                                    level_four_entry = {
                                        "_id": level_four['_id'],
                                        "name": level_four['name'],
                                        "level_five_category_list": [] ,
                                        "level_five_category_count": 0 
                                    }
                                    level_five_map = {level_five['_id']: level_five for level_five in entry.get('level_five_category', [])}
                                    for level_five_id in level_four.get('level_five_category_list', []):
                                        level_five = level_five_map.get(level_five_id)
                                        if level_five:
                                            level_five_entry = {
                                                "_id": level_five['_id'],
                                                "name": level_five['name']
                                            }
                                            level_four_entry['level_five_category_list'].append(level_five_entry) 
                                    level_three_entry['level_four_category_list'].append(level_four_entry) 
                                    level_four_entry['level_five_category_count'] = len(level_four_entry['level_five_category_list'])
                            level_two_entry['level_three_category_list'].append(level_three_entry) 
                            level_three_entry['level_four_category_count'] = len(level_three_entry['level_four_category_list'])
                    level_one_entry['level_two_category_list'].append(level_two_entry) 
                    level_two_entry['level_three_category_count'] = len(level_two_entry['level_three_category_list'])
            category_entry['level_one_category_list'].append(level_one_entry) 
            level_one_entry['level_two_category_count'] = len(level_one_entry['level_two_category_list'])
        transformed_result.append(category_entry) 
        category_entry['level_one_category_count'] = len(category_entry['level_one_category_list'])
    result = sorted(transformed_result, key=lambda x: x['_id'])
    last_all_ids = []
    category_list = DatabaseModel.list_documents(category.objects)
    for category_obj in category_list:
        if len(category_obj.level_one_category_list)>0:
            for i in category_obj.level_one_category_list:
                if len(i.level_two_category_list)>0:
                    for j in i.level_two_category_list:
                        if len(j.level_three_category_list)>0:
                            for k in j.level_three_category_list:
                                if len(k.level_four_category_list)>0:
                                    for l in  k.level_four_category_list:
                                        if len(l.level_five_category_list)>0:
                                            for m in  l.level_five_category_list:
                                                last_all_ids.append({'id':str(m.id),'name':m.name})
                                        else:
                                            last_all_ids.append({'id':str(l.id),'name':l.name})
                                else:
                                    last_all_ids.append({'id':str(k.id),'name':k.name})
                        else:
                            last_all_ids.append({'id':str(j.id),'name':j.name})
                else:
                    last_all_ids.append({'id':str(i.id),'name':i.name})
        else:
            last_all_ids.append({'id':str(category_obj.id),'name':category_obj.name})
    data = dict()
    data['last_level_category'] = last_all_ids
    convert_object_ids_to_strings(result)  
    data['category_list'] = result
    data['category_count'] = len(result)
    return data


@csrf_exempt
def obtainAllProductList(request):
    # json_req = JSONParser().parse(request)
    client_id = get_current_client()
    print(client_id)
    category_id = request.GET.get("category_id")
    filter = request.GET.get("filter")
    if filter == "true" or filter == None:
        reverse_check = True
    else:
        reverse_check = False
    level_name = request.GET.get("level_name")
    if category_id:
        all_ids = []
        if level_name == "level-1":
            category_obj = DatabaseModel.get_document(category.objects,{'id':category_id,"client_id":client_id})
            if category_obj:
                all_ids.append(category_id)
                for i in category_obj.level_one_category_list:
                    all_ids.append(i.id)
                    for j in i.level_two_category_list:
                        all_ids.append(j.id)
                        for k in j.level_three_category_list:
                            all_ids.append(k.id)
                            for l in  k.level_four_category_list:
                                all_ids.append(l.id)
                                for m in  l.level_five_category_list:
                                    all_ids.append(m.id)
        elif  level_name == "level-2":
            level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'id':category_id})
            if level_one_category_obj:
                all_ids.append(level_one_category_obj.id)
                for j in level_one_category_obj.level_two_category_list:
                    all_ids.append(j.id)
                    for k in j.level_three_category_list:
                        all_ids.append(k.id)
                        for l in  k.level_four_category_list:
                            all_ids.append(l.id)
                            for m in  l.level_five_category_list:
                                all_ids.append(m.id)
        elif  level_name == "level-3":
            level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'id':category_id})
            if level_two_category_obj:
                all_ids.append(level_two_category_obj.id)
                for k in level_two_category_obj.level_three_category_list:
                    all_ids.append(k.id)
                    for l in  k.level_four_category_list:
                        all_ids.append(l.id)
                        for m in  l.level_five_category_list:
                            all_ids.append(m.id)
        elif  level_name == "level-4":
            level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'id':category_id})
            if level_three_category_obj:
                all_ids.append(level_three_category_obj.id)
                for l in  level_three_category_obj.level_four_category_list:
                    all_ids.append(l.id)
                    for m in  l.level_five_category_list:
                        all_ids.append(m.id)
        elif  level_name == "level-5":
            level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'id':category_id})
            if level_four_category_obj:
                all_ids.append(level_four_category_obj.id)
                for m in  level_four_category_obj.level_five_category_list:
                    all_ids.append(m.id)
        all_ids = [str(i) for i in all_ids]
        category_obj = {"category_id":{'$in':all_ids}}
    else:
        category_obj = {}
    pipeline = [
    {
            "$match":category_obj
        },
        {
        '$lookup': {
            'from': 'products',
            'localField': 'product_id',
            'foreignField': '_id',
            'as': 'products'
        }
    }, 
    {
            '$unwind': {
                'path': '$products',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        "$match":{'products.client_id':ObjectId(client_id)}
    },
    {
        '$lookup': {
            'from': 'brand',
            'localField': 'products.brand_id',
            'foreignField': '_id',
            'as': 'brand'
        }
    }, 
    {
            '$unwind': {
                'path': '$brand',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        '$group': {
            "_id":None,
            'product_list': {
                "$push": {
                    'product_name': "$products.product_name",
                    'product_id': "$products._id",
                    'model':"$products.model",
                    'upc_ean':"$products.upc_ean",
                    'breadcrumb':"$products.breadcrumb",
                    'brand':"$brand.name",
                    'product_name':"$products.product_name",
                    'long_description':"$products.long_description",
                    'short_description':"$products.short_description",
                    'features':"$products.features",
                    'attributes':"$products.attributes",
                    'tags':"$products.tags",
                    'msrp':"$products.msrp",
                    'mpn':"$products.mpn",
                    'base_price':"$products.base_price",
                    'key_features':"$products.key_features",
                    'image':"$products.image",
                    'level':'$category_level',
                    'category_id':'$category_id'
                }
            }
        }
    }
    ]
    result = list(product_category_config.objects.aggregate(*pipeline))
    data = dict()
    data['product_list'] = list()
    data['product_count'] = 0
    if len(result)>0:
        result = result[0]
        del result['_id']
        result['product_list']
        for j in result['product_list']:
            j['product_id'] = str(j['product_id']) if 'product_id'in j else ""
            getCategoryLevelOrder(j)
        data['product_list'] = result['product_list']
        data['product_count'] = len(result['product_list'])
        data['product_list'] = sorted(data['product_list'], key=lambda x: ObjectId(x['product_id']),reverse=reverse_check)
    return data


@csrf_exempt
def obtainProductDetails(request):
    json_req = JSONParser().parse(request)
    product_id = ObjectId(json_req['id'])
    pipeline = [
    {
            "$match":{'_id':product_id}
        }, {
        '$lookup': {
            'from': 'brand',
            'localField': 'brand_id',
            'foreignField': '_id',
            'as': 'brand'
        }
    }, 
    {
            '$unwind': {
                'path': '$brand',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        '$group': {
            "_id":None,
            'product_obj': {
                "$first": {
                    'product_name': "$product_name",
                    'product_id': "$_id",
                    'mpn': "$mpn",
                    'model':"$model",
                    'upc_ean':"$upc_ean",
                    'breadcrumb':"$breadcrumb",
                    'brand':"$brand.name",
                    'brand_id':"$brand._id",
                    'product_name':"$product_name",
                    'long_description':"$long_description",
                    'short_description':"$short_description",
                    'features':"$features",
                    'attributes':"$attributes",
                    'tags':"$tags",
                    'msrp':"$msrp",
                    'base_price':"$base_price",
                    'key_features':"$key_features",
                    'image':"$image",
                }
            }
        }
    }
    ]
    result = list(products.objects.aggregate(*pipeline))
    if len(result)>0:
        result = result[0]
        del result['_id']
        result['product_obj']['product_id'] = str(result['product_obj']['product_id'])
        result['product_obj']['brand_id'] = str(result['product_obj']['brand_id'])
        # result['product_obj']['ImageURL'] = result['product_obj']['ImageURL'][0] if len(result['product_obj']['ImageURL']) >0 else ""
        product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{"product_id":result['product_obj']['product_id']})
        result['category_id'] = product_category_config_obj.category_id
        result['category_name'] = product_category_config_obj.category_level
        i = dict()
        i['level'] = result['category_name']
        i['category_id'] = result['category_id']
        brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':i['category_id'],'brand_id':result['product_obj']['brand_id'],'is_active':True})
        result['category_brand_price'] = dict()
        if brand_category_price_obj:
            result['category_brand_price']['price'] = brand_category_price_obj.price
            result['category_brand_price']['price_option'] = brand_category_price_obj.price_option
        else:
            result['category_brand_price']['price'] = 0
            result['category_brand_price']['price_option'] = ""
        print(i)
        getCategoryLevelOrder(i)
        result['category_level'] = i['category_name']
    return  result


def productBulkUpdate(request):
    json_req = JSONParser().parse(request)
    product_obj_list = json_req['product_obj_list']
    for i in product_obj_list:
        DatabaseModel.update_documents(products.objects,{'id':i['id']},i['update_obj'])
    data = dict()
    data['is_updated'] = True
    return data


@csrf_exempt
def productUpdate(request):
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    product_id = json_req['id']
    json_req['update_obj']['brand_id'] = ObjectId(json_req['update_obj']['brand_id'])
    DatabaseModel.update_documents(products.objects,{'id':product_id},json_req['update_obj'])
    logForCreateProduct(product_id,user_login_id,"update")
    data = dict()
    data['is_updated'] = True
    return data


@csrf_exempt
def varientBulkUpdate(request):
    json_req = JSONParser().parse(request)
    varient_obj_list = json_req['varient_obj_list']
    for i in varient_obj_list:
        DatabaseModel.update_documents(product_varient.objects,{'id':i['id']},{'sku_number':i[""],"finished_price":i["finished_price"],"un_finished_price":i["un_finished_price"],"quantity":i["quantity"]})
    data = dict()
    data['is_updated'] = True
    return data


@csrf_exempt
def obtainAllVarientList(request):
    json_req = JSONParser().parse(request)
    product_id = ObjectId(json_req['product_id'])
    pipeline = [
    {
            "$match":{'_id':product_id}
        },
        {
            '$lookup': {
                "from": 'product_varient',
                "localField": 'options',
                "foreignField": "_id",
                "as": "product_varient_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            '$lookup': {
                "from": 'product_varient_option',
                "localField": 'product_varient_ins.varient_option_id',
                "foreignField": "_id",
                "as": "product_varient_option_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_option_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
        '$lookup': {
            'from': 'type_name',
            'localField': 'product_varient_option_ins.option_name_id',
            'foreignField': '_id',
            'as': 'type_name'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_name',
                'preserveNullAndEmptyArrays': True
            }
        },    {
        '$lookup': {
            'from': 'type_value',
            'localField': 'product_varient_option_ins.option_value_id',
            'foreignField': '_id',
            'as': 'type_value'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_value',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        '$group': {
            "_id":"$product_varient_ins._id",
            "sku_number": { "$first": "$product_varient_ins.sku_number" },
            "finished_price": { "$first": "$product_varient_ins.finished_price" },
            "un_finished_price": { "$first": "$product_varient_ins.un_finished_price" },
            "retail_price": { "$first": "$product_varient_ins.retail_price" },
            "quantity": { "$first": "$product_varient_ins.quantity" },
            "image_url": { "$first": "$product_varient_ins.image_url" },
            'varient_option_list': {
                "$push": {
                    'type_name': "$type_name.name",
                    'type_value': "$type_value.name",
                }
            }
        }
    }, {
            '$project': {
                "_id": 0,
                "sku_number":1,
                'retail_price':1,
            "finished_price":1,
            "un_finished_price":1,
            "quantity": 1,
            "image_url": 1,
            'varient_option_list':1
            }
        }
    ]
    result = list(products.objects.aggregate(*pipeline))
    return  result


@csrf_exempt
def exportAll(request):
    category_id = request.GET.get('category_id')
    client_id = get_current_client()
    if category_id:
        category_obj = {'product_category_config_ins.category_id':category_id,"client_id":ObjectId(client_id)}
    else:
        category_obj = {"client_id":ObjectId(client_id)}
    pipeline = [
        {
            '$lookup': {
                "from": 'product_varient',
                "localField": 'options',
                "foreignField": "_id",
                "as": "product_varient_ins"
            }
        },
        {'$unwind': {'path': '$product_varient_ins', 'preserveNullAndEmptyArrays': True}},
        {
            '$lookup': {
                "from": 'product_category_config',
                "localField": '_id',
                "foreignField": "product_id",
                "as": "product_category_config_ins"
            }
        },
        {'$unwind': {'path': '$product_category_config_ins', 'preserveNullAndEmptyArrays': True}},
        {
            "$match": category_obj
        },
        {
            '$lookup': {
                'from': 'product_varient_option',
                'localField': 'product_varient_ins.varient_option_id',
                'foreignField': '_id',
                'as': 'product_varient_option_ins'
            }
        },  
        {'$unwind': {'path': '$product_varient_option_ins', 'preserveNullAndEmptyArrays': True}},{
        '$lookup': {
            'from': 'product_varient_option',
            'localField': 'product_varient_ins.varient_option_id',
            'foreignField': '_id',
            'as': 'product_varient_option_ins'
        }
        },  {
            '$unwind': {
                'path': '$product_varient_option_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, {
        '$lookup': {
            'from': 'type_name',
            'localField': 'product_varient_option_ins.option_name_id',
            'foreignField': '_id',
            'as': 'type_name'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_name',
                'preserveNullAndEmptyArrays': True
            }
        },    {
        '$lookup': {
            'from': 'type_value',
            'localField': 'product_varient_option_ins.option_value_id',
            'foreignField': '_id',
            'as': 'type_value'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_value',
                'preserveNullAndEmptyArrays': True
            }
        }, {
        '$lookup': {
            'from': 'brand',
            'localField': 'brand_id',
            'foreignField': '_id',
            'as': 'brand'
        }
    }, 
    {
            '$unwind': {
                'path': '$brand',
                'preserveNullAndEmptyArrays': True
            }
        },{
            "$group": {
                "_id": "$product_varient_ins._id",
                "model":{ "$first":"$model"},
                "mpn":{ "$first":"$mpn"},
                "upc_ean":{ "$first":"$upc_ean"},
                "product_name":{ "$first":"$product_name"},
                "category level":{ "$first":"$product_category_config_ins.category_level"},
                "category_id":{ "$first":"$product_category_config_ins.category_id"},
                "long_description":{ "$first":"$long_description"},
                "short_description":{ "$first":"$short_description"}, 
                "brand":{ "$first":"$brand.name"},
                "breadcrumb":{ "$first":"$breadcrumb"},
                # "msrp":{ "$first":"$msrp"},
                "retail_price":{ "$first":"$product_varient_ins.retail_price"},
                "Tags":{ "$first":"$tags"}, 
                "Variant SKU":{ "$first":"$product_varient_ins.sku_number"},
                "Un Finished Price":{ "$first":"$product_varient_ins.un_finished_price"},
                "Finished Price":{ "$first":"$product_varient_ins.finished_price"},
                "Image Src":{ "$first":"$image"},
                "Key Features":{ "$first":"$key_features"},
                "stockv":{ "$first":"$product_varient_ins.quantity"},
                "varient_option_list":{'$addToSet':{'name':"$type_name.name","value":"$type_value.name"}}
        }
    } , {
            '$project': {
                "_id": 0,
                "model":1,
                "upc_ean":1,
                "category level":1,
                "category_id":1,
                "product_name":1,
                "long_description":1,
                "short_description":1, 
                "brand":1,
                "breadcrumb":1,
                # "msrp":1,
                "retail_price":1,
                "Tags":1, 
                "Variant SKU":1,
                "Un Finished Price":1,
                "Finished Price":1,
                "Image Src":1, 
                "Image Position":1,
                "Key Features":1,
                "stockv":1,
                "varient_option_list":1,
                'mpn':1,
            }
        }
    
    ]
    result = list(products.objects.aggregate(*pipeline))
    print(result)
    max_variants = 0
    max_image = 0
    
    for i in result:
        if max_variants < len(i['varient_option_list']):
            max_variants = len(i['varient_option_list'])
        if i['Image Src'] != None:
            if max_image < len(i['Image Src']):
                max_image = len(i['Image Src'])
    print()
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Products"
    # headers = [   
    # "S.No","mpn", "Variant SKU","Product Name","Model", "UPC/EAN","taxonomy","Brand", "Short Description","Long Description",
    # "Retail Price", "Unfinished Price", "Finished Price"
    # ]
    headers = ["S.No","Handle","Title","Body (HTML)","Vendor","Product Category","Type","Tags","Published"]
    variant_headers = []
    for i in range(1, max_variants + 1):
        variant_headers.append(f"Option{i} Name")
        variant_headers.append(f"Option{i} Value")
        variant_headers.append(f"Option{i} Linked To")
    headers.extend(variant_headers)
    headers.extend(["Variant Grams","Variant Inventory Tracker","Variant Inventory Qty","Variant Inventory Policy","Variant Fulfillment Service","Variant Price","Variant Compare At Price","Variant Requires Shipping","Variant Taxable","Variant Barcode","Image Src","Image Position","Image Alt Text","Gift Card","SEO Title","SEO Description","Google Shopping / Google Product Category","Google Shopping / Gender","Google Shopping / Age Group","Google Shopping / MPN","Google Shopping / Condition","Google Shopping / Custom Product","Google Shopping / Custom Label 0","Google Shopping / Custom Label 1","Google Shopping / Custom Label 2","Google Shopping / Custom Label 3","Google Shopping / Custom Label 4","Complimentary Product Text (product.metafields.custom.complimentary_product_text)","Custom Additions (product.metafields.custom.custom_additions)","Details as Shown (product.metafields.custom.details_as_shown1)","Dimensions (product.metafields.custom.dimensions1)","Key Features (product.metafields.custom.key_features1)","Options (product.metafields.custom.options1)","Quickship or Regular (product.metafields.custom.quickship_or_regular)","Quickship or Regular Product (product.metafields.custom.quickship_or_regular_product)","Google: Custom Product (product.metafields.mm-google-shopping.custom_product)","Bed/Frame features (product.metafields.shopify.bed-frame-features)","Color (product.metafields.shopify.color-pattern)","Frame color (product.metafields.shopify.frame-color)","Furniture/Fixture features (product.metafields.shopify.furniture-fixture-features)","Furniture/Fixture material (product.metafields.shopify.furniture-fixture-material)","Seat structure (product.metafields.shopify.seat-structure)","Tabletop shape (product.metafields.shopify.tabletop-shape)","Upholstery material (product.metafields.shopify.upholstery-material)","Complementary products (product.metafields.shopify--discovery--product_recommendation.complementary_products)","Related products (product.metafields.shopify--discovery--product_recommendation.related_products)","Related products settings (product.metafields.shopify--discovery--product_recommendation.related_products_display","Variant Image","Variant Weight Unit","Variant Tax Code","Cost per item","Included / United States","Price / United States","Compare At Price / United States","Status"])

    worksheet.append(headers)

    for i, item in enumerate(result):
        i_dict = dict()
        i_dict['level'] = item.get("category level", "")
        i_dict['category_id'] = item.get("category_id", "")
        getCategoryLevelOrder(i_dict)
        row = [
            i + 1,
            item.get("product_name", ""),
            item.get("product_name", ""),
            item.get("long_description", ""),
            item.get("brand", ""),
            item.get("category_last_name", ""),
            i_dict.get("category_name", ""),
            item.get("Tags", ""),
            item.get(""), #Published
        ]
        variant_options = item.get("varient_option_list", [])
        for j in range(max_variants):
            if j < len(variant_options):
                row.append(variant_options[j].get('name', ''))
                row.append(variant_options[j].get('value', ''))
            else:
                row.append('')  # Add empty values for missing variants
                row.append('')  # Add empty values for missing variants
        row.extend(["","","","","",item.get("retail_price",""),"","","",""])
        img_src = item.get("Image Src", [])
        img_src_str = ""
        print(img_src)
        for j in img_src:
            img_src_str = j +"," + img_src_str
        row.append(img_src_str)
        row.extend(["","","","","","","","","","","","","","","","","","","","",item.get("Key Features", ""),"","","","","","","","","","","","","","","","","",""])
        row.append(item.get("Cost per item",""))
        row.extend(["","","",""])
        worksheet.append(row)
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0) 
    response = HttpResponse(buffer, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response


@csrf_exempt
def retrieveData(request):
    data = dict()
    data['status'] = False
    if 'file' not in request.FILES:
        return data
    file = request.FILES['file']
    try:
        if file.name.endswith('.xlsx'):
            sheets_dict = pd.read_excel(file, sheet_name=None)
            all_sheets_json = {}
            for sheet_name, df in sheets_dict.items():
                json_data = df.to_json(orient='records')
                all_sheets_json[sheet_name] = json_data

            with open('sheets_output.json', 'w') as json_file:
                json.dump(all_sheets_json, json_file)
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)
            json_data = df.to_json(orient='records')
        elif file.name.endswith('.txt'):
            df = pd.read_csv(file, sep='\t') 
            json_data = df.to_json(orient='records')
            print(json_data)
        elif file.name.endswith('.pdf'):
            with pdfplumber.open(file) as pdf:
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text()
            print(all_text)
        else:
            return data
    except Exception as e:
        print(">>>",e)
        return data


@csrf_exempt
def obtainVarientForCategory(request):
    category_id = request.GET.get("id")
    client_id = get_current_client()
    pipeline = [
        {
            "$match":{'category_id':category_id}
        },
        {
        '$lookup': {
            'from': 'varient_option',
            'localField': 'varient_option_id_list',
            'foreignField': '_id',
            'as': 'varient_option'
        }
        }, 
        {
            '$unwind': {
                'path': '$varient_option',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            "$match":{'varient_option.client_id':ObjectId(client_id)}
        },
        {
        '$lookup': {
            'from': 'type_name',
            'localField': 'varient_option.option_name_id',
            'foreignField': '_id',
            'as': 'type_name'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_name',
                'preserveNullAndEmptyArrays': True
            }
        },    {
        '$lookup': {
            'from': 'type_value',
            'localField': 'varient_option.option_value_id_list',
            'foreignField': '_id',
            'as': 'type_value'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_value',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
        '$group': {
            "_id":"$varient_option",
            "type_name":{'$first':"$type_name.name"},
            "varient_option_id":{'$first':"$varient_option._id"},
            "type_id":{'$first':"$type_name._id"},
            "category_varient_id":{'$first':"$_id"},
            'option_value_list': {
                "$push": {
                    'type_value_name': "$type_value.name",
                    'type_value_id': "$type_value._id",
                }
            }
        }
        },{
        '$project':{
            "_id":0,
            "type_name":1,
            'option_value_list': 1,
            'varient_option_id':1,
            'category_varient_id':1,
            'type_id':1
        }
        }
        ]
    result = list(category_varient.objects.aggregate(*pipeline))
    
    data = dict()
    data['category_varient_id'] = ""
    if len(result)>0:
        for i in result:
            i['type_id'] = str(i['type_id']) if 'type_id'in i else ""
            data['category_varient_id'] = str(i['category_varient_id'])
            del i['category_varient_id']
            i ['tagged_category_list'] = list()
            category_varient_list = DatabaseModel.list_documents(category_varient.objects,{'varient_option_id_list__in':[ i['varient_option_id']]})
            for ins in category_varient_list:
                dist_i = dict()
                dist_i['level'] = ins.category_level
                dist_i['category_id'] = ins.category_id
                dist_i['category_name'] = ""
                getCategoryLevelOrder(dist_i)
                i ['tagged_category_list'].append(dist_i['category_name'])
            del  i['varient_option_id']
            for j in i['option_value_list']:
                j['type_value_id'] = str(j['type_value_id']) if 'type_value_id'in j else ""
    data['varient_list'] = result
    return data


@csrf_exempt
def createVarientOption(request):
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    client_id = get_current_client()
    name = json_req.get("name").title()
    category_varient_id = json_req.get("category_varient_id")
    category_id = json_req.get("category_id")
    category_level = json_req.get("category_name")
    if category_varient_id == "":
        category_varient_obj = DatabaseModel.save_documents(category_varient,{'category_id':category_id,'category_level':category_level})
        category_varient_id = str(category_varient_obj.id)
    type_name_obj = DatabaseModel.get_document(type_name.objects,{'name':name})
    if type_name_obj:
        type_name_id = type_name_obj.id
        varient_option_obj = DatabaseModel.get_document(varient_option.objects,{'option_name_id':type_name_id,'client_id':ObjectId(client_id)})
        if varient_option_obj:
            varient_option_id = varient_option_obj.id
        else:
            varient_option_obj = DatabaseModel.save_documents(varient_option,{'option_name_id':type_name_id})
            varient_option_id = varient_option_obj.id
        
    else:
        type_name_id = DatabaseModel.save_documents(type_name,{'name':name})
        varient_option_obj = DatabaseModel.save_documents(varient_option,{'option_name_id':type_name_id})
        varient_option_id = varient_option_obj.id
    category_varient_obj = DatabaseModel.get_document(category_varient.objects,{"id":category_varient_id,'varient_option_id_list__in':[varient_option_id]})
    if category_varient_obj:
        data = dict()
        data['is_created'] = False
        data['error'] = "Varient Option Name Already Present"
        return data
    obtainlogForCategoryVarientOption(category_id,varient_option_id,"update",ObjectId(user_login_id),category_level)
    DatabaseModel.update_documents(category_varient.objects,{"id":category_varient_id},{'add_to_set__varient_option_id_list':varient_option_id})
    
    data = dict()
    data['is_created'] = True
    return data


@csrf_exempt
def createValueForVarientName(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    data = dict()
    client_id = get_current_client()
    option_id = json_req.get("option_id")
    type_value_obj = DatabaseModel.get_document(type_value.objects,{'name':name})
    if type_value_obj:
        type_value_id = type_value_obj.id
    else:
        type_value_id = DatabaseModel.save_documents(type_value,{'name':name}).id
    print(option_id,client_id,type_value_id)
    varient_option_obj = DatabaseModel.get_document(varient_option.objects,{"option_name_id":option_id,"client_id":ObjectId(client_id),'option_value_id_list__in':[ObjectId(type_value_id)]})
    if varient_option_obj:
        data['is_created'] = False
        data['error'] = "Value Already Present In This Varient Option"
    else:
        DatabaseModel.update_documents(varient_option.objects,{"option_name_id":option_id,'client_id':client_id},{'add_to_set__option_value_id_list':type_value_id})
        data['is_created'] = True
    return data


def obtainDashboardCount(request):
    data = dict()
    client_id = get_current_client()
    print("///////////////",client_id)
    data['total_product'] = DatabaseModel.count_documents(products.objects,{'client_id':client_id})
    data['total_brand'] = DatabaseModel.count_documents(brand.objects,{'client_id':client_id})
    last_all_ids = []
    category_list = DatabaseModel.list_documents(category.objects,{'client_id':client_id})
    for category_obj in category_list:
        if len(category_obj.level_one_category_list)>0:
            for i in category_obj.level_one_category_list:
                if len(i.level_two_category_list)>0:
                    for j in i.level_two_category_list:
                        if len(j.level_three_category_list)>0:
                            for k in j.level_three_category_list:
                                if len(k.level_four_category_list)>0:
                                    for l in  k.level_four_category_list:
                                        if len(l.level_five_category_list)>0:
                                            for m in  l.level_five_category_list:
                                                last_all_ids.append({'id':m.id,'name':m.name})
                                        else:
                                            last_all_ids.append({'id':l.id,'name':l.name})
                                else:
                                    last_all_ids.append({'id':k.id,'name':k.name})
                        else:
                            last_all_ids.append({'id':j.id,'name':j.name})
                else:
                    last_all_ids.append({'id':i.id,'name':i.name})
        else:
            last_all_ids.append({'id':category_obj.id,'name':category_obj.name})
    data['category_project_dict'] = dict()
    for i in last_all_ids:
        data['category_project_dict'][i['name']] = DatabaseModel.count_documents(product_category_config.objects,{'category_id':str(i['id'])})
    data['total_last_level_category'] = len(last_all_ids)
    data['total_parent_level_category'] = len(category_list)
    pipeline = [
             {
            '$match':{'client_id':ObjectId(client_id)}
        },
        {
        '$lookup': {
            'from': 'type_name',
            'localField': 'option_name_id',
            'foreignField': '_id',
            'as': 'type_name'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_name',
                'preserveNullAndEmptyArrays': True
            }
        },    {
        '$lookup': {
            'from': 'type_value',
            'localField': 'option_value_id_list',
            'foreignField': '_id',
            'as': 'type_value'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_value',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
        '$group': {
            "_id":"$type_name._id",
            "type_name":{'$first':"$type_name.name"},
            'option_value_list': {
                "$push":  "$type_value.name",
            }
        }
        },{
        '$project':{
            "_id":0,
            "type_name":1,
            'option_value_count': {'$size':'$option_value_list'},

        }
        }
        ]
    result = list(varient_option.objects.aggregate(*pipeline))
    data['varent_list'] = result
    return data


@csrf_exempt
def swapProductToCategory(request):
    json_req = JSONParser().parse(request)
    product_id = json_req.get("product_id")
    category_id = json_req.get("category_id")
    category_name = json_req.get("category_name")
    data = dict()
    product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'product_id':product_id})
    previous_category_id = product_category_config_obj.category_id
    DatabaseModel.update_documents(product_category_config.objects,{'product_id':product_id},{'category_level':category_name,"category_id":category_id})
    category_varient_obj = DatabaseModel.get_document(category_varient.objects,{'category_id':previous_category_id})
    varient_option_id_list = category_varient_obj.varient_option_id_list
    pre_category_varient_obj = DatabaseModel.get_document(category_varient.objects,{'category_id':category_id})
    if pre_category_varient_obj:
        pre_category_varient_obj.category_name = category_name
        pre_category_varient_obj.varient_option_id_list.extend(varient_option_id_list)
        pre_category_varient_obj.save()
    else:
        DatabaseModel.save_documents(category_varient,{'category_id':category_id,'varient_option_id_list':varient_option_id_list,"category_level":category_name})
    data['is_update'] = True
    return data





@csrf_exempt
def createAndAddVarient(request):
    data = dict()
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    json_req = JSONParser().parse(request)
    product_id = json_req.get("product_id")
    varient_obj = json_req.get("varient_obj")
    client_id = get_current_client()
    product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":varient_obj['sku_number'],"finished_price":str(varient_obj['finished_price']),"un_finished_price":str(varient_obj['un_finished_price']),"quantity":varient_obj['quantity'],"retail_price":str(varient_obj['retail_price'])})
    for i in varient_obj['options']:
        product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":i['option_name_id'],"option_value_id":i['option_value_id']})
        DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
    logForCreateProductVarient(product_varient_obj.id,user_login_id,"create")
    createradial_price_log(product_varient_obj.id,"0",str(varient_obj['retail_price']),user_login_id,client_id)
    DatabaseModel.update_documents(products.objects,{"id":product_id},{"add_to_set__options":product_varient_obj.id})
    data['status'] = True
    return data


def logForCategory(category_id,action,user_id,level):
    DatabaseModel.save_documents(category_log,{"category_id":str(category_id),"action":str(action),"user_id":ObjectId(user_id),'level':level})
    return 1

def obtainlogForCategoryVarientOption(category_id,category_varient_option_id,action,user_id,category_level):
    DatabaseModel.save_documents(category_varient_option_log,{"category_id":str(category_id),"category_varient_option_id":ObjectId(category_varient_option_id),"user_id":ObjectId(user_id),'action':action,'level':category_level})
    return 1

def logForCreateProduct(product_id,user_id,action):
    DatabaseModel.save_documents(product_log,{"product_id":ObjectId(product_id),"user_id":ObjectId(user_id),'action':action})
    return 1

def logForCreateProductVarient(product_varient_id,user_id,action):
    DatabaseModel.save_documents(product_varient_log,{"product_varient_id":ObjectId(product_varient_id),"user_id":ObjectId(user_id),'action':action})
    return 1



@csrf_exempt
def obtainCategoryLog(request):
    client_id = get_current_client()
    json_req = json.loads(request.body.decode("utf-8")) if request.body else {}
    action = json_req.get("action", None)
    level = json_req.get("level", None)
    if action:
        filter_obj = {'action':action,}
    elif level:
        filter_obj = {'level':level}
    else:
        filter_obj = {}
    pipeline = [
        {
            "$match": filter_obj
        },
        {
            '$lookup': {
                'from': 'user',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_ins'
        }
        },
        {
            '$unwind': {
                'path': '$user_ins',
                'preserveNullAndEmptyArrays': True
            }
        },{
            '$match':{'user_ins.client_id':ObjectId(client_id)}
        },
        {
            '$group': {
                "_id":None,
                "category_log_list":{'$push':{"user_name":"$user_ins.name",'category_id':'$category_id','action':'$action','level':'$level','log_date':'$log_date'}}
        }
        }
        ]
    result = list(category_log.objects.aggregate(*pipeline))
    data = dict()
    data['result'] = []
    if result:
        for i in result[0]['category_log_list']:
            i['category_last_name'] = ""
            getCategoryLevelOrder(i)
            print(i['category_last_name'])
            original_date = i['log_date'] 
            i['log_date_ist'] = convert_to_timezone(original_date, 'Asia/Kolkata').strftime('%Y-%m-%d %H:%M:%S')
            i['log_date'] = convert_to_timezone(original_date, 'US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
        data['result'] = result[0]['category_log_list']
        data['result'] = sorted(data['result'], key=lambda x: x['log_date'],reverse=True)
        return data
    return data


@csrf_exempt
def obtainCategoryVarientLog(request):
    client_id = get_current_client()
    json_req = json.loads(request.body.decode("utf-8")) if request.body else {}
    action = json_req.get("action", None)
    level = json_req.get("level", None)
    if action:
        filter_obj = {'action':action}
    elif level:
        filter_obj = {'level':level}
    else:
        filter_obj = {}
    pipeline = [
        {
            "$match": filter_obj
        },
        {
            '$lookup': {
                'from': 'user',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_ins'
        }
        },
        {
            '$unwind': {
                'path': '$user_ins',
                'preserveNullAndEmptyArrays': True
            }
        },{
            '$match':{'user_ins.client_id':ObjectId(client_id)}
        },
        {
            '$lookup': {
                'from': 'varient_option',
                'localField': 'category_varient_option_id',
                'foreignField': '_id',
                'as': 'varient_option_ins'
        }
        },
        {
            '$unwind': {
                'path': '$varient_option_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            '$lookup': {
                'from': 'type_name',
                'localField': 'varient_option_ins.option_name_id',
                'foreignField': '_id',
                'as': 'type_name_ins'
        }
        },
        {
            '$unwind': {
                'path': '$type_name_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
        
        {
            '$group': {
                "_id":None,
                "category_varient_log_list":{'$push':{"user_name":"$user_ins.name",'category_id':'$category_id','action':'$action','level':'$level','varient_option_name':'$type_name_ins.name','log_date':'$log_date'}}
        }
        }
        ]
    result = list(category_varient_option_log.objects.aggregate(*pipeline))
    data = dict()
    data['result'] = []
    if result:
        for i in result[0]['category_varient_log_list']:
            i['category_last_name'] = ""
            getCategoryLevelOrder(i)
            original_date = i['log_date'] 
            i['log_date_ist'] = convert_to_timezone(original_date, 'Asia/Kolkata').strftime('%Y-%m-%d %H:%M:%S')
            i['log_date'] = convert_to_timezone(original_date, 'US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
        data['result'] = result[0]['category_varient_log_list']
        data['result'] = sorted(data['result'], key=lambda x: x['log_date'],reverse=True)

        return data
    return data



@csrf_exempt
def obtainProductLog(request):
    json_req = json.loads(request.body.decode("utf-8")) if request.body else {}
    action = json_req.get("action", None)
    client_id = get_current_client()
    level = json_req.get("level", None)
    if action:
        filter_obj = {'action':action}
    elif level:
        filter_obj = {'level':level}
    else:
        filter_obj = {}
    pipeline = [
        {
            "$match": filter_obj
        },
        {
            '$lookup': {
                'from': 'user',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_ins'
        }
        },
        {
            '$unwind': {
                'path': '$user_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'product_id',
                'foreignField': '_id',
                'as': 'products_ins'
        }
        },
        {
            '$unwind': {
                'path': '$products_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            "$match":{'products_ins.client_id':ObjectId(client_id)}
        },
        {
            '$group': {
                "_id":None,
                "category_varient_log_list":{'$push':{"user_name":"$user_ins.name",'product_name':'$products_ins.product_name','action':'$action','log_date':'$log_date'}}
        }
        }
        ]
    result = list(product_log.objects.aggregate(*pipeline))
    data = dict()
    data['result'] = []
    if result:
        for i in result[0]['category_varient_log_list']:
            original_date = i['log_date'] 
            i['log_date_ist'] = convert_to_timezone(original_date, 'Asia/Kolkata').strftime('%Y-%m-%d %H:%M:%S')
            i['log_date'] = convert_to_timezone(original_date, 'US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
        data['result']  = result[0]['category_varient_log_list']
        data['result'] = sorted(data['result'], key=lambda x: x['log_date'],reverse=True)
        
        return data
    return data



def convert_to_timezone(dt, tz_name):
    target_tz = timezone(tz_name)
    if is_naive(dt):
        dt = make_aware(dt)
    return dt.astimezone(target_tz)


@csrf_exempt
def obtainProductVarientLog(request):
    json_req = json.loads(request.body.decode("utf-8")) if request.body else {}
    client_id = get_current_client()
    action = json_req.get("action", None)
    level = json_req.get("level", None)
    if action:
        filter_obj = {'action':action}
    elif level:
        filter_obj = {'level':level}
    else:
        filter_obj = {}
    pipeline = [
        {
            "$match": filter_obj
        },
        {
            '$lookup': {
                'from': 'user',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_ins'
        }
        },
        {
            '$unwind': {
                'path': '$user_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$lookup': {
                'from': 'product_varient',
                'localField': 'product_varient_id',
                'foreignField': '_id',
                'as': 'product_varient_ins'
        }
        },
        {
            '$unwind': {
                'path': '$product_varient_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$lookup': {
                'from': 'products',
                'localField': 'product_varient_id',
                'foreignField': 'options',
                'as': 'product_ins'
        }
        },
        {
            "$match":{'product_ins.client_id':ObjectId(client_id)}
        },
        {
            '$unwind': {
                'path': '$product_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
        {
            '$group': {
                "_id":None,
                "product_varient_log_list":{'$push':{"user_name":"$user_ins.name",'sku_number':'$product_varient_ins.sku_number','action':'$action','log_date':'$log_date','product_name':'$product_ins.product_name'}}
        }
        }
        ]
    result = list(product_varient_log.objects.aggregate(*pipeline))
    data = dict()
    data['result'] = []
    if result:
        for i in result[0]['product_varient_log_list']:
            original_date = i['log_date'] 
            i['log_date_ist'] = convert_to_timezone(original_date, 'Asia/Kolkata').strftime('%Y-%m-%d %H:%M:%S')
            i['log_date'] = convert_to_timezone(original_date, 'US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
        data['result'] = result[0]['product_varient_log_list']
        data['result'] = sorted(data['result'], key=lambda x: x['log_date'],reverse=True)
        return data
    return data


@csrf_exempt
def createBrand(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    brand_obj = DatabaseModel.get_document(brand.objects,{'name':name})
    data = dict()
    if brand_obj:
        data['is_created'] = False
        data['error'] = "Brand Already Present"
        return data
    else:
        brand_obj = DatabaseModel.save_documents(brand,{'name':name})
    data['is_created'] = True
    return data


@csrf_exempt
def obtainBrand(request):
    client_id = get_current_client()
    data = dict()
    pipeline = [
        {
            '$match':{'client_id':ObjectId(client_id)}
        },
    {
            '$group': {
                "_id":None,
                "brand_list":{'$push':{"id":"$_id",'name':'$name','brand_number':'$brand_number','logo':'$logo'}}
        }
        }
    ]
    brand_list = list(brand.objects.aggregate(*pipeline))
    data['brand_list'] = list() 
    if brand_list:
        for brand_ins in brand_list[0]['brand_list']:
            brand_ins['id'] = str(brand_ins['id'])
        data['brand_list'] = brand_list[0]['brand_list']
    return data



@csrf_exempt
def upload_file(request):
    data = dict()
    data['status'] = False
    if 'file' not in request.FILES:
        return data
    file = request.FILES['file']
    try:
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        elif file.name.endswith('.csv') or file.name.endswith('.txt'):
            df = pd.read_csv(file)
        else:
            return data
    except Exception as e:
        return data
    row_dict = df.iloc[0].to_dict()
    keys_list = list(row_dict.keys())
    exclude_fields = [key for key in keys_list if re.match(r"^Option\d+.*", key)]
    exclude_fields.extend([key for key in keys_list if re.match(r"^Image\d+.*", key)])
    filtered_keys = [key for key in keys_list if key not in exclude_fields]
    data['extract_list'] = filtered_keys
    xl_mapping_obj = DatabaseModel.get_document(xl_mapping.objects)
    data['Database_list'] = []
    if xl_mapping_obj:
        data['Database_list'] =xl_mapping_obj.data
    data['Database_options'] = [
        "model", "upc_ean", "product_name", "long_description", "short_description", "brand",
        "category level", "breadcrumb", "msrp", "base_price", "Tags", "Variant SKU",
        "Un Finished Price", "Finished Price", "Key Features", 
        "stock"
    ]
    upload_dir = 'uploads/' 
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)  
    fs = FileSystemStorage(location=upload_dir)
    filename = fs.save(file.name, file)
    file_path = os.path.join(fs.location, filename)
    print(file_path)
    data['file_path'] = file_path
    return data


@csrf_exempt
def saveXlData(request):
    data = dict()
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    field_data = request.POST.get('field_data')
    file_path = request.POST.get('file_path')
    data['status'] = False
    print(">>>>>>>>>>>>>>>>>>>>>>>>",1)
    field_data = json.loads(field_data)
    xl_mapping_obj = DatabaseModel.get_document(xl_mapping.objects,{'user_id':user_login_id})
    if xl_mapping_obj:
        DatabaseModel.update_documents(xl_mapping.objects,{'user_id':user_login_id},{'data':field_data})
    else:
        DatabaseModel.save_documents(xl_mapping,{'data':field_data,'user_id':user_login_id})
    model_key= field_data.get('model')
    upc_ean_key= field_data.get('upc_ean')
    product_name_key = field_data.get('product_name')
    long_description_key = field_data.get('long_description')
    short_description_key = field_data.get('short_description')
    brand_key = field_data.get('brand')
    breadcrumb_key = field_data.get('breadcrumb')
    # msrp_key = field_data.get('msrp')
    # base_price_key = field_data.get('base_price')
    Tags_key = field_data.get('Tags')
    Variant_SKU_key = field_data.get('Variant SKU')
    Un_Finished_Price_key = field_data.get('Un Finished Price')
    Finished_Price_key = field_data.get('Finished Price')
    Key_Features_key = field_data.get('Key Features')
    category_level_key = field_data.get('category level')
    stockv_key = field_data.get('stockv')
    client_id = get_current_client()
    print(file_path)
    try:
        with open(file_path, 'r') as file:
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            elif file.name.endswith('.csv') or file.name.endswith('.txt'):
                df = pd.read_csv(file)
            else:
                return data
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
        data['status'] = False
        return data
    row_dict = df.iloc[0].to_dict()
    for i in range(len(df)):
        row_dict = df.iloc[i].to_dict()
        model = None if isinstance(row_dict.get(model_key), float) and math.isnan(row_dict.get(model_key)) else row_dict.get(model_key)
        upc_ean = None if isinstance(row_dict.get(upc_ean_key), float) and math.isnan(row_dict.get(upc_ean_key)) else row_dict.get(upc_ean_key)
        product_name = None if isinstance(row_dict.get(product_name_key), float) and math.isnan(row_dict.get(product_name_key)) else row_dict.get(product_name_key)
        long_description = None if isinstance(row_dict.get(long_description_key), float) and math.isnan(row_dict.get(long_description_key)) else row_dict.get(long_description_key)
        short_description = None if isinstance(row_dict.get(short_description_key), float) and math.isnan(row_dict.get(short_description_key)) else row_dict.get(short_description_key)
        brand_name = None if isinstance(row_dict.get(brand_key), float) and math.isnan(row_dict.get(brand_key)) else row_dict.get(brand_key)
        breadcrumb = None if isinstance(row_dict.get(breadcrumb_key), float) and math.isnan(row_dict.get(breadcrumb_key)) else row_dict.get(breadcrumb_key)
        # msrp = None if isinstance(row_dict.get(msrp_key), float) and math.isnan(row_dict.get(msrp_key)) else row_dict.get(msrp_key)
        # base_price = None if isinstance(row_dict.get(base_price_key), float) and math.isnan(row_dict.get(base_price_key)) else row_dict.get(base_price_key)
        Tags = None if isinstance(row_dict.get(Tags_key), float) and math.isnan(row_dict.get(Tags_key)) else row_dict.get(Tags_key)
        Variant_SKU = None if isinstance(row_dict.get(Variant_SKU_key), float) and math.isnan(row_dict.get(Variant_SKU_key)) else row_dict.get(Variant_SKU_key)
        Un_Finished_Price = "0" if isinstance(row_dict.get(Un_Finished_Price_key), float) and math.isnan(row_dict.get(Un_Finished_Price_key)) else row_dict.get(Un_Finished_Price_key)
        Finished_Price = "0" if isinstance(row_dict.get(Finished_Price_key), float) and math.isnan(row_dict.get(Finished_Price_key)) else row_dict.get(Finished_Price_key)
        # img_src = None if isinstance(row_dict.get("Image Src"), float) and math.isnan(row_dict.get("Image Src")) else row_dict.get("Image Src")
        key_features = None if isinstance(row_dict.get(Key_Features_key), float) and math.isnan(row_dict.get(Key_Features_key)) else row_dict.get(Key_Features_key)
        stockv = None if isinstance(row_dict.get(stockv_key), float) and math.isnan(row_dict.get(stockv_key)) else row_dict.get(stockv_key)
        category_level = None if isinstance(row_dict.get(category_level_key), float) and math.isnan(row_dict.get(category_level_key)) else row_dict.get(category_level_key)
        options = []
        if isinstance(model,str) == False and isinstance(upc_ean,str) == False and isinstance(Variant_SKU,str) == False  and isinstance(category_level,str) == False:
            break
        if isinstance(model,str) == False:
            is_varient = True
        else:
            is_varient = False
        option_name_list = list()
        option_number = 1
        while f'Option{option_number} Name' in row_dict and f'Option{option_number} Value' in row_dict:
            option_name = row_dict[f'Option{option_number} Name']
            option_value = row_dict[f'Option{option_number} Value']
            if is_varient:
                print(option_number)
                option_name = option_name_list[option_number-1]
            else:
                option_name_list.append(option_name)
            if isinstance(option_name, str) :
                options.append({"name":option_name,"value": option_value})
            option_number += 1
        image_str_list = list()
        option_number = 1
        while f'Image{option_number}' in row_dict:
            if is_varient:
                option_name = image_str_list[option_number-1]
            else:
                image_str_list.append(option_name)
            if isinstance(option_name, str) :
                options.append({"name":option_name,"value": option_value})
            option_number += 1
        product_obj = DatabaseModel.get_document(products.objects,{"model":model,'client_id':ObjectId(client_id)})
        print(">>>>>>>>>>>>>>>>>>>>>>>>",product_obj)
        if product_obj==None:
            
            category_list = []
            if isinstance(category_level, str):
                category_list = [item.strip() for item in category_level.split('>')]
            previous_category_id = ""
            for index,i in enumerate(category_list):
                i = i.title()
                if index == 0:
                    category_obj = DatabaseModel.get_document(category.objects,{'name':i,'client_id':client_id})
                    if category_obj == None:
                        category_obj = DatabaseModel.save_documents(category,{'name':i})
                    previous_category_id = category_obj.id
                if index == 1:
                    level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'name':i,'client_id':client_id})
                    if level_one_category_obj == None:
                        level_one_category_obj = DatabaseModel.save_documents(level_one_category,{'name':i})
                    DatabaseModel.update_documents(category.objects,{"id":previous_category_id},{"push__level_one_category_list":level_one_category_obj.id})
                    previous_category_id = level_one_category_obj.id
                if index == 2:
                    level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'name':i,'client_id':client_id})
                    if level_two_category_obj == None:
                        level_two_category_obj = DatabaseModel.save_documents(level_two_category,{'name':i})
                    DatabaseModel.update_documents(level_one_category.objects,{"id":previous_category_id},{"push__level_two_category_list":level_two_category_obj.id})
                    previous_category_id = level_two_category_obj.id
                if index == 3:
                    level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'name':i,'client_id':client_id})
                    if level_three_category_obj == None:
                        level_three_category_obj = DatabaseModel.save_documents(level_three_category,{'name':i})
                    DatabaseModel.update_documents(level_two_category.objects,{"id":previous_category_id},{"push__level_three_category_list":level_three_category_obj.id})
                    previous_category_id = level_three_category_obj.id
                if index == 4:
                    level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'name':i,'client_id':client_id})
                    if level_four_category_obj == None:
                        level_four_category_obj = DatabaseModel.save_documents(level_four_category,{'name':i})
                    DatabaseModel.update_documents(level_three_category.objects,{"id":previous_category_id},{"push__level_four_category_list":level_four_category_obj.id})
                    previous_category_id = level_four_category_obj.id
                if index == 5:
                    level_five_category_obj = DatabaseModel.get_document(level_five_category.objects,{'name':i,'client_id':client_id})
                    if level_five_category_obj == None:
                        level_five_category_obj = DatabaseModel.save_documents(level_five_category,{'name':i})
                    DatabaseModel.update_documents(level_four_category.objects,{"id":previous_category_id},{"push__level_five_category_list":level_five_category_obj.id})
                    previous_category_id = level_five_category_obj.id
            brand_obj = DatabaseModel.get_document(brand.objects,{'name':brand_name.title()})
            if brand_obj:
                brand_id = brand_obj.id
            else:
                brand_obj = DatabaseModel.save_documents(brand,{'name':brand_name.title()})
                brand_id = brand_obj.id
            print(">>>",key_features)
            product_obj = DatabaseModel.save_documents(products,{"model":model,"upc_ean":str(upc_ean),"product_name":product_name.title(),"long_description":long_description,"short_description":short_description,"brand_id":brand_id,"breadcrumb":breadcrumb,"key_features":str(key_features),'tags':Tags,'image':image_str_list})
            product_id = product_obj.id
            category_level = ""
            if len(category_list) == 1:
                category_level = "level-1"
            elif len(category_list) == 2:
                category_level = "level-2"
            elif len(category_list) == 3:
                category_level = "level-3"
            elif len(category_list) == 4:
                category_level = "level-4"
            elif len(category_list) == 5:
                category_level = "level-5"
            elif len(category_list) == 6:
                category_level = "level-6"
            product_category_config_obj = DatabaseModel.save_documents(product_category_config,{'product_id':product_id,'category_level':category_level,"category_id":str(previous_category_id)})
        else:
            product_id = product_obj.id
        product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'product_id':product_id})
        cat_retail_price = 1
        retail_price = "0"
        if Finished_Price == None:
            Finished_Price = "0"
        if Un_Finished_Price == None:
            Un_Finished_Price = "0"
        if product_category_config_obj:
            category_id = product_category_config_obj.category_id
            brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':ObjectId(category_id),'brand_id':ObjectId(product_obj.brand_id.id),'is_active':True})
            if brand_category_price_obj:
                cat_retail_price = brand_category_price_obj.price
                if brand_category_price_obj.price_option == 'finished_price':
                    retail_price = str(float(Finished_Price) * float(cat_retail_price))
                else:
                    retail_price = str(float(Un_Finished_Price) * float(cat_retail_price))
        product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":Variant_SKU,"finished_price":str(Finished_Price),"un_finished_price":str(Un_Finished_Price),"quantity":stockv,"retail_price":retail_price})
        createradial_price_log(product_varient_obj.id,"0",retail_price,user_login_id,client_id)
        
        logForCreateProductVarient(product_varient_obj.id,user_login_id,"create")
        for i in options:
            type_name_obj = DatabaseModel.get_document(type_name.objects,{'name':i['name'].title()})
            if type_name_obj ==None:
                type_name_obj = DatabaseModel.save_documents(type_name,{'name':i['name'].title()})   
            type_name_id = type_name_obj.id
            type_value_obj = DatabaseModel.get_document(type_value.objects,{'name':str(i['value']).title()})
            if type_value_obj ==None:
                type_value_obj = DatabaseModel.save_documents(type_value,{'name':str(i['value']).title()})   
            type_value_id = type_value_obj.id
            product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":type_name_id,"option_value_id":type_value_id})
            DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
        DatabaseModel.update_documents(products.objects,{"id":product_id},{"add_to_set__options":product_varient_obj.id,'add_to_set__image':image_str_list})
    file_path = "/home/dell/PLMP/plmp_backend/uploads"
    print(">>>>>>>>>>>>>>>>>>>>>>>>",2)
    try:
        if os.path.exists(file_path) and os.path.isdir(file_path):
            shutil.rmtree(file_path)
            print(f"Folder {file_path} has been deleted successfully.")
        else:
            print(f"The folder at {file_path} does not exist or is not a valid directory.")
    except Exception as e:
        print(f"An error occurred while deleting the folder: {e}")
    data['status'] = True
    return data


def obtainPriceLog(request):
    data = dict()
    client_id = get_current_client()
    radial_price_log_list = DatabaseModel.list_documents(radial_price_log.objects,{'client_id':client_id})
    data = dict()
    data['result']  = list()
    for i in radial_price_log_list:
        data['result'].append(
        {
        "sku_number" : i.product_varient_id.sku_number,
        "old_retail_price" : i.old_retail_price,
        "new_retail_price" : i.new_retail_price,
        "user_id" : i.user_id.name,
        "log_date" : i.log_date   
        })
    return data
# import requests
# from bs4 import BeautifulSoup
from django.http import JsonResponse

# @csrf_exempt
# def sampleData(req):
#     data_list = data_fn()
#     for data in data_list:
#         category_name = "level-3"
#         category_id = "6728c594f254bfbc4a59a6b6"
#         product_obj = data['product_obj']
#         product_obj_save = {
#             "model" :product_obj['model'],
#             "upc_ean" :product_obj['upc_ean'],
#             "mpn" :product_obj['mpn'],     
#             "breadcrumb":product_obj['breadcrumb'],
#             "brand_id":ObjectId(product_obj['brand_id']),
#             "product_name":product_obj['product_name'],
#             "long_description":product_obj['long_description'],
#             "short_description":product_obj['short_description'],
#             "features":product_obj['features'],
#             "attributes":product_obj['attributes'],
#             "tags":product_obj['tags'],
#             "msrp":str(product_obj['msrp']),
#             "base_price":str(product_obj['base_price']),
#             "key_features":product_obj['key_features'],
#             "image":product_obj['image_str_list']
#         }
#         products_obj_1 = DatabaseModel.save_documents(products,product_obj_save)
#         user_login_id = "6729ac25db9f51647ea76af4"
#         for z in product_obj['varients']:
#             product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":z['sku_number'],"finished_price":str(z['finished_price']),"un_finished_price":str(z['un_finished_price']),"quantity":z['quantity']})
#             logForCreateProductVarient(product_varient_obj.id,user_login_id,"create")
#             for i in z['options']:
#                 type_name_obj = DatabaseModel.get_document(type_name.objects,{'name':i['name'].title()})
#                 if type_name_obj ==None:
#                     type_name_obj = DatabaseModel.save_documents(type_name,{'name':i['name'].title()})   
#                 type_name_id = type_name_obj.id
#                 type_value_obj = DatabaseModel.get_document(type_value.objects,{'name':i['value'].title()})
#                 if type_value_obj ==None:
#                     type_value_obj = DatabaseModel.save_documents(type_value,{'name':i['value'].title()})   
#                 type_value_id = type_value_obj.id
#                 product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":type_name_id,"option_value_id":type_value_id})
#                 DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
#             DatabaseModel.update_documents(products.objects,{"id":products_obj_1.id},{"add_to_set__options":product_varient_obj.id})
#         products_obj = DatabaseModel.save_documents(product_category_config,{'product_id':products_obj_1.id,'category_level':category_name,"category_id":category_id})
#         logForCreateProduct(products_obj_1.id,user_login_id,"create")
#     data = dict()
#     data['status'] = True
#     return JsonResponse(data)




from .data_py import data_list_file
def data_fn():
    return data_list_file



#SuperAdmin
@csrf_exempt
def createClient(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name").title()
    logo = json_req.get("logo")
    location = json_req.get("location")
    client_obj = DatabaseModel.get_document(client.objects,{'name':name})
    data = dict()
    if client_obj:
        data['is_created'] = False
        data['error'] = "client Already Present"
        return data
    else:
        client_obj = DatabaseModel.save_documents(client,{'name':name,'logo':logo,'location':location})
    data['is_created'] = True
    return data


@csrf_exempt
def obtainClient(request):
    data = dict()
    pipeline = [
    {
            '$group': {
                "_id":None,
                "client_list":{'$push':{"id":"$_id",'name':'$name','logo':'$logo','location':'$location'}}
        }
        }
    ]
    client_list = list(client.objects.aggregate(*pipeline))
    data['client_list'] = list() 
    if client_list:
        for client_ins in client_list[0]['client_list']:
            client_ins['id'] = str(client_ins['id'])
        data['client_list'] = client_list[0]['client_list']
    return data


def obtainSuperAdminDashboard(request):
    data = dict()
    data['clients_count'] = DatabaseModel.count_documents(client.objects,{})
    data['active_users_count'] = 0
    return data

@csrf_exempt
def obtainClientDetail(request):
    client_id = request.GET.get("id")
    data = dict()
    pipeline = [
        {
            '$match':{'_id':ObjectId(client_id)}
        }, {
            '$lookup': {
                'from': 'user',
                'localField': 'user_id',
                'foreignField': '_id',
                'as': 'user_ins'
        }
        },
        {
            '$unwind': {
                'path': '$user_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
            '$group': {
                "_id":None,
                "id":{'$push':"$_id"},
                'name':{'$push':'$name'},
                'logo':{'$push':'$logo'},
                'location':{'$push':'$location'},
                "user_list":{'$push':{'name':'$user_ins.name','role':'$user_ins.role'}}
        }
        }
    ]
    client_list = list(client.objects.aggregate(*pipeline))
    data['client_obj'] = dict()
    if client_list:
        client_list = client_list[0]
        client_list['id'] = str(client_list['id'])
        data['client_obj'] = client_list
    return data

@csrf_exempt
def addUserAndRoleForClient(request):
    json_req = JSONParser().parse(request)
    user_obj = json_req.get("user_obj")
    id = json_req.get("id")
    data = dict()
    user_obj = DatabaseModel.get_document(user.objects,{'name':'','email':""})
    if user_obj:
        data['is_created'] = False
        data['error'] = "user Already Present"
        return data
    else:
        DatabaseModel.save_documents(user,{'name':user_obj['name'],'email':user_obj['email'],'role':user_obj['role'],'client_id':ObjectId(user_obj['id'])})

@csrf_exempt
def categoryLevelForChildCategory(request):
    json_req = JSONParser().parse(request)
    dist_i = dict()
    dist_i['level'] = json_req['category_level']
    dist_i['category_id'] = json_req['category_id']
    dist_i['category_name'] = ""
    getCategoryLevelOrder(dist_i)
    return dist_i

def obtainClientName(request):
    client_id = get_current_client()
    client_obj = DatabaseModel.get_document(client.objects,{'id':client_id})
    data = dict()
    data['logo'] = ""
    data['name'] = ""
    if client_obj:
        data['name'] = client_obj.name
        data['logo'] = client_obj.logo
    return data

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from odf.opendocument import load
# from odf.table import Table, TableRow, TableCell
# import os

# @csrf_exempt
# def sampleData(request):
#     data = {'status': False}
#     if 'file' not in request.FILES:
#         return JsonResponse(data, status=400)  # Return 400 Bad Request if no file is uploaded
#     file = request.FILES['file']
#     file_path = os.path.join('/tmp', file.name)
#     try:
#         with open(file_path, 'wb') as f:
#             for chunk in file.chunks():
#                 f.write(chunk)
#         # Convert ODS to JSON
#         json_data = ods_to_json(file_path)
#         print(json_data)
#         data['status'] = True
#         data['data'] = json_data
#         return JsonResponse(data, safe=False)
#     finally:
#         if os.path.exists(file_path):
#             os.remove(file_path)  # Clean up the temporary file even if an error occurs

# def ods_to_json(file_path):
#     doc = load(file_path)
#     data = []
#     for sheet in doc.getElementsByType(Table):
#         sheet_data = []
#         for row in sheet.getElementsByType(TableRow):
#             row_data = {}
#             cells = row.getElementsByType(TableCell)
#             print(cells)
#             if len(cells) > 1:
#                 key = ''.join(node.nodeValue for node in cells[0].childNodes if node.nodeType == 3).strip() 
#                 value = ''.join(node.nodeValue for node in cells[1].childNodes if node.nodeType == 3).strip()
#                 print(key,value)
#                 if key and value:
#                     row_data[key] = value
#             if row_data:
#                 sheet_data.append(row_data)
#         if sheet_data:
#             data.append(sheet_data)
#     return data

def  obtainAllLastLevelIds(request):
    client_id = get_current_client()
    last_all_ids = []
    category_list = DatabaseModel.list_documents(category.objects,{'client_id':ObjectId(client_id)})
    for category_obj in category_list:
        if len(category_obj.level_one_category_list)>0:
            for i in category_obj.level_one_category_list:
                if len(i.level_two_category_list)>0:
                    for j in i.level_two_category_list:
                        if len(j.level_three_category_list)>0:
                            for k in j.level_three_category_list:
                                if len(k.level_four_category_list)>0:
                                    for l in  k.level_four_category_list:
                                        if len(l.level_five_category_list)>0:
                                            for m in  l.level_five_category_list:
                                                last_all_ids.append({'id':str(m.id),'name':m.name})
                                        else:
                                            last_all_ids.append({'id':str(l.id),'name':l.name})
                                else:
                                    last_all_ids.append({'id':str(k.id),'name':k.name})
                        else:
                            last_all_ids.append({'id':str(j.id),'name':j.name})
                else:
                    last_all_ids.append({'id':str(i.id),'name':i.name})
        else:
            last_all_ids.append({'id':str(category_obj.id),'name':category_obj.name})
    data = dict()
    data['last_level_category'] = last_all_ids
    return data

@csrf_exempt
def obtainBrandCategoryWisePrice(request):
    json_req = JSONParser().parse(request)
    brand_category_price_obj_list = DatabaseModel.list_documents(brand_category_price.objects,{'category_id__in':json_req['category_id_list'],'brand_id':ObjectId(json_req['brand_id'])})
    data = dict()
    data['price_list'] = []
    for i in  brand_category_price_obj_list:
        data['price_list'].append(i.price)
    return data


def createBrandCategoryWisePrice(json_req):
    brand_category_price_obj_1 = DatabaseModel.list_documents(brand_category_price.objects,{'category_id__in':json_req['category_id_list'],'brand_id':ObjectId(json_req['brand_id'])})
    for i in brand_category_price_obj_1:
        brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':str(i.category_id),'brand_id':ObjectId(json_req['brand_id']),'is_active':True})
        if brand_category_price_obj:
            DatabaseModel.update_documents(brand_category_price.objects,{'category_id':str(i.category_id),'brand_id':ObjectId(json_req['brand_id']),'is_active':True},{'is_active':False})
        brand_category_price_obj_ch = DatabaseModel.get_document(brand_category_price.objects,{'category_id':str(i.category_id),'brand_id':ObjectId(json_req['brand_id']),'price':json_req['price'],'price_option':json_req['price_option']})
        if brand_category_price_obj_ch:
            DatabaseModel.update_documents(brand_category_price.objects,{'category_id':str(i.category_id),'brand_id':ObjectId(json_req['brand_id']),'price':json_req['price'],'price_option':json_req['price_option']},{'is_active':True})
        else:
            DatabaseModel.save_documents(brand_category_price,{'category_id':str(i.category_id),'brand_id':ObjectId(json_req['brand_id']),'is_active':True,'price':str(json_req['price']),'price_option':json_req['price_option']})
    if len(brand_category_price_obj_1) == 0:
        for i in json_req['category_id_list']:
            DatabaseModel.save_documents(brand_category_price,{'category_id':str(i),'brand_id':ObjectId(json_req['brand_id']),'is_active':True,'price':json_req['price'],'price_option':json_req['price_option']})
    data = dict()
    data['is_created'] = True
    return data

from bson.dbref import DBRef
@csrf_exempt
def updateRetailPrice(request):
    json_req = JSONParser().parse(request)
    user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
    product_category_config_list = DatabaseModel.list_documents(product_category_config.objects,{'category_id__in':json_req['category_id_list']})
    createBrandCategoryWisePrice(json_req)
    for i in product_category_config_list:
        for j in i.product_id.options:
            print("......",i.product_id.id)
            brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':str(i.category_id),'brand_id':ObjectId(json_req['brand_id']),'is_active':True})
            if isinstance(j, DBRef):
                # Dereference and access the data
                old_price = '0'
                j.retail_price = json_req['price']
            else:
                old_price = j.retail_price if 'retail_price' in j else '0'
            if brand_category_price_obj:
                if brand_category_price_obj.price_option == "finished_price":
                    print(j.finished_price,json_req['price'])
                    if j.finished_price == '' or j.finished_price =='None'or j.finished_price ==None:
                        j.finished_price = '0' 
                    j.retail_price = str(float(j.finished_price) * float(json_req['price']))
                else:
                    if j.un_finished_price == '' or j.un_finished_price =='None' or j.un_finished_price ==None:
                        j.un_finished_price = '0'
                    j.retail_price = str(float(j.un_finished_price) * float(json_req['price']))
            if j.retail_price == None:
                j.retail_price = "0"
            j.save()
            client_id = get_current_client()
            
            createradial_price_log(j.id,str(old_price),str(j.retail_price),user_login_id,client_id)
    data = dict()
    data['is_updated'] = True
    return data


@csrf_exempt
def obtainBrandCategoryWisePriceTable(request):
    json_req = JSONParser().parse(request)
    if json_req.get('category_id_list') == None:
        brand_category_price_obj_list = DatabaseModel.list_documents(brand_category_price.objects,{'brand_id':ObjectId(json_req['brand_id'])})
    else:
        if json_req['category_id_list'] == []:
            brand_category_price_obj_list = DatabaseModel.list_documents(brand_category_price.objects,{'brand_id':ObjectId(json_req['brand_id'])})
        else:
            brand_category_price_obj_list = DatabaseModel.list_documents(brand_category_price.objects,{'category_id__in':json_req['category_id_list'],'brand_id':ObjectId(json_req['brand_id'])})
    data = dict()
    data['category_list'] = list()
    for brand_category_price_obj in  brand_category_price_obj_list:
        category_obj = DatabaseModel.get_document(category.objects,{'id':brand_category_price_obj.category_id})
        if category_obj == None:
            category_obj = DatabaseModel.get_document(level_one_category.objects,{'id':brand_category_price_obj.category_id})
        if category_obj == None:
            category_obj = DatabaseModel.get_document(level_two_category.objects,{'id':brand_category_price_obj.category_id})
        if category_obj == None:
            category_obj = DatabaseModel.get_document(level_three_category.objects,{'id':brand_category_price_obj.category_id})
        if category_obj == None:
            category_obj = DatabaseModel.get_document(level_four_category.objects,{'id':brand_category_price_obj.category_id})
        if category_obj == None:
            category_obj = DatabaseModel.get_document(level_five_category.objects,{'id':brand_category_price_obj.category_id})
        data['category_list'].append({"category_name":str(category_obj.name),"id":str(brand_category_price_obj.category_id),"price":brand_category_price_obj.price,"brand_name":brand_category_price_obj.brand_id.name,"brand_id":str(brand_category_price_obj.brand_id.id),"is_active":brand_category_price_obj.is_active,'brand_category_price_id':str(brand_category_price_obj.id),'price_option':brand_category_price_obj.price_option})
    data['category_list'] = sorted(data['category_list'], key=lambda x: ObjectId(x['brand_category_price_id']),reverse=True)

    return data


def createradial_price_log(product_varient_id,old_retail_price,new_retail_price,user_login_id,client_id):
    DatabaseModel.save_documents(radial_price_log,{"product_varient_id":product_varient_id,'old_retail_price':old_retail_price,'new_retail_price':new_retail_price,'user_id':ObjectId(user_login_id),'client_id':ObjectId(client_id)})
    return 1

@csrf_exempt
def updateActiveRetailPrice(request):
    json_req = JSONParser().parse(request)
    brand_category_price_obj_1 = DatabaseModel.update_documents(brand_category_price.objects,{'category_id':json_req['category_id'],'brand_id':json_req['brand_id'],'is_active':True},{'is_active':False})
    brand_category_price_obj_2 = DatabaseModel.update_documents(brand_category_price.objects,{'category_id':json_req['category_id'],'brand_id':json_req['brand_id'],'price':str(json_req['price'])},{'is_active':True})
    data = dict()
    data['is_updated'] = True
    return data
    
@csrf_exempt
def obtainRetailBrandPrice(request):
    json_req = JSONParser().parse(request)
    brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':json_req['category_id'],'brand_id':ObjectId(json_req['brand_id']),'is_active':True})
    data = dict()
    if brand_category_price_obj:
        data['price'] = brand_category_price_obj.price
        data['price_option'] = brand_category_price_obj.price_option
    else:
        data['price'] = 0
        data['price_option'] = ""
    return data

@csrf_exempt
def createUser(request):
    client_id = get_current_client()
    json_req = JSONParser().parse(request)
    DatabaseModel.save_documents(user,{'client_id':ObjectId(client_id),'user_name':json_req['user_name'],'name':json_req['name'],'email':json_req['email'],'role':'admin','password':json_req['password']})
    data = dict()
    data['is_created'] = True
    return data


@csrf_exempt
def obtainVarientOptionForRetailPrice(request):
    data = dict()
    data['varient_option_list'] = []
    varient_option_list = DatabaseModel.list_documents(varient_option.objects,{})
    for i in varient_option_list:
        data['varient_option_list'].append({'id':str(i.option_name_id.id),"name":i.option_name_id.name})
    return data


@csrf_exempt
def obtainVarientOptionValueForRetailPrice(request):
    data = dict()
    option_name_id = request.GET.get('id')
    data['varient_option_value_list'] = []
    varient_option_obj = DatabaseModel.get_document(varient_option.objects,{'option_name_id':option_name_id})
    if varient_option_obj:
        for i in varient_option_obj.option_value_id_list:
            data['varient_option_value_list'].append({'id':str(i.id),"name":i.name})
    return data


# @csrf_exempt
# def updateRetailPriceForVarientOptionValue(request):
#     json_req = JSONParser().parse(request)
#     user_login_id = request.META.get('HTTP_USER_LOGIN_ID')
#     percentage_price = json_req['percentage_price']
#     products_list = DatabaseModel.list_documents(products.objects,{'brand':json_req['brand_id']})
#     for i in products_list:
#         for j in i.options:
#             if json_req['option_name_id'] ==  str(j.varient_option_id.option_name_id.id)  and j.varient_option_id.option_value_id.id in json_req['option_value_id_list']:
#                 if json_req['price_option'] == 'finished_price':
#                     j.retail_price = ((j.finished_price/100)*percentage_price) + j.finished_price
#                 else:
#                     j.retail_price = ((j.un_finished_price/100)*percentage_price) + j.un_finished_price
#     data = dict()
#     data['is_updated'] = True
#     return data
@csrf_exempt
def obtainProductBasedOnVarientOption(request):
    json_req = JSONParser().parse(request)
    price_option = json_req['price_option'] 
    option_value_id_list = [ObjectId(i) for i in json_req['option_value_id']]
    pipeline = [
    {
            "$match":{'brand_id':ObjectId(json_req['brand_id'])}
        },
        {
            '$lookup': {
                "from": 'product_varient',
                "localField": 'options',
                "foreignField": "_id",
                "as": "product_varient_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            '$lookup': {
                "from": 'product_varient_option',
                "localField": 'product_varient_ins.varient_option_id',
                "foreignField": "_id",
                "as": "product_varient_option_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_option_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            "$match":{'product_varient_option_ins.option_name_id':ObjectId(json_req['option_name_id']),'product_varient_option_ins.option_value_id':{'$in':(option_value_id_list)}}
        },
        {
        '$lookup': {
            'from': 'type_name',
            'localField': 'product_varient_option_ins.option_name_id',
            'foreignField': '_id',
            'as': 'type_name'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_name',
                'preserveNullAndEmptyArrays': True
            }
        },    {
        '$lookup': {
            'from': 'type_value',
            'localField': 'product_varient_option_ins.option_value_id',
            'foreignField': '_id',
            'as': 'type_value'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_value',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        '$group': {
            "_id":"$product_varient_ins._id",
            "product_id": { "$first": "$_id" },
            "product_varient_id": { "$first": "$product_varient_ins._id" },
            "product_name": { "$first": "$product_name" },
            "sku_number": { "$first": "$product_varient_ins.sku_number" },
            "finished_price": { "$first": "$product_varient_ins.finished_price" },
            "un_finished_price": { "$first": "$product_varient_ins.un_finished_price" },
            "retail_price": { "$first": "$product_varient_ins.retail_price" },
            "image_url": { "$first": "$image" },
            'varient_option_list': {
                "$push": {
                    'type_name': "$type_name.name",
                    'type_value': "$type_value.name",
                }
            }
        }
    }, {
            '$project': {
            "_id": 0,
            'product_id':1,
            'product_varient_id':1,
            'product_name':1,
            "sku_number":1,
            'retail_price':1,
            "finished_price":1,
            "un_finished_price":1,
            "quantity": 1,
            "image_url": 1,
            'varient_option_list':1
            }
        }
    ]
    result = list(products.objects.aggregate(*pipeline))
    for i in result:
        i['brand_id'] = str(json_req['brand_id'])
        i[price_option] = float(i[price_option])
        json_req['price'] = float(json_req['price'])
        i['price_adding_sympol'] = json_req['price_symbol']
        if json_req['price_symbol'] == '%':
            i[price_option] = i[price_option] + (i[price_option]/100*json_req['price'])
        else:
            i[price_option] = float(i[price_option]) + (json_req['price'])
        product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'product_id':i['product_id']})
        i['product_id'] = str(i['product_id'])
        i['product_varient_id'] = str(i['product_varient_id'])
        category_id = ""
        if product_category_config_obj:
            category_id = product_category_config_obj.category_id
        i['category_id'] = product_category_config_obj.category_id
        brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':category_id,'brand_id':ObjectId(json_req['brand_id']),'price_option':price_option,'is_active':True})
        if brand_category_price_obj:
            i['retail_price'] =  str(i[price_option] * float(brand_category_price_obj.price))
        else:
            i['retail_price'] = str(i[price_option])
        i[price_option] = str(i[price_option])
        i['price_option'] = price_option
    return result

@csrf_exempt
def saveChangesForVarientOption(request):
    json_req = JSONParser().parse(request)
    result_list = json_req['result_list'] 
    data = dict()
    data['result_list'] = json_req['result_list']
    for i in result_list:
        brand_id = i['brand_id']
        product_varient_obj = DatabaseModel.get_document(product_varient.objects,{'id':i['product_varient_id']})
        for j in i['varient_option_list']:
            type_name_id = DatabaseModel.get_document(type_name.objects,{'name':j['type_name']}).id
            type_value_id =DatabaseModel.get_document(type_value.objects,{'name':j['type_value']}).id
            if i['price_option'] == 'finished_price':
                revert_varient_retail_price_obj = DatabaseModel.get_document(revert_varient_retail_price.objects,{"brand_id" :ObjectId(brand_id),"type_name_id" :type_name_id,"type_value_id" :type_value_id,"current_price" :i['finished_price'],"old_price":product_varient_obj.finished_price,"old_retail_price":product_varient_obj.retail_price,"current_retail_price":str(i['retail_price']),'price_option':i['price_option']})
            else:
                revert_varient_retail_price_obj = DatabaseModel.get_document(revert_varient_retail_price.objects,{"brand_id" :ObjectId(brand_id),"type_name_id" :type_name_id,"type_value_id" :type_value_id,"current_price" :i['un_finished_price'],"old_price":product_varient_obj.un_finished_price,"old_retail_price":product_varient_obj.retail_price,"current_retail_price":str(i['retail_price']),'price_option':i['price_option']})
                
            if revert_varient_retail_price_obj == None:
                if i['price_option'] == 'finished_price':
                    DatabaseModel.save_documents(revert_varient_retail_price,{"brand_id" :ObjectId(brand_id),"type_name_id" :type_name_id,"type_value_id" :type_value_id,"current_price" :i['finished_price'],"old_price":product_varient_obj.finished_price,"old_retail_price":product_varient_obj.retail_price,"current_retail_price":str(i['retail_price']),'price_option':i['price_option'],'price_adding_sympol':i['price_adding_sympol']})
                else:
                    DatabaseModel.save_documents(revert_varient_retail_price,{"brand_id" :ObjectId(brand_id),"type_name_id" :type_name_id,"type_value_id" :type_value_id,"current_price" :i['un_finished_price'],"old_price":product_varient_obj.un_finished_price,"old_retail_price":product_varient_obj.retail_price,"current_retail_price":str(i['retail_price']),'price_option':i['price_option']})
            else:
                revert_varient_retail_price_obj.old_retail_price = product_varient_obj.retail_price
                revert_varient_retail_price_obj.current_retail_price = str(i['retail_price'])
        product_varient_obj.finished_price = i['finished_price']
        product_varient_obj.un_finished_price = i['un_finished_price']
        product_varient_obj.retail_price = str(i['retail_price'])
        product_varient_obj.save()
    return data

@csrf_exempt
def obtainRevertPreviousAndCurrentPriceForCategory(request):
    json_req = JSONParser().parse(request)
    data = dict()
    brand_category_price_list = DatabaseModel.list_documents(brand_category_price.objects,{'category_id__in':json_req['category_id'],'brand_id':ObjectId(json_req['brand_id']),'price_option':json_req['price_option']})
    data['old_price'] = 0
    data['current_price'] = 0
    last_two_values = []
    brand_category_price_list = list(brand_category_price_list) 
    if len(brand_category_price_list) >= 2:
        last_two_values = brand_category_price_list[-2:]
        data['old_price'] = last_two_values[0].price
        data['current_price'] = last_two_values[1].price
    elif len(brand_category_price_list) == 1:
        data['current_price'] = brand_category_price_list[0].price
        data['old_price'] = brand_category_price_list[0].price
    return data


@csrf_exempt
def obtainRevertPreviousAndCurrentPriceForVarientOption(request):
    json_req = JSONParser().parse(request)
    brand_id = json_req.get('brand_id')
    type_name_id = json_req.get('option_name_id')
    type_value_id = json_req.get('option_value_id')
    type_value_id = [ObjectId(i) for i in type_value_id]
    data = dict()
    revert_varient_retail_price_obj = DatabaseModel.list_documents(revert_varient_retail_price.objects,{'brand_id':brand_id,'type_name_id':type_name_id,'type_value_id__in':type_value_id,'price_option':json_req['price_option']})
    revert_varient_retail_price_obj = list(revert_varient_retail_price_obj)
    if revert_varient_retail_price_obj:
        revert_varient_retail_price_obj = revert_varient_retail_price_obj[-1]
    print(revert_varient_retail_price_obj)
    data['current_price'] = 0
    data['old_price'] = 0
    if revert_varient_retail_price_obj:
        data['old_price'] = revert_varient_retail_price_obj.old_price
        data['current_price'] = revert_varient_retail_price_obj.current_price
    return data

@csrf_exempt
def updateRevertPriceForCategory(request):
    json_req = JSONParser().parse(request)
    brand_category_price_list = DatabaseModel.list_documents(brand_category_price.objects,{'category_id__in':json_req['category_id'],'brand_id':ObjectId(json_req['brand_id']),'price_option':json_req['price_option']})
    old_price = 0
    current_price = 0
    last_two_values = []
    brand_category_price_list = list(brand_category_price_list) 
    if len(brand_category_price_list) >= 2:
        last_two_values = brand_category_price_list[-2:]
        old_price = last_two_values[0].price
        current_price = last_two_values[1].price
    elif len(brand_category_price_list) == 1:
        current_price = brand_category_price_list[0].price
        old_price = brand_category_price_list[0].price
    brand_category_price_obj_1 = DatabaseModel.get_document(brand_category_price.objects,{'category_id__in':json_req['category_id'],'brand_id':ObjectId(json_req['brand_id']),'price':old_price,'price_option':json_req['price_option']})
    if brand_category_price_obj_1:
        brand_category_price_obj_1.is_active = True
        brand_category_price_obj_1.save()
    brand_category_price_obj_2 = DatabaseModel.get_document(brand_category_price.objects,{'category_id__in':json_req['category_id'],'brand_id':ObjectId(json_req['brand_id']),'price':current_price,'price_option':json_req['price_option']})
    if brand_category_price_obj_2:
        brand_category_price_obj_2.delete()
        
    pipeline = [
    {
            "$match":{'brand_id':ObjectId(json_req['brand_id'])}
        },
        {
            '$lookup': {
                "from": 'product_category_config',
                "localField": '_id',
                "foreignField": "product_id",
                "as": "product_category_config_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_category_config_ins',
                'preserveNullAndEmptyArrays': True
            }
        },{
            "$match":{'product_category_config_ins.category_id':str(json_req['category_id'])}
        },
        
        {
            '$lookup': {
                "from": 'product_varient',
                "localField": 'options',
                "foreignField": "_id",
                "as": "product_varient_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_ins',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        '$group': {
            "_id":"$product_varient_ins._id",
            "product_varient_id": { "$first": "$product_varient_ins._id" },
            "finished_price": { "$first": "$product_varient_ins.finished_price" },
            "un_finished_price": { "$first": "$product_varient_ins.un_finished_price" },
            "retail_price": { "$first": "$product_varient_ins.retail_price" },
        }
    }
    ]
    result = list(products.objects.aggregate(*pipeline))
    for i in result:
        if json_req['price_option'] == 'finished_price':
            retail_price = str(float(i['finished_price']) * float(brand_category_price_obj_1['price']))
            DatabaseModel.update_documents(product_varient.objects,{'id':i['product_varient_id']},{'retail_price':retail_price})
    data = dict()
    data['is_updated'] = True
    return data

@csrf_exempt
def updateRevertPriceForVarientOption(request):
    json_req = JSONParser().parse(request)
    revert_varient_retail_price_obj = DatabaseModel.list_documents(revert_varient_retail_price.objects,{'brand_id':json_req['brand_id'],'type_name_id':json_req['option_name_id'],'type_value_id__in':json_req['option_value_id'],'price_option':json_req['price_option']})
    revert_varient_retail_price_obj = list(revert_varient_retail_price_obj)
    if revert_varient_retail_price_obj:
        revert_varient_retail_price_obj = revert_varient_retail_price_obj[-1]
    else:
        data = dict()
        data['is_updated'] = False
        return data
    price_option = json_req['price_option']
    pipeline = [
    {
            "$match":{'brand_id':ObjectId(json_req['brand_id'])}
        },
        {
            '$lookup': {
                "from": 'product_varient',
                "localField": 'options',
                "foreignField": "_id",
                "as": "product_varient_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            '$lookup': {
                "from": 'product_varient_option',
                "localField": 'product_varient_ins.varient_option_id',
                "foreignField": "_id",
                "as": "product_varient_option_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_varient_option_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            "$match":{'product_varient_option_ins.option_name_id':ObjectId(json_req['option_name_id']),'product_varient_option_ins.option_value_id':{'$in':json_req['option_value_id']}}
        },
        {
        '$lookup': {
            'from': 'type_name',
            'localField': 'product_varient_option_ins.option_name_id',
            'foreignField': '_id',
            'as': 'type_name'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_name',
                'preserveNullAndEmptyArrays': True
            }
        },    {
        '$lookup': {
            'from': 'type_value',
            'localField': 'product_varient_option_ins.option_value_id',
            'foreignField': '_id',
            'as': 'type_value'
        }
        }, 
        {
            '$unwind': {
                'path': '$type_value',
                'preserveNullAndEmptyArrays': True
            }
        },
    {
        '$group': {
            "_id":"$product_varient_ins._id",
            "product_id": { "$first": "$_id" },
            "product_varient_id": { "$first": "$product_varient_ins._id" },
            "product_name": { "$first": "$product_name" },
            "sku_number": { "$first": "$product_varient_ins.sku_number" },
            "finished_price": { "$first": "$product_varient_ins.finished_price" },
            "un_finished_price": { "$first": "$product_varient_ins.un_finished_price" },
            "retail_price": { "$first": "$product_varient_ins.retail_price" },
            "image_url": { "$first": "$image" },
            'varient_option_list': {
                "$push": {
                    'type_name': "$type_name.name",
                    'type_value': "$type_value.name",
                }
            }
        }
    }, {
            '$project': {
            "_id": 0,
            'product_id':1,
            'product_varient_id':1,
            'product_name':1,
            "sku_number":1,
            'retail_price':1,
            "finished_price":1,
            "un_finished_price":1,
            "quantity": 1,
            "image_url": 1,
            'varient_option_list':1
            }
        }
    ]
    result = list(products.objects.aggregate(*pipeline))
    for i in result:
        i['brand_id'] = str(json_req['brand_id'])
        i[price_option] = float(i[price_option])
        json_req['price'] = float(revert_varient_retail_price_obj.old_price)
        if revert_varient_retail_price_obj.price_adding_sympol == '%':
            i[price_option] = i[price_option] + (i[price_option]/100*json_req['price'])
        else:
            i[price_option] = float(i[price_option]) + (json_req['price'])
        product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{'product_id':i['product_id']})
        i['product_id'] = str(i['product_id'])
        i['product_varient_id'] = str(i['product_varient_id'])
        category_id = ""
        if product_category_config_obj:
            category_id = product_category_config_obj.category_id
        i['category_id'] = product_category_config_obj.category_id
        brand_category_price_obj = DatabaseModel.get_document(brand_category_price.objects,{'category_id':category_id,'brand_id':ObjectId(json_req['brand_id']),'price_option':price_option,'is_active':True})
        if brand_category_price_obj:
            i['retail_price'] =  str(i[price_option] * float(brand_category_price_obj.price))
        else:
            i['retail_price'] = str(i[price_option])
        i[price_option] = str(i[price_option])
        i['price_option'] = str(i[price_option])
        if price_option =='finished_price':
            DatabaseModel.update_documents(product_varient.objects,{'id':i['product_varient_id']},{'finished_price':i[price_option],'retail_price':i['retail_price']})
        else:
            DatabaseModel.update_documents(product_varient.objects,{'id':i['product_varient_id']},{'un_finished_price':i[price_option],'retail_price':i['retail_price']})
    revert_varient_retail_price_obj.delete()
    data = dict()
    data['is_updated'] = True
    return data
