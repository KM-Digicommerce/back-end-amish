
from django.http import JsonResponse
from .models import category
from .models import products
from .models import product_type
from .models import wood_type
from .models import Variants
from .models import varient_option
from .models import section
from .models import size_option
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
def createSection(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    category_id = json_req.get("category_id")
    section_obj = DatabaseModel.save_documents(section,{'name':name})
    DatabaseModel.update_documents(category.objects,{"id":category_id},{'add_to_set__section_list':section_obj.id})
    data = dict()
    data['is_created'] = True
    return data


@csrf_exempt
def createProductType(request):
    json_req = JSONParser().parse(request)
    name = json_req.get("name")
    section_id = json_req.get("section_id")
    product_type_obj = DatabaseModel.save_documents(product_type,{'name':name})
    DatabaseModel.update_documents(section.objects,{"id":section_id},{'add_to_set__product_type_list':product_type_obj.id})
    data = dict()
    data['is_created'] = True
    return data

#delete
@csrf_exempt
def deleteCategory(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    DatabaseModel.delete_documents(category,{'id':id})
    data = dict()
    data['is_deleted'] = True
    return data


@csrf_exempt
def deleteSection(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    DatabaseModel.delete_documents(section,{'id':id})
    data = dict()
    data['is_deleted'] = True
    return data


@csrf_exempt
def deleteProductType(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    DatabaseModel.delete_documents(product_type,{'id':id})
    data = dict()
    data['is_deleted'] = True
    return data

#update
@csrf_exempt
def updateCategory(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    name = json_req.get("name")
    DatabaseModel.update_documents(category,{'id':id},{'name':name})
    data = dict()
    data['is_updated'] = True
    return data


@csrf_exempt
def updateSection(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    name = json_req.get("name")
    DatabaseModel.update_documents(section,{'id':id},{'name':name})
    data = dict()
    data['is_updated'] = True
    return data


@csrf_exempt
def updateProductType(request):
    json_req = JSONParser().parse(request)
    id = json_req.get("id")
    name = json_req.get("name")
    DatabaseModel.update_documents(product_type,{'id':id},{'name':name})
    data = dict()
    data['is_updated'] = True
    return data

def obtainCategoryAndSections(request):
    
    pipeline = [
    {
        '$lookup': {
            "from": 'section',
            "localField": 'section_list',
            "foreignField": "_id",
            "as": "section_ins"
        }
    },  {
        '$unwind': {
            'path': '$section_ins',
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$lookup': {
            "from": 'product_type',
            "localField": 'section_ins.product_type_list',
            "foreignField": "_id",
            "as": "product_type_ins"
        }
    }, {
        '$unwind': {
            'path': '$product_type_ins',
            'preserveNullAndEmptyArrays': True
        }
    },
    {
        '$group': {
            "_id": {
                'category_id': "$_id", 
                "name":"$name",
                'section_name': "$section_ins.name",
                'section_id': "$section_ins._id"
            },
            'product_type_list': {
                "$push": {
                    'name': "$product_type_ins.name",
                    'id': "$product_type_ins._id"
                }
            }
        }
    },
    {
        '$group': {
            "_id": "$_id.category_id",
            "name":{'$first':"$_id.name"},
            'sections': {
                "$push": {
                    'section_name': "$_id.section_name",
                    'section_id': "$_id.section_id",
                    'product_types': "$product_type_list"
                }
            }
        }
    },
    {
        '$project': {
            'category_id':"$_id",
            'name': "$name",
            'sections': 1  ,
            "_id":0
        }
    }
    ]
    result = list(category.objects.aggregate(*pipeline))
    result = sorted(result, key=lambda x: x['category_id'])
    for i in result:
        if 'category_id':
            i['category_id'] = str(i['category_id']) 
            for j in i['sections']:
                if 'section_id'in j :
                    j['section_id'] = str(j['section_id']) 
                    for k in j['product_types']:
                        if 'id'in k:
                            k['id'] = str(k['id']) 
    return result


@csrf_exempt
def obtainAllProductList(request):
    # json_req = JSONParser().parse(request)
    product_type_id = request.POST.get("id")
    if product_type_id:
        product_type_id = {'product_type_id':ObjectId(product_type_id)}
    else:
        product_type_id = {}
    pipeline = [
    {
            "$match":product_type_id
        },
    {
        '$group': {
            "_id":None,
            'product_list': {
                "$push": {
                    'product_name': "$product_name",
                    'product_id': "$_id",
                    'url':"$ImageURL",
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
            if i['name'] =="Wood Type":
                wood_type_obj = DatabaseModel.get_document(wood_type.objects,{"name":i['value']})
                if wood_type_obj:
                    option_value_id = wood_type_obj.id
                else:
                    wood_type_obj = DatabaseModel.save_documents(wood_type,{'name':i['value']})
                    option_value_id = wood_type_obj.id
            if i['name'] =="Size":
                size_option_obj = DatabaseModel.get_document(size_option.objects,{"name":i['value']})
                if size_option_obj:
                    option_value_id = size_option_obj.id
                else:
                    size_option_obj = DatabaseModel.save_documents(size_option,{'name':i['value']})
                    option_value_id = size_option_obj.id
            Variants_opt_obj = DatabaseModel.save_documents(varient_option,{'varient_count':0,"option_name":i['name'],'option_value_id':str(option_value_id)})
            Variants_opt_id_list.append(Variants_opt_obj.id)
        if isinstance(product_image, str):
            DatabaseModel.save_documents(Variants,{'product_id':product_obj.id,"options":Variants_opt_id_list,"varient_sku":varient_sku,"unfinished_price":0,"finished_price":variant_Price,"image_url":product_image})
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
    for i in varient_obj_list:
        DatabaseModel.update_documents(Variants.objects,{'id':i['id']},i['update_obj'])
    data = dict()
    data['is_updated'] = True
    return data

@csrf_exempt
def obtainAllVarientList(request):
    json_req = JSONParser().parse(request)
    product_id = ObjectId(json_req['id'])
    pipeline = [
        {
            "$match": {'product_id': product_id}
        },
        {
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
                "name": { "$first": "$name" },
                "varient_sku": { "$first": "$varient_sku" },
                "unfinished_price": { "$first": "$unfinished_price" },
                "finished_price": { "$first": "$finished_price" },
                "varient_code": { "$first": "$varient_code" },
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
        },
        {
            '$unwind': "$options" 
        },
        {
            '$project': {
                "id": "$_id",
                "_id": 0,
                "name": 1,
                "varient_sku": 1,
                "unfinished_price": 1,
                "finished_price": 1,
                "varient_code": 1,
                "options": 1
            }
        }
    ]
    result = list(Variants.objects.aggregate(*pipeline))
    option_dict = dict()
    if len(result)>0:
        for Variant_obj in result:
            Variant_obj['id'] = str(Variant_obj['id'])
            for i in Variant_obj['options']:
                if i['option_name'] == "Wood Type":
                    if str(i['option_value']) in option_dict:
                        i['option_value'] = option_dict[str(i['option_value'])]
                    else:
                        wood_type_obj = DatabaseModel.get_document(wood_type.objects,{'id':i['option_value']})
                        option_dict[str(i['option_value'])] = wood_type_obj.name
                        i['option_value'] = wood_type_obj.name
                if i['option_name'] == "Size":
                    if str(i['option_value']) in option_dict:
                        i['option_value'] = option_dict[str(i['option_value'])]
                    else:
                        size_option_obj = DatabaseModel.get_document(size_option.objects,{'id':i['option_value']})
                        option_dict[str(i['option_value'])] = size_option_obj.name
                        i['option_value'] = size_option_obj.name
    return  result


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
                "Vendor": { "$first": "$product_ins.Manufacturer_name" },
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
    result = list(Variants.objects.aggregate(*pipeline))
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
