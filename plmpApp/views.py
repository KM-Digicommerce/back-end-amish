
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

def v1(request):
    return JsonResponse({"PLMP_API":"v2"},safe=False)
def create_user(request):
    json_request = json.loads(request.body)
    categories_data = json_request.get('categories')

    category_objects = []
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
    print(name, section_id )
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
    name = json_req.get("name")
    category_id = json_req.get("category_id")
    category_name = json_req.get("category_name")
    products_obj = DatabaseModel.save_documents(products,{'product_name':name})
    products_obj = DatabaseModel.save_documents(product_category_config,{'product_id':products_obj.id,'category_level':category_name,"category_id":category_id})
    data = dict()
    data['is_created'] = True
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
            "level_one_category_list": []  
        }

        level_two_map = {level_two['_id']: level_two for level_two in entry.get('level_two_category', [])}

        for level_one in entry.get('level_one_category', []):
            level_one_entry = {
                "_id": level_one['_id'],
                "name": level_one['name'],
                "level_two_category_list": []  
            }
            for level_two_id in level_one.get('level_two_category_list', []):
                level_two = level_two_map.get(level_two_id)
                if level_two:
                    level_two_entry = {
                        "_id": level_two['_id'],
                        "name": level_two['name'],
                        "level_three_category_list": []
                    }
                    level_three_map = {level_three['_id']: level_three for level_three in entry.get('level_three_category', [])}

                    for level_three_id in level_two.get('level_three_category_list', []):
                        level_three = level_three_map.get(level_three_id)
                        if level_three:
                            level_three_entry = {
                                "_id": level_three['_id'],
                                "name": level_three['name'],
                                "level_four_category_list": [] 
                            }
                            level_four_map = {level_four['_id']: level_four for level_four in entry.get('level_four_category', [])}

                            for level_four_id in level_three.get('level_four_category_list', []):
                                level_four = level_four_map.get(level_four_id)
                                if level_four:
                                    level_four_entry = {
                                        "_id": level_four['_id'],
                                        "name": level_four['name'],
                                        "level_five_category_list": [] 
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
                            level_two_entry['level_three_category_list'].append(level_three_entry) 
                    level_one_entry['level_two_category_list'].append(level_two_entry) 

            category_entry['level_one_category_list'].append(level_one_entry) 

        transformed_result.append(category_entry) 

    result = sorted(transformed_result, key=lambda x: x['_id'])


    convert_object_ids_to_strings(result)  
    return result


@csrf_exempt
def obtainAllProductList(request):
    category_id = request.POST.get("id")
    if category_id:
        category_obj = {'category_id':category_id}
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
                    'url':"$products.ImageURL",
                    "Manufacturer_name":"$products.Manufacturer_name",
                    "tags":"$products.tags",
                    "BasePrice":"$products.BasePrice",
                    "Key_features":"$products.Key_features"
                }
            }
        }
    }
    ]
    result = list(product_category_config.objects.aggregate(*pipeline))
    if len(result)>0:
        result = result[0]
        del result['_id']
        for j in result['product_list']:
            j['product_id'] = str(j['product_id']) if 'product_id'in j else ""
    return  result


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
    l = list()
    for i in range(len(df)):
        row_dict = df.iloc[i].to_dict()
        Handle = row_dict['Handle']
        Title = row_dict['Title']
        Vendor = row_dict['Vendor']
        category_string = row_dict['Product Category']
        Tags = row_dict['Tags']
        KeyFeatures = row_dict['Key Features (product.metafields.custom.key_features1)']
        options = []
        product_image = row_dict['Image Src']
        if isinstance(Title, str) == False:
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
        product_obj = DatabaseModel.get_document(products.objects,{"Handle":Handle})
        if product_obj==None:
            category_list = []
            if isinstance(category_string, str):
                category_list = [item.strip() for item in category_string.split('>')]
            product_type_obj = DatabaseModel.get_document(product_type.objects,{"name":category_list[2]})
            if product_type_obj== None:
                product_type_obj = DatabaseModel.save_documents(product_type,{'name':category_list[2]})
            section_obj = DatabaseModel.get_document(section.objects,{"name":category_list[1]})
            if section_obj== None:
                section_obj = DatabaseModel.save_documents(section,{'name':category_list[1],'product_type_list':[product_type_obj.id]})
            category_obj = DatabaseModel.get_document(category.objects,{"name":category_list[0]})
            if category_obj== None:
                category_obj = DatabaseModel.save_documents(category,{'name':category_list[0],'section_list':[section_obj.id]})
            if product_obj == None:
                product_obj = DatabaseModel.save_documents(products,{'product_name':Title,"Handle":Handle,"product_type_id":product_type_obj.id,"Manufacturer_name":Vendor,"tags":Tags,"Key_features":KeyFeatures,"ImageURL":[product_image]})
        else:
            if isinstance(product_image, str):
                DatabaseModel.update_documents(products.objects,{"id":product_obj.id},{"push__ImageURL":product_image})
        varient_sku = row_dict['Variant SKU']
        variant_Price = row_dict['Variant Price']
        Variants_opt_id_list = list()
        for i in options:
            option_value_id = ""
            # if i['name'] =="Wood Type":
            #     # wood_type_obj = DatabaseModel.get_document(wood_type.objects,{"name":i['value']})
            #     if wood_type_obj:
            #         option_value_id = wood_type_obj.id
            #     else:
            #         # wood_type_obj = DatabaseModel.save_documents(wood_type,{'name':i['value']})
            #         option_value_id = wood_type_obj.id
            # if i['name'] =="Size":
            #     # size_option_obj = DatabaseModel.get_document(size_option.objects,{"name":i['value']})
            #     if size_option_obj:
            #         option_value_id = size_option_obj.id
            #     else:
            #         # size_option_obj = DatabaseModel.save_documents(size_option,{'name':i['value']})
            #         option_value_id = size_option_obj.id
            Variants_opt_obj = DatabaseModel.save_documents(varient_option,{'varient_count':0,"option_name":i['name'],'option_value_id':str(option_value_id)})
            Variants_opt_id_list.append(Variants_opt_obj.id)
    #     if isinstance(product_image, str):
    #         DatabaseModel.save_documents(Variants,{'product_id':product_obj.id,"options":Variants_opt_id_list,"varient_sku":varient_sku,"unfinished_price":0,"finished_price":variant_Price,"image_url":product_image})
    # data['status'] = True
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
                    'ImageURL':"$ImageURL",
                    "Manufacturer_name":"$Manufacturer_name",
                    "tags":"$tags",
                    "BasePrice":"$BasePrice",
                    "Key_features":"$Key_features"
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
        result['product_obj']['ImageURL'] = result['product_obj']['ImageURL'][0] if len(result['product_obj']['ImageURL']) >0 else ""
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
    return  product_id


