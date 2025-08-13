from django.urls import path

from api.v1.customer import views
app_name = 'customer'


urlpatterns = [
    path('login/', views.login,name='login'),
    path('register/', views.register ,name='register'),
    path('address/', views.address, name='address'),
    path('address/add/', views.add_address, name='add_address'),
    path('update_address/<int:id>/', views.update_address, name='update_address'),
    path('delete_address/<int:id>/', views.delete_address, name='delete_address'),
    path('account/', views.account, name='account'),
    path('offers/', views.offers, name='offers'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:id>/', views.add_fooditem, name='add_fooditem'),
    path('increase_fooditem/<int:id>/', views.inc_fooditem, name='inc_fooditem'),
    path('decrease_fooditem/<int:id>/', views.dec_fooditem, name='dec_fooditem'),
    path('address_select/<int:id>/', views.address_select, name='address_select'),
    path('offerapply/<int:id>/', views.offerapply, name='offerapply'),
    path('order/', views.order, name='order'),
    path('placeorder/', views. placeorder, name='placeorder'),
    path('track/<int:id>/', views.track, name='track'),
    path('restaurent/<int:id>/', views.restaurent, name='restaurent'),
    path('single_rest/<int:id>/', views.single_rest, name='single_rest'),
    path('logout/', views.logout, name='logout'),
    path("checkout/",views.checkout,name="checkout"),
 
]