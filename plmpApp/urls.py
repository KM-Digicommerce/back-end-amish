

from django.urls import path
from .views import v1, create_user,createCategory,createSection, createProductType, deleteCategory, deleteSection, deleteProductType, updateCategory, updateSection, updateProductType, obtainCategoryAndSections, obtainAllProductList, upload_file, obtainProductDetails, productBulkUpdate, productUpdate, obtainAllVarientList, exportAll


urlpatterns = [
    path('v1/', v1, name='v1'), 
    path('list-users/', create_user, name='list_users'), 
    path('createCategory/', createCategory, name='createCategory'), 
    path('createSection/', createSection, name='createSection'), 
    path('createProductType/', createProductType, name='createProductType'), 
    path('deleteCategory/', deleteCategory, name='deleteCategory'), 
    path('deleteSection/', deleteSection, name='deleteSection'), 
    path('deleteProductType/', deleteProductType, name='deleteProductType'), 
    path('updateCategory/', updateCategory, name='updateCategory'), 
    path('updateSection/', updateSection, name='updateSection'), 
    path('updateProductType/', updateProductType, name='updateProductType'), 
    path('obtainCategoryAndSections/', obtainCategoryAndSections, name='obtainCategoryAndSections'), 
    path('obtainAllProductList/', obtainAllProductList, name='obtainAllProductList'), 
    path('upload_file/', upload_file, name='upload_file'), 
    path('obtainProductDetails/', obtainProductDetails, name='obtainProductDetails'), 
    path('productBulkUpdate/', productBulkUpdate, name='productBulkUpdate'), 
    path('productUpdate/', productUpdate, name='productUpdate'), 
    path('obtainAllVarientList/', obtainAllVarientList, name='obtainAllVarientList'), 
    path('exportAll/', exportAll, name='exportAll'), 
]
