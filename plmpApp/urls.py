

from django.urls import path
from .views import v1, create_user,createCategory,createCategory1, createCategory2,createCategory3,createCategory4,createCategory5,createProduct,deleteCategory, updateCategory,obtainCategoryAndSections, obtainAllProductList, upload_file, obtainProductDetails, productBulkUpdate, productUpdate, obtainAllVarientList, exportAll, retrieveData, varientBulkUpdate ,obtainVarientForCategory,createVarientOption,createValueForVarientName,obtainDashboardCount
from .authentication import loginUser,sendOtp,resetPassword

urlpatterns = [    
    path('v1/', v1, name='v1'), 
    path('list-users/', create_user, name='list_users'),
    path('list-users/', create_user, name='list_users'),
    #create
    path('loginUser/', loginUser, name='loginUser'), 
    path('sendOtp/', sendOtp, name='sendOtp'),
    path('resetPassword/', resetPassword, name='resetPassword'),

    
    path('createCategory1/', createCategory1, name='createCategory1'), 
    path('createCategory2/', createCategory2, name='createCategory2'), 
    path('createCategory3/', createCategory3, name='createCategory3'), 
    path('createCategory4/', createCategory4, name='createCategory4'), 
    path('createCategory5/', createCategory5, name='createCategory5'), 
    path('createProduct/', createProduct, name='createProduct'),
    #delete
    path('deleteCategory/', deleteCategory, name='deleteCategory'),
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
    path('obtainVarientForCategory/', obtainVarientForCategory, name='obtainVarientForCategory'),
    path('createVarientOption/', createVarientOption, name='createVarientOption'),
    path('createValueForVarientName/', createValueForVarientName, name='createValueForVarientName'),
    path('obtainDashboardCount/', obtainDashboardCount, name='obtainDashboardCount'),
    
    

]
