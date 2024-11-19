from .global_service import DatabaseModel
from .models import category
from .models import level_one_category
from .models import level_two_category
from .models import level_three_category
from .models import level_four_category
from .models import level_five_category

def getCategoryLevelOrder(i):
    if i['level']=='level-1':
        i['category_name'] = DatabaseModel.get_document(category.objects,{'id':i['category_id']}).name
    elif i['level']=='level-2':
        i['category_name'] = DatabaseModel.get_document(level_one_category.objects,{'id':i['category_id']}).name
        # i['category_name'] = i['category_name'] + ">" +DatabaseModel.get_document(category.objects,{'level_one_category_list__in':[i['category_id']]}).name
        i['category_name'] = DatabaseModel.get_document(category.objects,{'level_one_category_list__in':[i['category_id']]}).name + ">"+i['category_name']
    elif i['level']=='level-3':
        i['category_name'] = DatabaseModel.get_document(level_two_category.objects,{'id':i['category_id']}).name
        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'level_two_category_list__in':[i['category_id']]})
        i['category_name'] =  level_one_category_obj.name + ">" + i['category_name']
        i['category_name'] = DatabaseModel.get_document(category.objects,{'level_one_category_list__in':[level_one_category_obj.id]}).name + ">" + i['category_name'] 
    elif i['level']=='level-4':
        i['category_name'] = DatabaseModel.get_document(level_three_category.objects,{'id':i['category_id']}).name
        level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'level_three_category_list__in':[i['category_id']]})
        i['category_name'] =  level_two_category_obj.name + ">" + i['category_name'] 
        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'level_two_category_list__in':[level_two_category_obj.id]})
        i['category_name'] =  level_one_category_obj.name + ">" + i['category_name'] 
        i['category_name'] = DatabaseModel.get_document(category.objects,{'level_one_category_list__in':[level_one_category_obj.id]}).name + ">" + i['category_name'] 
        
    elif i['level']=='level-4':
        
        i['category_name'] = DatabaseModel.get_document(level_four_category.objects,{'id':i['category_id']}).name
        level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'level_four_category_list__in':[i['category_id']]})
        i['category_name'] =  level_three_category_obj.name  + ">" + i['category_name']
        level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'level_three_category_list__in':[level_three_category_obj.id]})
        i['category_name'] =  level_two_category_obj.name + ">" + i['category_name'] 
        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'level_two_category_list__in':[level_two_category_obj.id]})
        i['category_name'] =  level_one_category_obj.name + ">" + i['category_name']
        i['category_name'] = DatabaseModel.get_document(category.objects,{'level_one_category_list__in':[level_one_category_obj.id]}).name  + ">" + i['category_name']
        
    elif i['level']=='level-6':
        i['category_name'] = DatabaseModel.get_document(level_five_category.objects,{'id':i['category_id']}).name
        level_four_category_obj = DatabaseModel.get_document(level_four_category.objects,{'level_five_category_list__in':[i['category_id']]})
        i['category_name'] =  level_three_category_obj.name  + ">" + i['category_name']
        level_three_category_obj = DatabaseModel.get_document(level_three_category.objects,{'level_four_category_list__in':[level_four_category_obj.id]})
        i['category_name'] = level_three_category_obj.name  + ">" + i['category_name']
        level_two_category_obj = DatabaseModel.get_document(level_two_category.objects,{'level_three_category_list__in':[level_three_category_obj.id]})
        i['category_name'] =level_two_category_obj.name + ">" +  i['category_name'] 
        level_one_category_obj = DatabaseModel.get_document(level_one_category.objects,{'level_two_category_list__in':[level_two_category_obj.id]})
        i['category_name'] =level_one_category_obj.name   + ">" +  i['category_name']
        i['category_name'] =DatabaseModel.get_document(category.objects,{'level_one_category_list__in':[level_one_category_obj.id]}).name + ">" + i['category_name'] 
        