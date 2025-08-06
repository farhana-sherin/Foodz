from django.urls import path
from web import views



app_name='web'

urlpatterns = [
    path("",views.index,name="index"),
    path("login/",views.login,name="login"),
    path("register/",views.register,name="register"),
    path("logout/",views.logout,name="logout"),
    path("restaurent/<int:id>/",views.restaurent,name="restaurent"),
    path("single_rest/<int:id>/",views.single_rest,name="single_rest"),
    path("account/",views.account,name="account"),
    path("offers/",views.offers,name="offers"),
    path("cart/",views.cart,name="cart"),
    path('add_address/', views.add_address, name='add_address'),
    
    path('address/', views.address, name='address'),
    path('address_edit/<int:id>/',views.address_edit,name="address_edit"),
    path('address_delete/<int:id>/',views.address_delete,name="address_delete"),
    path("checkout/",views.checkout,name="checkout"),

    path('add_fooditem/<int:id>/',views.add_fooditem,name='add_fooditem'),
    path('inc_fooditem/<int:id>/',views.inc_fooditem,name='inc_fooditem'),
    path('decr_fooditem/<int:id>/',views.decr_fooditem,name='decr_fooditem'),
    path('cart_inc_fooditem/<int:id>/',views.cart_inc_fooditem,name='cart_inc_fooditem'),
    path('cart_decr_fooditem/<int:id>/',views.cart_decr_fooditem,name='cart_decr_fooditem'),
    path('address_select/<int:id>/',views.address_select,name='address_select'),
    path('offerapply/<int:id>/',views.offerapply,name='offerapply'),
    path('orders/',views.orders,name='orders'),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('track/<int:id>/',views.track,name='track'),


    





    
    



]



