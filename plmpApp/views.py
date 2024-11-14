
from django.http import JsonResponse
from .models import category
from .models import products
from .models import product_type
from .models import section
from .models import varient_option
from .models import level_one_category
from .models import level_two_category
from .models import level_three_category
from .models import level_four_category
from .models import level_five_category
from .models import product_category_config
from .models import product_varient_option
from .models import product_varient
from .models import category_varient
from .models import type_name
from .models import type_value
from django.http import HttpResponse
from openpyxl import Workbook
import pandas as pd
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
import json
from bson import ObjectId
from rest_framework import status
from rest_framework.decorators import api_view
from .global_service import DatabaseModel
from django.core.management.utils import get_random_secret_key
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
#CRUD
#create
@csrf_exempt
def createCategory(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    category_obj = DatabaseModel.save_documents(category,{'name':name})
    data = dict()
    data['is_created'] = True
    return data

@csrf_exempt
def createCategory1(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    category_id = json_req.get("category_id")
    level_one_categoryn_obj = DatabaseModel.save_documents(level_one_category,{'name':name})
    DatabaseModel.update_documents(category.objects,{"id":category_id},{'add_to_set__level_one_category_list':level_one_categoryn_obj.id})
    data = dict()
    data['is_created'] = True
    return data
@csrf_exempt
def createCategory2(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    category_id = json_req.get("category_id")
    section_obj = DatabaseModel.save_documents(level_two_category,{'name':name})
    DatabaseModel.update_documents(level_one_category.objects,{"id":category_id},{'add_to_set__level_two_category_list':section_obj.id})
    data = dict()
    data['is_created'] = True
    return data


@csrf_exempt
def createCategory3(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    section_id = json_req.get("category_id")
    product_type_obj = DatabaseModel.save_documents(level_three_category,{'name':name})
    DatabaseModel.update_documents(level_two_category.objects,{"id":section_id},{'add_to_set__level_three_category_list':product_type_obj.id})
    data = dict()
    data['is_created'] = True
    return data
@csrf_exempt
def createCategory4(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    section_id = json_req.get("category_id")
    product_type_obj = DatabaseModel.save_documents(level_four_category,{'name':name})
    DatabaseModel.update_documents(level_three_category.objects,{"id":section_id},{'add_to_set__level_four_category_list':product_type_obj.id})
    data = dict()
    data['is_created'] = True
    return data

@csrf_exempt
def createCategory5(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    section_id = json_req.get("category_id")
    product_type_obj = DatabaseModel.save_documents(level_five_category,{'name':name})
    DatabaseModel.update_documents(level_four_category.objects,{"id":section_id},{'add_to_set__level_five_category_list':product_type_obj.id})
    data = dict()
    data['is_created'] = True
    return data

@csrf_exempt
def createProduct(request):
    json_req = JSONParser().parse(request)
    product_obj = json_req.get("product_obj")
    category_id = product_obj["category_id"]
    category_name = product_obj["category_name"]
    product_obj_save = {
        "model" :product_obj['model'],
        "upc_ean" :product_obj['upc_ean'],
        "upc_ean" :product_obj['upc_ean'],
        "breadcrumb":product_obj['breadcrumb'],
        "brand":product_obj['brand_name'],
        "product_name":product_obj['product_name'],
        "long_description":product_obj['long_description'],
        "short_description":product_obj['short_description'],
        "features":product_obj['features'],
        "attributes":product_obj['attributes'],
        "tags":product_obj['tags'],
        "msrp":str(product_obj['msrp']),
        "base_price":str(product_obj['base_price']),
        "key_features":product_obj['key_features']
    }
    products_obj_1 = DatabaseModel.save_documents(products,product_obj_save)
    all_ids = ""
    if category_name == "level-1":
        category_obj = DatabaseModel.get_document(category.objects,{'id':category_id})
        if category_obj:
            all_ids = category_obj.name
            for i in category_obj.level_one_category_list:
                all_ids = all_ids  + ">"+ i.name 
                for j in i.level_two_category_list:
                    all_ids = all_ids + ">"+ j.name 
                    for k in j.level_three_category_list:
                        all_ids = all_ids + ">"+ k.name
                        for l in  k.level_four_category_list:
                            all_ids = all_ids + ">"+ l.name 
                            for m in  l.level_five_category_list:
                                all_ids = all_ids + ">"+ m.name 
    elif  category_name == "level-2":
        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'id':category_id})
        if level_one_category_obj:
            all_ids = level_one_category_obj.name
            for j in level_one_category_obj.level_two_category_list:
                all_ids = all_ids + ">"+ j.name 
                for k in j.level_three_category_list:
                    all_ids = all_ids + ">"+ k.name
                    for l in  k.level_four_category_list:
                        all_ids = all_ids + ">"+ l.name 
                        for m in  l.level_five_category_list:
                            all_ids = all_ids + ">"+ m.name 

    elif  category_name == "level-3":
        level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'id':category_id})
        if level_two_category_obj:
            all_ids = level_two_category_obj.name
            for k in level_two_category_obj.level_three_category_list:
                all_ids = all_ids + ">"+ k.name
                for l in  k.level_four_category_list:
                    all_ids = all_ids + ">"+ l.name 
                    for m in  l.level_five_category_list:
                        all_ids = all_ids + ">"+ m.name
    elif  category_name == "level-4":
        level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'id':category_id})
        if level_three_category_obj:
            all_ids = level_three_category_obj.name
            for l in  level_three_category_obj.level_four_category_list:
                all_ids = all_ids + ">"+ l.name 
                for m in  l.level_five_category_list:
                    all_ids = all_ids + ">"+ m.name
    elif  category_name == "level-5":
        level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'id':category_id})
        if level_four_category_obj:
            all_ids = level_three_category_obj.name
            for m in  level_four_category_obj.level_five_category_list:
                all_ids = all_ids + ">"+ m.name
    for z in product_obj['varients']:
        product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":z['sku_number'],"finished_price":str(z['finished_price']),"un_finished_price":str(z['un_finished_price']),"quantity":z['quantity']})
        for i in z['options']:
            product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":i['option_name_id'],"option_value_id":i['option_value_id']})
            DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
        DatabaseModel.update_documents(products.objects,{"id":products_obj_1.id},{"add_to_set__options":product_varient_obj.id})
    products_obj = DatabaseModel.save_documents(product_category_config,{'product_id':products_obj_1.id,'category_level':all_ids,"category_id":category_id})
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
    name = json_req.get("name")
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

    pipeline = [
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
    }
]

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
    category_id = request.GET.get("id")
    level_name = request.GET.get("level_name")
    if category_id:
        all_ids = []
        if level_name == "level-1":
            category_obj = DatabaseModel.get_document(category.objects,{'id':category_id})
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

        category_obj = {"category_id":{'$in':[all_ids]}}
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
        '$group': {
            "_id":None,
            'product_list': {
                "$push": {
                    'product_name': "$products.product_name",
                    'product_id': "$products._id",
                    'model':"$products.model",
                    'upc_ean':"$products.upc_ean",
                    'breadcrumb':"$products.breadcrumb",
                    'brand':"$products.brand",
                    'product_name':"$products.product_name",
                    'long_description':"$products.long_description",
                    'short_description':"$products.short_description",
                    'features':"$products.features",
                    'attributes':"$products.attributes",
                    'tags':"$products.tags",
                    'msrp':"$products.msrp",
                    'base_price':"$products.base_price",
                    'key_features':"$products.key_features",
                    'image':"$products.image",
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
        data['product_list'] = result['product_list']
        data['product_count'] = len(result['product_list'])
    return data


import math
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
    for i in range(len(df)):
        print(i)
        row_dict = df.iloc[i].to_dict()
        if not pd.isna(row_dict.get("Variant SKU")):
            print(">>123")
            model = None if isinstance(row_dict.get("model"), float) and math.isnan(row_dict.get("model")) else row_dict.get("model")
            upc_ean = None if isinstance(row_dict.get("upc_ean"), float) and math.isnan(row_dict.get("upc_ean")) else row_dict.get("upc_ean")
            product_name = None if isinstance(row_dict.get("product_name"), float) and math.isnan(row_dict.get("product_name")) else row_dict.get("product_name")
            long_description = None if isinstance(row_dict.get("long_description"), float) and math.isnan(row_dict.get("long_description")) else row_dict.get("long_description")
            short_description = None if isinstance(row_dict.get("short_description"), float) and math.isnan(row_dict.get("short_description")) else row_dict.get("short_description")
            brand = None if isinstance(row_dict.get("brand"), float) and math.isnan(row_dict.get("brand")) else row_dict.get("brand")
            breadcrumb = None if isinstance(row_dict.get("breadcrumb"), float) and math.isnan(row_dict.get("breadcrumb")) else row_dict.get("breadcrumb")
            msrp = None if isinstance(row_dict.get("msrp"), float) and math.isnan(row_dict.get("msrp")) else row_dict.get("msrp")
            base_price = None if isinstance(row_dict.get("base_price"), float) and math.isnan(row_dict.get("base_price")) else row_dict.get("base_price")
            Tags = None if isinstance(row_dict.get("Tags"), float) and math.isnan(row_dict.get("Tags")) else row_dict.get("Tags")
            Variant_SKU = None if isinstance(row_dict.get("Variant SKU"), float) and math.isnan(row_dict.get("Variant SKU")) else row_dict.get("Variant SKU")
            Un_Finished_Price = None if isinstance(row_dict.get("Un Finished Price"), float) and math.isnan(row_dict.get("Un Finished Price")) else row_dict.get("Un Finished Price")
            Finished_Price = None if isinstance(row_dict.get("Finished Price"), float) and math.isnan(row_dict.get("Finished Price")) else row_dict.get("Finished Price")
            img_src = None if isinstance(row_dict.get("Image Src"), float) and math.isnan(row_dict.get("Image Src")) else row_dict.get("Image Src")
            image_position = None if isinstance(row_dict.get("Image Position"), float) and math.isnan(row_dict.get("Image Position")) else row_dict.get("Image Position")
            key_features = None if isinstance(row_dict.get("Key Features"), float) and math.isnan(row_dict.get("Key Features")) else row_dict.get("Key Features")
            stockv = None if isinstance(row_dict.get("stockv"), float) and math.isnan(row_dict.get("stockv")) else row_dict.get("stockv")
            category_level = None if isinstance(row_dict.get("category level"), float) and math.isnan(row_dict.get("category level")) else row_dict.get("category level")
            options = []
            if isinstance(model, str) == False:
                is_varient = True
            else:
                is_varient = False
            option_name_list = list()
            option_number = 1
            while f'Option{option_number} Name' in row_dict and f'Option{option_number} Value' in row_dict:
                option_name = row_dict[f'Option{option_number} Name']
                option_value = row_dict[f'Option{option_number} Value']
                if is_varient:
                    option_name = option_name_list[option_number-1]
                else:
                    option_name_list.append(option_name)
                if isinstance(option_name, str) :
                    options.append({"name":option_name,"value": option_value})
                option_number += 1
            product_obj = DatabaseModel.get_document(products.objects,{"model":model})
            if product_obj==None:
                category_list = []
                if isinstance(category_level, str):
                    category_list = [item.strip() for item in category_level.split('>')]
                previous_category_id = ""
                for index,i in enumerate(category_list):
                    if index == 0:
                        category_obj = DatabaseModel.get_document(category.objects,{'name':i})
                        if category_obj == None:
                            category_obj = DatabaseModel.save_documents(category,{'name':i})
                        previous_category_id = category_obj.id
                    if index == 1:
                        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'name':i})
                        if level_one_category_obj == None:
                            level_one_category_obj = DatabaseModel.save_documents(level_one_category,{'name':i})
                        DatabaseModel.update_documents(category.objects,{"id":previous_category_id},{"push__level_one_category_list":level_one_category_obj.id})
                        previous_category_id = level_one_category_obj.id
                    if index == 2:
                        level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'name':i})
                        if level_two_category_obj == None:
                            level_two_category_obj = DatabaseModel.save_documents(level_two_category,{'name':i})
                        DatabaseModel.update_documents(level_one_category.objects,{"id":previous_category_id},{"push__level_two_category_list":level_two_category_obj.id})
                        previous_category_id = level_two_category_obj.id
                    if index == 3:
                        level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'name':i})
                        if level_three_category_obj == None:
                            level_three_category_obj = DatabaseModel.save_documents(level_three_category,{'name':i})
                        DatabaseModel.update_documents(level_two_category.objects,{"id":previous_category_id},{"push__level_three_category_list":level_three_category_obj.id})
                        previous_category_id = level_three_category_obj.id
                    if index == 4:
                        level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'name':i})
                        if level_four_category_obj == None:
                            level_four_category_obj = DatabaseModel.save_documents(level_four_category,{'name':i})
                        DatabaseModel.update_documents(level_three_category.objects,{"id":previous_category_id},{"push__level_four_category_list":level_four_category_obj.id})
                        previous_category_id = level_four_category_obj.id
                    if index == 5:
                        level_five_category_obj = DatabaseModel.get_document(level_five_category.objects,{'name':i})
                        if level_five_category_obj == None:
                            level_five_category_obj = DatabaseModel.save_documents(level_five_category,{'name':i})
                        DatabaseModel.update_documents(level_four_category.objects,{"id":previous_category_id},{"push__level_five_category_list":level_five_category_obj.id})
                        previous_category_id = level_five_category_obj.id
                product_obj = DatabaseModel.save_documents(products,{"model":model,"upc_ean":str(upc_ean),"product_name":product_name,"long_description":long_description,"short_description":short_description,"brand":brand,"breadcrumb":breadcrumb,"msrp":str(msrp),"base_price":str(base_price),"key_features":key_features,'tags':Tags})
                product_id = product_obj.id
                product_category_config_obj = DatabaseModel.save_documents(product_category_config,{'product_id':product_id,'category_level':category_level,"category_id":str(previous_category_id)})
            else:
                product_id = product_obj.id 
            product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":Variant_SKU,"finished_price":Finished_Price,"un_finished_price":Un_Finished_Price,"quantity":stockv,'image_url':[img_src]})
            for i in options:
                type_name_obj = DatabaseModel.get_document(type_name.objects,{'name':i['name']})
                if type_name_obj ==None:
                    type_name_obj = DatabaseModel.save_documents(type_name,{'name':i['name']})   
                type_name_id = type_name_obj.id
                type_value_obj = DatabaseModel.get_document(type_value.objects,{'name':i['value']})
                if type_value_obj ==None:
                    type_value_obj = DatabaseModel.save_documents(type_value,{'name':i['value']})   
                type_value_id = type_value_obj.id
                product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":type_name_id,"option_value_id":type_value_id})
                DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
            DatabaseModel.update_documents(products.objects,{"id":product_id},{"add_to_set__options":product_varient_obj.id})
        else:
            print(">>>",1)
    data['status'] = True
    return data


