from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate ,login as auth_Login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from users.models import User
from customer.models import *
from restaurent.models import *



@login_required(login_url='/login/')
def index(request):

    store_categories=StoreCategory.objects.all()
    stores=Store.objects.all()
    context={
        'store_categories':store_categories,
        'stores':stores,
    }
    return render(request,'web/index.html',context=context)


def login(request):
    if request.method =='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        user=authenticate(request ,email=email ,password=password)

        if user is not None:
            auth_Login(request,user)

            if user.is_superuser:
                
                return HttpResponseRedirect(reverse('manager:index'))
            
            elif user.is_store:
                return HttpResponseRedirect(reverse('store_owner:index'))

            else:
                return HttpResponseRedirect(reverse('web:index'))
        else:
            context={

        'error':True,
        'message':'invalid email or password'
       
     }
            return render(request,'web/login.html', context=context)
    else:
        return render(request ,'web/login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            context = {
                'error': True,
                'message': 'Email already exists'
            }
            return render(request, 'web/register.html', context=context)
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password,
                is_customer=True
            )
            user.save()

            customer = Customer.objects.create(
                user=user
            )
            customer.save()

            return HttpResponseRedirect(reverse('web:login'))

    else:
        return render(request, 'web/register.html')

    

def logout(request):
    auth_logout(request)

    return HttpResponseRedirect(reverse('web:login'))


def restaurent(request,id):
    
    store_categories=StoreCategory.objects.all()
    stores=Store.objects.all()


    selected_category=StoreCategory.objects.get(id=id)


    stores=stores.filter(category=selected_category)


    context={
        'store_categories':store_categories,
        'stores':stores,
    }
    return render(request , 'web/restaurent.html',context=context)


@login_required(login_url='/login/')
def single_rest(request,id):
    user=request.user
    customer=Customer.objects.get(user=user)
    store=Store.objects.get(id=id)
    food_categories=FoodCategory.objects.filter(store=store)
    carts=Cart.objects.filter(customer=customer)
    fooditems=FoodItem.objects.filter(store=store)
    count=carts.count()
    sum=carts.aggregate(Sum('amount'))['amount__sum']
    

    cart_product=[]

    for fooditem in fooditems:
        
        itemcart= Cart.objects.filter(item=fooditem,customer=customer).first()

        if itemcart:
            quantity=itemcart.quantity

        else:
            quantity=0
        
        cart_product.append({  
                'fooditem':fooditem,
                'quantity':quantity,
                'cart':itemcart
            })




    context={
        'food_categories':food_categories,
        'store':store,
        ' carts': carts,
        'cart_product':cart_product,
        'count':count,
        'sum':sum

    }

    return render (request, 'web/single-rest.html', context=context)

@login_required(login_url='/login/')
def account(request ):
    user=request.user
    customer=Customer.objects.get(user=user)
    order_count = Order.objects.filter(customer=customer).count()
    order=Order.objects.filter(customer=customer).order_by('-id')[:2]
  

    item_count=[]
    

    for order in order:
        
        count=OrderItem.objects.filter(order=order).count()

        item_count.append({

            'order':order,
            'count':count,
            'order_count':order_count,
            

            

        })


   

    context={
        
       'customer':customer,
       ' order_count': order_count,
       'item_count':item_count,
      
       
    }


    return render(request, 'web/account.html',context=context)

def offers(request):
    
    offers=Offers.objects.all()
    context={
        'offers':offers
    }
    return render(request, 'web/offers.html', context=context)

