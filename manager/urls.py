from django.urls import path
from manager import views


app_name='manager'

urlpatterns = [
     path("",views.index,name="index"), 
     path("store/categories/",views.store_categories,name="store_categories"),
     path("store/categories/add/",views.store_categories_add,name="store_categories_add"),
     path("store/categories/update/<int:id>/",views.store_categories_update,name="store_categories_update"),
     path("store/categories/delete/<int:id>/",views.store_categories_delete,name="store_categories_delete"),
     path("store", views.store, name="store"),
     path('stores/add/', views.add_store, name='add_store'),
     path('stores/edit/<int:id>/', views.edit_store, name='edit_store'),
     path('stores/delete/<int:id>/', views.delete_store, name='delete_store'),
     
     path("store",views.store,name="store"),
     path("store_managers",views.store_managers,name="store_managers"),
     path("orders",views.orders,name="orders"),
     
     path("food/category/",views.food_category,name="food_category"),
     path("food/category/add/",views.add_foodcategory,name="add_foodcategory"),
     path("food/category/edit/<int:id>/",views.edit_foodCategory,name="edit_foodCategory"),
     path("food/category/delete/<int:id>/",views.delete_foodCategory,name="delete_foodCategory"),
     path("food/item/",views.fooditem,name="fooditem"),
     path('fooditems/add/', views.add_fooditem, name='add_fooditem'),
     path('fooditems/edit/<int:id>/', views.edit_fooditem, name='edit_fooditem'),
     path('fooditems/delete/<int:id>/', views.delete_fooditem, name='delete_fooditem'),
     path('profile/', views.profile, name='profile'),
     path('logout/', views.logout, name='logout'),
     path('currentOrder/<int:id>/', views.currentOrder, name='currentOrder'),









     

   
     





     




    

     
]