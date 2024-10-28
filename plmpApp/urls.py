

from django.urls import path
from .views import v1, create_user,createCategory,createCategory1, createCategory2,createCategory3,createCategory4,createCategory5,deleteCategory, deleteCategory1, deleteCategory2,deleteCategory3,deleteCategory4,deleteCategory5, updateCategory,obtainCategoryAndSections, obtainAllProductList, upload_file, obtainProductDetails, productBulkUpdate, productUpdate, obtainAllVarientList, exportAll, retrieveData, varientBulkUpdate


urlpatterns = [
    path('v1/', v1, name='v1'), 
    path('list-users/', create_user, name='list_users'), 
    #create
    path('createCategory/', createCategory, name='createCategory'), 
    path('createCategory1/', createCategory1, name='createCategory1'), 
    path('createCategory2/', createCategory2, name='createCategory2'), 
    path('createCategory3/', createCategory3, name='createCategory3'), 
    path('createCategory4/', createCategory4, name='createCategory4'), 
    path('createCategory5/', createCategory5, name='createCategory5'), 
    #delete
    path('deleteCategory/', deleteCategory, name='deleteCategory'), 
    path('deleteCategory1/', deleteCategory1, name='deleteCategory1'), 
    path('deleteCategory2/', deleteCategory2, name='deleteCategory2'),
    path('deleteCategory3/', deleteCategory3, name='deleteCategory3'),
    path('deleteCategory4/', deleteCategory4, name='deleteCategory4'),
    path('deleteCategory5/', deleteCategory5, name='deleteCategory5'),
    #update
    path('updateCategory/', updateCategory, name='updateCategory'),

    path('obtainCategoryAndSections/', obtainCategoryAndSections, name='obtainCategoryAndSections'), 
    path('obtainAllProductList/', obtainAllProductList, name='obtainAllProductList'), 
    path('upload_file/', upload_file, name='upload_file'), 
    path('obtainProductDetails/', obtainProductDetails, name='obtainProductDetails'), 
    path('productBulkUpdate/', productBulkUpdate, name='productBulkUpdate'), 
    path('productUpdate/', productUpdate, name='productUpdate'), 
    path('obtainAllVarientList/', obtainAllVarientList, name='obtainAllVarientList'), 
    path('exportAll/', exportAll, name='exportAll'), 
    path('retrieveData/', retrieveData, name='retrieveData'),
    path('varientBulkUpdate/', varientBulkUpdate, name='varientBulkUpdate'),
]