def cart(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    carts=Cart.objects.filter(customer=customer)
    store=carts.first().store 
    addresses=Address.objects.filter(customer=customer)
    itemtotal=carts.aggregate(Sum('amount'))['amount__sum']
    
    
    
    


    selected_address=None
    for address in addresses:
        if address.is_selected:
            selected_address=address

    

    if CartBill.objects.filter(customer=customer).exists():
        cartbill=CartBill.objects.get(customer=customer)
    else:
        cartbill=CartBill.objects.create(
            customer=customer
        )
        cartbill.save()

    
    topay = itemtotal - cartbill.offer_amount - cartbill.delivery_charge

    offers=Offers.objects.all()

    error=None
    if request.method =='POST':
        Coupencode=request.POST.get('CoupenCode')
        for offer in offers:
            if Coupencode == offer.code :
                
                if offer.is_pecentage:
                    cartbill.offer_amount=itemtotal*(offer.offer/100)
                    cartbill.coupe_code=Coupencode
                    cartbill.save()
                   
                else:
                    
                    cartbill.offer_amount=(offer.offer)
                    cartbill.coupe_code=Coupencode
                    cartbill.save()
                   

            else:
                error ='Invalid Coupen Code'
        
        
        return HttpResponseRedirect(reverse('web:cart'))
    

    context={
        
        'store':store,
        'carts':carts,
        'selected_address':selected_address,
        'itemtotal':itemtotal,
        'offers':offers,
        'error': error,
        'cartbill':cartbill,
        'topay':topay

    } 




    return render(request, 'web/cart.html',context=context)

   



def checkout(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    carts=Cart.objects.filter(customer=customer)
    cartbill=CartBill.objects.get(customer=customer)
    itemtotal=carts.aggregate(Sum('amount'))['amount__sum']
    offers=Offers.objects.all()
    topay = itemtotal - cartbill.offer_amount - cartbill.delivery_charge


    context={
        'itemtotal':itemtotal,
        'offers':offers,
        'topay':topay,
        'cartbill':cartbill
    }


    return render(request, 'web/checkout.html',context=context)

def add_address(request):
    user = request.user
    customer =Customer.objects.get(user=user)

    if request.method =='POST':
        address=request.POST.get('Address')
        appartment=request.POST.get('Appartment')
        landmark=request.POST.get('landmark')
        address_type=request.POST.get('address_type')

    
        addr=Address.objects.create(
            customer = customer,
            address= address,
            appartment= appartment,
            landmark=landmark,
            address_type=address_type,

        )
        addr.save()

        return HttpResponseRedirect(reverse('web:address'))

    else:
     

        return render(request, 'web/add-addres.html')

def address(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    address=Address.objects.filter(customer = customer)

    context ={
        "address" : address,
    }

    return render(request, 'web/address.html',context=context)


def address_edit(request ,id):
     user = request.user
     customer =Customer.objects.get(user=user)
     
     form = Address.objects.get(id=id, customer=customer)
     

     if request.method =='POST':
        address=request.POST.get('Address')
        apartment=request.POST.get('Appartment')
        landmark=request.POST.get('landmark')
        address_type=request.POST.get('address_type')


        form.address = address
        form.appartment = apartment
        form.landmark = landmark
        form.address_type = address_type

        form.save()
        

        return HttpResponseRedirect(reverse('web:address'))
     
     context={
         "form": form,
     }
          
     return render(request, 'web/add-addres.html', context=context)

     


def address_delete(request,id):
    address=Address.objects.get(id=id)
    address.delete()
    return HttpResponseRedirect(reverse('web:address'))


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
    return HttpResponseRedirect(reverse('web:single_rest',kwargs={"id":store.id}))


def inc_fooditem(request ,id):
    
    cart=Cart.objects.get(id=id)
    fooditem_price=cart.item.price
    store=cart.store



    cart.quantity += 1
    cart.amount += fooditem_price

    cart.save()
    return HttpResponseRedirect(reverse('web:single_rest',kwargs={"id":store.id}))

def decr_fooditem(request ,id):
    cart=Cart.objects.get(id=id)
    fooditem_price= cart.item.price
    store=cart.store
    cart.quantity -= 1
    cart.amount -= fooditem_price

    cart.save()

    return HttpResponseRedirect(reverse('web:single_rest',kwargs={"id":store.id}))



def cart_inc_fooditem(request ,id):
    
    cart=Cart.objects.get(id=id)
    fooditem_price=cart.item.price
    



    cart.quantity += 1
    cart.amount += fooditem_price

    cart.save()
    return HttpResponseRedirect(reverse('web:cart'))

def cart_decr_fooditem(request ,id):
    cart=Cart.objects.get(id=id)
    fooditem_price= cart.item.price
    
    cart.quantity -= 1
    cart.amount -= fooditem_price

    cart.save()

    return HttpResponseRedirect(reverse('web:cart'))



def address_select(request ,id):
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

    return HttpResponseRedirect(reverse('web:address'))

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

    return HttpResponseRedirect(reverse('web:cart'))


def orders(request):
   
    user=request.user
    customer=Customer.objects.get(user=user)
    order=Order.objects.filter(customer=customer)
  

    item_count=[]

    for order in order:
        count=OrderItem.objects.filter(order=order).count()

        item_count.append({

            'order':order,
            'count':count,
            

            

        })


   

    context={
        
       'customer':customer,
       
       'item_count':item_count,
      
       
    }
    return render(request,'web/order.html',context=context)



def placeorder(request):

    user=request.user
    customer=Customer.objects.get(user=user)
    addrs=Address.objects.filter(customer=customer)
    cartbill=CartBill.objects.get(customer=customer)
    carts=Cart.objects.filter(customer=customer)
    subtotal=carts.aggregate(Sum('amount'))['amount__sum']
    total= subtotal -cartbill.offer_amount


    for addr in addrs:
        if addr.is_selected:
            address=addr



    for cart in carts:
        store=cart.store


    previous=Order.objects.filter(customer=customer).first()

    if previous:
        order_id=f'ORD000{previous.id+1}'
    else:
        order_id='ORD0001'




    order= Order.objects.create(

       customer=customer,
       store=store,
       address=address,
       subtotal= subtotal,
       total=total,
       order_id= order_id,
       status='PALCEORDER'


    )

    order.save()


    for cart in carts:
        cart_item=OrderItem.objects.create(
            order=order,
            quantity=cart.quantity,
            item=cart.item,
            amount=cart.amount,
            store=cart.store,
            customer=customer


            

        )
        cart.delete()


    cartbill.offer_amount=0
    cartbill.coupe_code=None
    cartbill.save()


    
    return HttpResponseRedirect(reverse('web:account'))


def track(request ,id):
    order=Order.objects.get(id=id)
    offer_amount=order.subtotal-order.total
    



    context={
        'offer_amount':offer_amount,
        'order':order
      
    }

    return render(request,'web/track.html',context=context)







        

    

    
    




    
    



        
     
    













    
