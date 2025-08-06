from django.urls import path

from api.v1.customer import views


urlspatterns = [
    path('login/', views.login),
    path('register/', views.register),
    path('address/', views.address),
    path('add_address/', views.add_address),
    path('update_address/<int:address_id>/', views.update_address),
    path('delete_address/<int:address_id>/', views.delete_address),
]