@csrf_exempt
def obtainProductDetails(request):
    json_req = JSONParser().parse(request)
    product_id = ObjectId(json_req['id'])
    pipeline = [
    {
            "$match":{'_id':product_id}
        },
    {
        '$group': {
            "_id":None,
            'product_obj': {
                "$first": {
                    'product_name': "$product_name",
                    'product_id': "$_id",
                    'model':"$model",
                    'upc_ean':"$upc_ean",
                    'breadcrumb':"$breadcrumb",
                    'brand':"$brand",
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
        # result['product_obj']['ImageURL'] = result['product_obj']['ImageURL'][0] if len(result['product_obj']['ImageURL']) >0 else ""
        product_category_config_obj = DatabaseModel.get_document(product_category_config.objects,{"product_id":str(result['product_obj']['product_id'])})
        result['category_id'] = product_category_config_obj.category_id
        result['category_name'] = product_category_config_obj.category_level
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
    json_req = JSONParser().parse(request)
    product_id = json_req['id']
    print(".",json_req['update_obj'])
    json_req['update_obj']['base_price'] = str(json_req['update_obj']['base_price'])
    json_req['update_obj']['msrp'] = str(json_req['update_obj']['msrp'])
    DatabaseModel.update_documents(products.objects,{'id':product_id},json_req['update_obj'])
    data = dict()
    data['is_updated'] = True
    return data

@csrf_exempt
def varientBulkUpdate(request):
    json_req = JSONParser().parse(request)
    varient_obj_list = json_req['varient_obj_list']
    # for i in varient_obj_list:
    #     DatabaseModel.update_documents(Variants.objects,{'id':i['id']},i['update_obj'])
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


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook
from io import BytesIO

@csrf_exempt
def exportAll(request):
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
        },
       {
            "$group": {
                "_id": "$product_varient_ins._id",
                "model":{ "$first":"$model"},
                "upc_ean":{ "$first":"$upc_ean"},
                "product_name":{ "$first":"$product_name"},
                "category level":{ "$first":"$product_category_config_ins.category_level"},
                "long_description":{ "$first":"$long_description"},
                "short_description":{ "$first":"$short_description"}, 
                "brand":{ "$first":"$brand"},
                "breadcrumb":{ "$first":"$breadcrumb"},
                "msrp":{ "$first":"$msrp"},
                "base_price":{ "$first":"$base_price"},
                "Tags":{ "$first":"$tags"}, 
                "Variant SKU":{ "$first":"$product_varient_ins.sku_number"},
                "Un Finished Price":{ "$first":"$product_varient_ins.un_finished_price"},
                "Finished Price":{ "$first":"$product_varient_ins.finished_price"},
                "Image Src":{ "$first":"$product_varient_ins.image_url"},
                "Key Features":{ "$first":"$key_features"},
                "stockv":{ "$first":"$product_varient_ins.quantity"},
                "varient_option":{'$push':{'name':"$type_name.name","value":"$type_value.name"}}
        }
    } , {
            '$project': {
                "_id": 0,
                "model":1,
                "upc_ean":1,
                "category level":1,
                "product_name":1,
                "long_description":1,
                "short_description":1, 
                "brand":1,
                "breadcrumb":1,
                "msrp":1,
                "base_price":1,
                "Tags":1, 
                "Variant SKU":1,
                "Un Finished Price":1,
                "Finished Price":1,
                "Image Src":1, 
                "Image Position":1,
                "Key Features":1,
                "stockv":1,
                "varient_option":1
            }
        }
    
    ]
    result = list(products.objects.aggregate(*pipeline))
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Products"
    headers = [
    "S.No", "Model", "UPC/EAN", "Product Name", "Category Level", "Long Description", "Short Description",
    "Brand", "Breadcrumb", "MSRP", "Base Price", "Tags", "Variant SKU", "Unfinished Price", 
    "Finished Price", "Image Src", "Key Features", "Stock"
    ]

    # Add headers for variant options dynamically based on the number of variant options in the data
    variant_headers = []
    max_variants = 5
    for i in range(1, max_variants + 1):
        variant_headers.append(f"Variant {i} Name")
        variant_headers.append(f"Variant {i} Value")
    headers.extend(variant_headers)

    worksheet.append(headers)

    for i, item in enumerate(result):
        row = [
            i + 1,
            item.get("model", ""),
            item.get("upc_ean", ""),
            item.get("product_name", ""),
            item.get("category level", ""),
            item.get("long_description", ""),
            item.get("short_description", ""),
            item.get("brand", ""),
            item.get("breadcrumb", ""),
            item.get("msrp", ""),
            item.get("base_price", ""),
            item.get("Tags", ""),
            item.get("Variant SKU", ""),
            item.get("Un Finished Price", ""),
            item.get("Finished Price", ""),
            str(item.get("Image Src", "")),
            item.get("Key Features", ""),
            item.get("stockv", ""),
        ]

        # Extract variant options and add them to the row
        variant_options = item.get("varient_option", [])
        for j in range(max_variants):
            if j < len(variant_options):
                row.append(variant_options[j].get('name', ''))
                row.append(variant_options[j].get('value', ''))
            else:
                row.append('')  # Empty values for variants that don't exist

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

import pandas as pd
import pdfplumber
import pandas as pd

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
            i['type_id'] = str(i['type_id'])
            for j in i['option_value_list']:
                j['type_value_id'] = str(j['type_value_id']) if 'type_value_id'in j else ""
    data['varient_list'] = result
    return data

@csrf_exempt
def createVarientOption(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    category_varient_id = json_req.get("category_varient_id")
    category_id = json_req.get("category_id")
    if category_varient_id == "":
        category_varient_obj = DatabaseModel.save_documents(category_varient,{'category_id':category_id})
        category_varient_id = str(category_varient_obj.id)
    type_name_obj = DatabaseModel.get_document(type_name.objects,{'name':name})
    if type_name_obj:
        type_name_id = type_name_obj.id
        varient_option_obj = DatabaseModel.get_document(varient_option.objects,{'option_name_id':type_name_id})
        if varient_option_obj:
            varient_option_id = varient_option_obj.id
        else:
            varient_option_obj = DatabaseModel.save_documents(varient_option,{'option_name_id':type_name_id})
            varient_option_id = varient_option_obj.id
    else:
        type_name_id = DatabaseModel.save_documents(type_name,{'name':name})
        varient_option_id = DatabaseModel.save_documents(varient_option,{'option_name_id':type_name_id})
    DatabaseModel.update_documents(category_varient.objects,{"id":category_varient_id},{'add_to_set__varient_option_id_list':varient_option_id})
    data = dict()
    data['is_created'] = True
    return data

@csrf_exempt
def createValueForVarientName(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    option_id = json_req.get("option_id")
    type_value_obj = DatabaseModel.get_document(type_value.objects,{'name':name})
    if type_value_obj:
        type_value_id = type_value_obj.id
    else:
        type_value_id = DatabaseModel.save_documents(type_value,{'name':name})
    DatabaseModel.update_documents(varient_option.objects,{"option_name_id":option_id},{'add_to_set__option_value_id_list':type_value_id})
    data = dict()
    data['is_created'] = True
    return data

def obtainDashboardCount(request):
    data = dict()
    data['total_product'] = DatabaseModel.count_documents(products.objects,{})
    data['total_brand'] = 0
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
    data = dict()
    json_req = JSONParser().parse(request)
    product_id = json_req.get("product_id")
    category_id = json_req.get("category_id")
    category_name = json_req.get["category_name"]
    all_ids = ""
    if category_name == "level-1":
        category_obj = DatabaseModel.get_document(category.objects,{'id':category_id})
        if category_obj:
            all_ids = category_obj.name
            for i in category_obj.level_one_category_list:
                all_ids = all_ids  + ">"+ i.name 
                for j in i.level_two_category_list:
                    all_ids = all_ids + ">"+ j.name 
                    for k in j.level_three_category_list:
                        all_ids = all_ids + ">"+ k.name
                        for l in  k.level_four_category_list:
                            all_ids = all_ids + ">"+ l.name 
                            for m in  l.level_five_category_list:
                                all_ids = all_ids + ">"+ m.name 
    elif  category_name == "level-2":
        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'id':category_id})
        if level_one_category_obj:
            all_ids = level_one_category_obj.name
            for j in i.level_two_category_list:
                all_ids = all_ids + ">"+ j.name 
                for k in j.level_three_category_list:
                    all_ids = all_ids + ">"+ k.name
                    for l in  k.level_four_category_list:
                        all_ids = all_ids + ">"+ l.name 
                        for m in  l.level_five_category_list:
                            all_ids = all_ids + ">"+ m.name 

    elif  category_name == "level-3":
        level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'id':category_id})
        if level_two_category_obj:
            all_ids = level_two_category_obj.name
            for k in j.level_three_category_list:
                all_ids = all_ids + ">"+ k.name
                for l in  k.level_four_category_list:
                    all_ids = all_ids + ">"+ l.name 
                    for m in  l.level_five_category_list:
                        all_ids = all_ids + ">"+ m.name
    elif  category_name == "level-4":
        level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'id':category_id})
        if level_three_category_obj:
            all_ids = level_three_category_obj.name
            for l in  k.level_four_category_list:
                all_ids = all_ids + ">"+ l.name 
                for m in  l.level_five_category_list:
                    all_ids = all_ids + ">"+ m.name
    elif  category_name == "level-5":
        level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'id':category_id})
        if level_four_category_obj:
            all_ids = level_three_category_obj.name
            for m in  l.level_five_category_list:
                all_ids = all_ids + ">"+ m.name
    DatabaseModel.update_documents(product_category_config.objects,{'product_id':product_id},{'category_level':all_ids,"category_id":category_id})
    data['status'] = True
    return data

@csrf_exempt
def sampleData(request):
    pass

@csrf_exempt
def createAndAddVarient(request):
    data = dict()
    json_req = JSONParser().parse(request)
    product_id = json_req.get("product_id")
    varient_obj = json_req.get("varient_obj")
    product_varient_obj = DatabaseModel.save_documents(product_varient,{"sku_number":varient_obj['sku_number'],"finished_price":str(varient_obj['finished_price']),"un_finished_price":str(varient_obj['un_finished_price']),"quantity":varient_obj['quantity']})
    for i in varient_obj['options']:
        product_varient_option_obj = DatabaseModel.save_documents(product_varient_option,{"option_name_id":i['option_name_id'],"option_value_id":i['option_value_id']})
        DatabaseModel.update_documents(product_varient.objects,{"id":product_varient_obj.id},{"add_to_set__varient_option_id":product_varient_option_obj.id})
    DatabaseModel.update_documents(products.objects,{"id":product_id},{"add_to_set__options":product_varient_obj.id})
    data['status'] = True
    return data