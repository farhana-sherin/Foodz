from django.contrib.auth import authenticate


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from customer.models import *
from users.models import User
from api.v1.customer.serializers import AddressSerializer






@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(email=email,password=password).exists():
        user=authenticate(request, email=email, password=password)



        if Customer.objects.filter(user=user).exists():
            refersh= RefreshToken.for_user(user)
            response_data = {
                "status_code":6000,
                "data":{
                    "access":str(refersh.access_token),
                   
                },
                "message":"Login Successfully"   
            }
        else:
            response_data = {
                "status_code": 6001,
                "data": {
                    
                },
                "message": "customer does not exist"
            }
    else:
        response_data = {
            "status_code": 6001,
            "data": {
                
            },
            "message": "Invalid credentials"
        }

    return Response(response_data)



@api_view(['POST'])
@permission_classes(AllowAny)
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
    else:
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        

        customer = Customer.objects.create(
            user=user,
            )
        

        user=authenticate(request, email=email, password=password)
        refersh = RefreshToken.for_user(user)
        response_data = {
            "status_code": 6000,
            "data": {
                "access": str(refersh.access_token),
            },
            "message": "Registration successful"
        }
    return Response(response_data)


@api_view(['POST'])
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
    address= request.data.get('Address')
    appartment = request.data.get('Apartment')
    landmark = request.data.get('landmark')
    address_type = request.data.get('address_type')

    Address.objects.create(
        address=address,
        appartment=appartment,
        landmark=landmark,
        address_type=address_type
    )
    response_data = {
        "status_code": 6000,
        
        "message": "Address created successfully"
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








        

   

    
 

   

