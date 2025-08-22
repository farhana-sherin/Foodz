
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.shortcuts import render,reverse
from customer.models import Customer, Address, Cart, CartBill, FoodItem, Offers
from users.models import User
from api.v1.customer.serializers import *
from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from django.db.models import Sum
from restaurent.models import *
from django.http import HttpResponseRedirect








@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    
    email = request.data.get('email')
    password = request.data.get('password')

    user=authenticate(email=email, password=password)
    if user:
        refresh= RefreshToken.for_user(user)
        response_data = {
            "status_code": 6000,
            "data": {
                "access": str(refresh.access_token),
            },
            "message": "Login successful"
        }
    else:
        response_data = {
            "status_code": 6000,
            
            "message": "Invalid credentials"
        }
    return Response(response_data)
    





@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if User.objects.filter(email=email).exists():
        response_data = {
            "status_code": 6001,
            "data": {},
            "message": "User already exists"

        }
        return Response(response_data)
   
    user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
    user.save()

        

    customer = Customer.objects.create(
            user=user,
            )
    customer.save()
        

        
    refersh = RefreshToken.for_user(user)
    response_data = {
            "status_code": 6000,
            "data": {
                "access": str(refersh.access_token),
            },
            "message": "Registration successful"
        }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def address(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    addresses = Address.objects.filter(customer=customer)

    context = {
        "request": request,
    }
    serializer = AddressSerializer(addresses,many=True,context=context)

    response_data = {
        "status_code": 6000,
        "data": serializer.data,
        "message": "Address List",
    }
    return Response(response_data)
    

@api_view(['POST'])
@permission_classes([AllowAny])
def add_address(request):
    user = request.user
    customer =Customer.objects.get(user=user)

    address = request.data.get('Address')
    appartment = request.data.get('Appartment')
    landmark = request.data.get('landmark')
    address_type = request.data.get('address_type')

    address = Address.objects.create(
        customer=customer,
        address=address,
        appartment=appartment,
        landmark=landmark,
        address_type=address_type
    )
    address.save()
    response_data = {
        "status_code": 6000,
        
        "message": "Address added successfully"
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def index(request):
    store_categories = StoreCategory.objects.all()
    stores = Store.objects.all()
    sliders = Slider.objects.all()

    response_data = {
        "status_code": 6000,
        "data": {
            "store_categories": StoreCategorySerializer(store_categories, many=True).data,
            "stores": StoreSerializer(stores, many=True).data,
            "sliders": SliderSerializer(sliders, many=True).data
        },
        "message": "successfully retrieved"
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([AllowAny])
def store(request):
    store = Store.objects.all()
    context = {"request": request}

    response_data = {
        "status_code": 6000,
        "data": {
            "store": StoreSerializer(store, many=True, context=context).data
        },
        "message": "Successfully retrieved"
    }
    return Response(response_data)



@api_view(['GET'])
@permission_classes([AllowAny])
def slider(request):
    sliders = Slider.objects.all()
    context = {
        "request": request
    }
    response_data = {
        "status_code": 6000,
        "data": {
            "sliders": SliderSerializer(sliders, many=True, context=context).data
        },
        "message": "successfully retrieved"
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def store_categories(request):
    store_categories = StoreCategory.objects.all()
    context = {
        "request": request
    }
    response_data = {
        "status_code": 6000,
        "data": {
            "store_categories": StoreCategorySerializer(store_categories, many=True , context=context).data
        },
        "message": "successfully retrieved"
    }
    return Response(response_data)

    
  

@api_view(['PUT'])
@permission_classes([AllowAny])
def update_address(request,id):
    user = request.user
    customer= Customer.objects.get(user=user)
    form= Address.objects.get(id=id, customer=customer)

    address=request.data.get('Address')
    appartment = request.data.get('Appartment')
    landmark = request.data.get('landmark')
    address_type = request.data.get('address_type')

    form.address = address
    form.appartment = appartment
    form.landmark = landmark
    form.address_type = address_type

    form.save()

    response_data = {
        "status_code": 6000,
        
        "message": "Address updated successfully"
    }
    return Response(response_data)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_address(request,id):
    address = Address.objects.get(id=id)
    address.delete()

    response_data = {
        "status_code": 6000,
        
        "message": "Address deleted successfully"
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def account(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    order_count = Order.objects.filter(customer=customer).count()
    order = Order.objects.filter(customer=customer).order_by('-id')[:5]

    item_count = []

    for order in order:
        count = OrderItem.objects.filter(order=order).count()

        item_count.append({
            'order': order,
            'count': count,
            'order_count': order_count,
        })

    response_data = {
        "status_code": 6000,
        "message": "Account details retrieved successfully"
    }

    return Response(response_data)



@api_view(['GET'])
@permission_classes([AllowAny])
def offers(request):
    
    offer=Offers.objects.all()

    response_data = {
        "status_code": 6000,
        "data": {
            "offers": [
                {
                    "offer": offer.offer,
                    "code": offer.code,
                    "description": offer.description,
                    "is_percentage": offer.is_pecentage
                } for offer in offer
            ]
        },
        
    "message": "Offers retrieved successfully"
    }
    return Response(response_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    store = carts.first().store if carts.exists() else None
    addresses = Address.objects.filter(customer=customer)
    itemtotal = carts.aggregate(Sum('amount'))['amount__sum'] or 0

    selected_address = None
    for address in addresses:
        if address.is_selected:
            selected_address = address
            

    cartbill, _ = CartBill.objects.get_or_create(customer=customer)

    error = None
    Coupencode = request.query_params.get('CouponCode')
    if Coupencode:
        matched = False
        for offer in Offers.objects.all():
            if Coupencode == offer.code:
                matched = True
                if offer.is_pecentage:
                    cartbill.offer_amount = itemtotal * (offer.offer / 100)
                    cartbill.coupe_code=Coupencode
                    cartbill.save()
                else:
                    cartbill.offer_amount = offer.offer
                cartbill.coupe_code = Coupencode
                cartbill.save()
                
        if not matched:
            error = "Invalid Coupon Code"

    topay = itemtotal - cartbill.offer_amount - cartbill.delivery_charge

    response_data = {
        "status_code": 6000,
        "data": {
            "cart": CartSerializer(carts, many=True).data,
            "store": StoreSerializer(store).data if store else None,
            "addresses": AddressSerializer(addresses, many=True).data,
            "cart_bill": CartBillSerializer(cartbill).data,
            "item_total": itemtotal,
            "topay": topay,
            "error": error
        },
        "message": "Cart details retrieved successfully"
    }
    return Response(response_data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_fooditem(request , id):
    user=request.user
    customer=Customer.objects.get(user=user)
    fooditem=FoodItem.objects.get(id=id)
    store=fooditem.store
    carts=Cart.objects.filter(customer=customer)
    for cart in carts:
        if not store == cart.store :
            cart.delete()

  

    cart=Cart.objects.create(
        customer=customer,
        store=store,
        item=fooditem,
        amount=fooditem.price,
        quantity=1,
    )



    cart.save()
    response_data = {
        "status_code": 6000,
        "data": {
            "cart": CartSerializer(cart).data

        },
        "message": "Food item added to cart successfully"
        
    }
    return Response(response_data)


@api_view(['PUT'])  
@permission_classes([IsAuthenticated])  
def inc_fooditem(request, id):
    fooditem= FoodItem.objects.get(id=id)
    cart = Cart.objects.get(item=fooditem)
   

    
   
    

    fooditem_price = cart.item.price
    store= cart.store



    cart.quantity += 1
    cart.amount += fooditem_price
    cart.save()

    response_data = {

        "status_code": 6000,
        "data": {
           
        

            
        },
        "message": "Food item quantity increased successfully"
    }
    return Response(response_data)

@api_view(['PUT'])  
@permission_classes([IsAuthenticated])
def dec_fooditem(request, id):
    fooditem= FoodItem.objects.get(id=id)
    cart = Cart.objects.get(item=fooditem)
    fooditem_price = cart.item.price
    store= cart.store

    cart.quantity -= 1
    cart.amount -= fooditem_price
    cart.save()

    response_data = {

        "status_code": 6000,
        "data": {
           
        },
        "message": "Food item quantity decreased successfully"
    }
    return Response(response_data)

@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def address_select(request,id):
    user=request.user
    customer=Customer.objects.get(user=user)
    addresses=Address.objects.filter(customer=customer)
    selected_address=Address.objects.get(id=id)
    for address in addresses:
        if address == selected_address:
            address.is_selected=True

            address.save()

        else:

            address.is_selected=False

            address.save()

    response_data = {

        "status_code": 6000,
        "data": {
           
        },
        "message": "Address selected successfully"
    }
    return Response(response_data)


@api_view(['GET'])  
@permission_classes([IsAuthenticated])

def offerapply(request,id):
    user=request.user
    customer=Customer.objects.get(user=user)
    offers=Offers.objects.get(id=id)
    carts=Cart.objects.filter(customer=customer)
    cartbill=CartBill.objects.get(customer=customer)
    itemtotal=carts.aggregate(Sum('amount'))['amount__sum']

    if offers.is_pecentage:
            cartbill.offer_amount=itemtotal*(offers.offer/100)
            cartbill.coupe_code=offers.code
            cartbill.save()
    else:
            cartbill.offer_amount=(offers.offer)
            cartbill.coupe_code=offers.code
            cartbill.save()

    response_data = {

        "status_code": 6000,
        "data": {
           
        },
        "message": "Offer applied successfully"
    }
    return Response(response_data)


@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def order(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    orders = Order.objects.filter(customer=customer)

    item_count = []
    for order in orders:
        count = OrderItem.objects.filter(order=order).count()
        item_count.append({
            'order': OrderSerializer(order).data,  # or 'order_id': order.id
            'count': count,
        })

    response_data = {
        "status_code": 6000,
        "data": {
            "orders": OrderSerializer(orders, many=True).data,
            "item_count": item_count,
        },
        "message": "Order retrieved successfully"
    }
    return Response(response_data)


@api_view(['POST'])  
@permission_classes([IsAuthenticated])
def placeorder(request):
   
    user = request.user
    customer = Customer.objects.get(user=user)
    addrs = Address.objects.filter(customer=customer)
    cartbill = CartBill.objects.get(customer=customer)
    carts = Cart.objects.filter(customer=customer)
    
    subtotal = carts.aggregate(Sum('amount'))['amount__sum'] or 0
    offer_amount = cartbill.offer_amount or 0
    total = subtotal - offer_amount

    address = None
    for addr in addrs:
        if addr.is_selected:
            address = addr

    store = None
    for cart in carts:
        store = cart.store

    previous = Order.objects.filter(customer=customer).first()

    if previous:
        order_id = f'ORD000{previous.id + 1}'
    else:
        order_id = 'ORD0001'

    order = Order.objects.create(
       customer=customer,
       store=store,
       address=address,
       subtotal=subtotal,
       total=total,
       order_id=order_id,
       status='PALCEORDER'  
    )

    order.save()

    for cart in carts:
        cart_item = OrderItem.objects.create(
            order=order,
            quantity=cart.quantity,
            item=cart.item,
            amount=cart.amount,
            store=cart.store,
            customer=customer
        )
        cart.delete()

    cartbill.offer_amount = 0
    cartbill.coupe_code = None
    cartbill.save()

    response_data = {
        "order_id": order.order_id,
        "status": "ORDERPLACED",
    }

    return Response(response_data)


@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def track(request,id):
    order=Order.objects.get(id=id)
    offer_amount=order.subtotal-order.total

    response_data = {
        "status_code": 6000,
        "data": {
            "order": OrderSerializer(order).data,
            "offer_amount": offer_amount,
        },
        "message": "Order retrieved successfully"
    }
    return Response(response_data)

@api_view(['GET'])  
@permission_classes([AllowAny])
def restaurent(request,id):
   store_categories = StoreCategory.objects.all()
   stores = Store.objects.all()

   selected_category = StoreCategory.objects.get(id=id)

   stores = stores.filter(category=selected_category)

   context ={
       'request':request
   }

   response_data = {
       "status_code": 6000,
       "data": {
           "store_categories": StoreCategorySerializer(store_categories, many=True ,context=context).data,
           "stores": StoreSerializer(stores, many=True).data,
       },
       "message": "Restaurent retrieved successfully"
   }
   return Response(response_data)

@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def single_rest(request, id):
    user = request.user
    customer = Customer.objects.get(user=user)
    store = Store.objects.get(id=id)
    food_categories = FoodCategory.objects.filter(store=store)
    carts = Cart.objects.filter(customer=customer)
    fooditems = FoodItem.objects.filter(store=store)
    count = carts.count()
    sum = carts.aggregate(Sum('amount'))['amount__sum']

    cart_product = []

    for fooditem in fooditems:
        itemcart = Cart.objects.filter(item=fooditem, customer=customer).first()

        if itemcart:
            quantity = itemcart.quantity
        else:
            quantity = 0

        cart_product.append({
            'fooditem': FoodItemSerializer(fooditem).data,
            'quantity': quantity,
            'cart': CartSerializer(itemcart).data if itemcart else None
        })

    response_data = {
        "status_code": 6000,
        "data": {
            "store": StoreSerializer(store).data,
            "food_categories": FoodCategorySerializer(food_categories, many=True).data,
            "fooditems": FoodItemSerializer(fooditems, many=True).data,
            "count": count,
            "sum": sum,
            "cart_product": cart_product,
        },
        "message": "Restaurant retrieved successfully"
    }
    return Response(response_data)

@api_view(['GET'])  
@permission_classes([IsAuthenticated])
def logout(request):
    auth_logout(request)

    response_data = {
        "status_code": 6000,
        "data": {},
        "message": "Logout successfully"
    }
    return Response(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def checkout(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    carts = Cart.objects.filter(customer=customer)
    cartbill = CartBill.objects.get(customer=customer)
    itemtotal = carts.aggregate(Sum('amount'))['amount__sum'] or 0
    offers = Offers.objects.all()

    offer_amount = cartbill.offer_amount or 0
    delivery_charge = cartbill.delivery_charge or 0

    topay = itemtotal - offer_amount + delivery_charge

    response_data = {
        "status_code": 6000,
        "data": {
            "carts": CartSerializer(carts, many=True).data,
            "cartbill": CartBillSerializer(cartbill).data,
            "itemtotal": itemtotal,
            "offers": OffersSerializer(offers, many=True).data,
            "topay": topay
        },
        "message": "Checkout retrieved successfully"
    }

    return Response(response_data)



   

    
  









            
           
    
    