@csrf_exempt
def exportAll(request):
    pipeline = [
        {
            '$lookup': {
                "from": 'products',
                "localField": 'product_id',
                "foreignField": "_id",
                "as": "product_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, 
        {
            '$lookup': {
                "from": 'product_type',
                "localField": 'product_ins.product_type_id',
                "foreignField": "_id",
                "as": "product_type_ins"
            }
        },
        {
            '$unwind': {
                'path': '$product_type_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                "from": 'section',
                "localField": 'product_type_ins._id',
                "foreignField": "product_type_list",
                "as": "section_ins"
            }
        },
        {
            '$unwind': {
                'path': '$section_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                "from": 'category',
                "localField": 'section_ins._id',
                "foreignField": "section_list",
                "as": "category_ins"
            }
        },
        {
            '$unwind': {
                'path': '$category_ins',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$lookup': {
                "from": 'varient_option',
                "localField": 'options',
                "foreignField": "_id",
                "as": "varient_option_ins"
            }
        },
   {
            "$group": {
                "_id": "$_id",
                "Variant SKU": { "$first": "$varient_sku" },
                "Variant Price": { "$first": "$finished_price" },
                "Image Src": { "$first": "$ImageURL" },
                "Handle": { "$first": "$product_ins.Handle" },
                "Title": { "$first": "$product_ins.product_name" },
                "Manufacturer_name": { "$first": "$product_ins.Manufacturer_name" },
                "Tags": { "$first": "$product_ins.tags" },
                "Key_features": { "$first": "$product_ins.Key_features" },
                "Product Category": {
            "$first": {
                "$concat": [
                    "$category_ins.name", " > ", "$section_ins.name", " > ", "$product_type_ins.name"
                ]
            }
        },
                "options": {
                    "$push": {
                        "$map": {
                            "input": "$varient_option_ins",
                            "as": "option",
                            "in": {
                                "option_name": "$$option.option_name",
                                "option_value": "$$option.option_value"
                            }
                        }
                    }
                }
            }
        },  {
            '$project': {
                "_id": 0,
                "Variant SKU": 1,
                "Variant Price": 1,
                "Image Src": 1, 
                "Handle": 1,
                "Title": 1,
                "Vendor": 1,
                "Tags": 1,
                "Key_features": 1,
                "options":1,
                "Product Category":1
            }
        }
    ]
    result = list(products.objects.aggregate(*pipeline))
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Products"

    headers = [
        "S.No","Handle", "Title","Vendor", "Tags", "Product Category", "Key_features","Variant SKU", "Variant Price", "Image Src", "Options"
    ]
    worksheet.append(headers)

    for i,item in enumerate(result):
        options_str = ""
        # options_str = '; '.join([
        #     f"{opt['option_name']}: {opt['option_value']}" 
        #     for opt in item.get('options', [])
        # ])
        row = [
            i+1,
            item["Handle"], 
            item["Title"], 
            item["Vendor"], 
            item["Tags"], 
            item["Product Category"], 
            item["Key_features"], 
            item["Variant SKU"], 
            item["Variant Price"], 
            item["Image Src"], 
            options_str
        ]
        worksheet.append(row)

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)  

    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="products.xlsx"'
    
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

            # Create a dictionary to hold the JSON data for each sheet
            all_sheets_json = {}

            # Iterate through the sheets and convert each to JSON
            for sheet_name, df in sheets_dict.items():
                # Convert DataFrame to JSON
                json_data = df.to_json(orient='records')
                
                # Store the JSON data for the current sheet
                all_sheets_json[sheet_name] = json_data

            # Print or save the JSON data for all sheets
            print(all_sheets_json)
            with open('sheets_output.json', 'w') as json_file:
                json.dump(all_sheets_json, json_file)
        elif file.name.endswith('.csv'):
            df = pd.read_csv(file)

            json_data = df.to_json(orient='records')

            print(json_data)
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
    print(category_id)
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
    if category_varient_id == None:
        category_varient_obj = DatabaseModel.save_documents(category_varient,{'category_id':category_id})
        category_varient_id = str(category_varient_obj.id)
    type_name_obj = DatabaseModel.get_document(type_name.objects,{'name':name})
    if type_name_obj:
        type_name_id = type_name_obj.id
    else:
        type_name_id = DatabaseModel.save_documents(type_name,{'name':name})
    varient_option_id = DatabaseModel.save_documents(varient_option,{'option_name_id':type_name_id})
    DatabaseModel.update_documents(category_varient.objects,{"id":category_varient_id},{'add_to_set__varient_option_id_list':varient_option_id})
    data = dict()
    data['is_created'] = True
    return data

def createValueForVarientName(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    type_value_id = json_req.get("type_value_id")
    type_value_obj = DatabaseModel.get_document(type_value.objects,{'name':name})
    if type_value_obj:
        type_value_id = type_value_obj.id
    else:
        type_value_id = DatabaseModel.save_documents(type_value,{'name':name})
    DatabaseModel.update_documents(varient_option.objects,{"option_name_id":type_value_id},{'add_to_set__option_value_id_list':type_value_id})
    data = dict()
    data['is_created'] = True
    return data
