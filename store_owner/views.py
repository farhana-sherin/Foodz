from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate ,login as auth_login,logout as auth_logout
from django.contrib.auth import authenticate ,login as auth_Login, logout as auth_logout
from django.contrib.auth.decorators import login_required


from restaurent.models import *
from manager.form import *
from manager.models import *
from customer.models import *
from store_owner.models import *




def index(request):
   
    instances= Order.objects.all().order_by('-id')[:10]
    orders=Order.objects.count()
    earnings=0
   
    for order in instances:
      earnings +=order.total - order.delivery_charge 

    customers=Customer.objects.count()
    stores=Store.objects.count()
   
    
    

    context={
        'instances':instances,  
        'customers':customers,
        'orders':orders,
        'stores': stores,
        'earnings':earnings
        
       

      }

    return render(request, 'store_owner/index.html',context=context)

def store_categories(request):
    instances=StoreCategory.objects.all()

    context={
        'title':"store Categories | Dashboard",
        'sub_title':"Store Categories",
        'name':"Store Categories List",
        'instances':instances

    }

    return render(request,'stor_owner/store-category.html',context=context)


   
def store_categories_add(request):
    if request.method == 'POST':
        form = StoreCategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stor_owner:store_categories'))
        else:
            message = "error "
            context = {
                'title': "Store Categories | Dashboard",
                'sub_title': "Store Categories",
                'name': "Add Store Category",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "stor_owner/add-store-category.html", context=context)
    
   
    else:
        form = StoreCategoryForm()
        context = {
            "title": "Store Categories | Dashboard",
            "sub_title": "Store Categories",
            "name": "Add Store Category",
            "form": form,
        }
        return render(request, "stor_owner/add-store-category.html", context=context)



def store_categories_update(request,id):
    instance = StoreCategory.objects.get(id=id)
    if request.method == 'POST':
        form = StoreCategoryForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('stor_owner:store_categories'))
        else:
            message = "error "
            form = StoreCategoryForm(instance=instance)
            context = {
                'title': "Store Categories | Dashboard",
                'sub_title': "Store Categories",
                'name': "Add Store Category",
                "error": True,
                "message": message,
                "form": form,
                "instance":instance
            }
            return render(request, "stor_owner/add-store-category.html", context=context)
    
   
    else:
        form = StoreCategoryForm(instance=instance)
        context = {
            "title": "Store Categories | Dashboard",
            "sub_title": "Store Categories",
            "name": "Add Store Category",
            "form": form,
            "instance": instance
        }
        return render(request, "stor_owner/add-store-category.html", context=context)

def store_categories_delete(request ,id):
    store=StoreCategory.objects.get(id=id)
    store.delete()
    return HttpResponseRedirect(reverse('stor_owner:store_categories'))
    
    

def store(request):
    stores = Store.objects.all()
    
    context = {
        'title': "Stores | Dashboard",
        'sub_title': "Store Management",
        'name': "Store List",
        'stores': stores,
    }

    return render(request, 'stor_owner/store.html', context=context)





def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse ('stor_owner:store'))  
    else:
        form = StoreForm()
    
    context = {
        'form': form,
        'title': 'Add Store',
    }
    return render(request, 'stor_owner/add_store.html', context=context)



def edit_store(request,id):
    instance=Store.objects.get(id=id)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse ('stor_owner:store'))
    else:
        form = StoreForm(instance=instance)

    context = {
        'form': form,
        'instance':instance,
        'title': 'Edit Store | Dashboard',
        'sub_title': 'Update Store Details',
        'name': 'Edit Store'
    }

    return render(request, 'stor_owner/add_store.html', context=context)


def delete_store(request,id):
    store = Store.objects.get(id=id)
    store.delete()
    
    return HttpResponseRedirect(reverse('stor_owner:store'))



def food_category(request):

    instances=FoodCategory.objects.all()
    context={

        'instances':instances

        }
    
    return render(request, 'store_owner/food-category.html', context=context)

def add_foodcategory(request):
    
    if request.method == 'POST':
        form = FoodCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse ('store_owner:food_category'))  
    else:
        form = FoodCategoryForm()
    
    context = {
        'form': form,
        'title': 'Add Store',
    }
    return render(request, 'store_owner/add-food-category.html', context=context)

def edit_foodCategory(request ,id):
    instances=FoodItem.objects.get(id=id)
      
    if request.method == 'POST':
        form = FoodCategoryForm(request.POST,instance=instances)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse ('store_owner:food_category'))  
    else:
        form = FoodCategoryForm(instance=instances)
    
    context = {
        'form': form,
        'title': 'Add Store',
    }
    return render(request, 'store_owner/add-food-category.html', context=context)


def delete_foodCategory(request ,id):
    food_Cateory=FoodCategory.objects.get(id=id)
    food_Cateory.delete()
    return HttpResponseRedirect(reverse('store_owner:food_category'))




def fooditem(request):
    instances=FoodItem.objects.all()

    
    context = {
        'instances':instances
    }

    return render(request,'store_owner/fooditem.html',context=context)

def add_fooditem(request):
    form = FoodItemForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store_owner:fooditem'))
        else:
            form = FoodItemForm()

    context = {
        'form': form,
        'title': 'Add Food Item',
        'page_heading': 'Add New Food Item',
        'button_text': 'Add Food',
    }

    return render(request, 'store_owner/add_fooditem.html', context=context)

def edit_fooditem(request, id):
    instances=FoodItem.objects.get(id=id)
    form = FoodItemForm(request.POST, request.FILES, instances=instances)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('store_owner:fooditem'))
        else:
            form = FoodItemForm(instances=instances)

    context = {
        'form': form,
        'title': 'Edit Food Item',
        'page_heading': 'Edit Food Item',
        'button_text': 'Update',
    }

    return render(request, 'store_owner/add_fooditem.html', context=context)



def delete_fooditem(request, id):

    item=FoodItem.objects.get(id=id)
    item.delete()
    return HttpResponseRedirect(reverse('store_owner:fooditem'))

    

def store(request):
    stores = Store.objects.all()
    
    context = {
        'title': "Stores | Dashboard",
        'sub_title': "Store Management",
        'name': "Store List",
        'stores': stores,
    }

    return render(request, 'store_owner/store.html', context=context)





def add_store(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse ('store_owner:store'))  
    else:
        form = StoreForm()
    
    context = {
        'form': form,
        'title': 'Add Store',
    }
    return render(request, 'store_owner/add_store.html', context=context)



def edit_store(request,id):
    instance=Store.objects.get(id=id)
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse ('store_owner:store'))
    else:
        form = StoreForm(instance=instance)

    context = {
        'form': form,
        'instance':instance,
        'title': 'Edit Store | Dashboard',
        'sub_title': 'Update Store Details',
        'name': 'Edit Store'
    }

    return render(request, 'store_owner/add_store.html', context=context)


def delete_store(request,id):
    store = Store.objects.get(id=id)
    store.delete()
    
    return HttpResponseRedirect(reverse('store_owner:store'))

def orders(request):
    all_orders = Order.objects.all()

    context = {
        'title': "Orders | Dashboard",
        'sub_title': "Order Management",
        'name': "All Orders",
        'orders': all_orders
    }

    return render(request, 'store_owner/orders.html', context=context)


@login_required(login_url='/login/')
def profile(request):
    user = request.user
    store_owner = StoreOwner.objects.get(user=user)

    stores = Store.objects.all()
    food_items = FoodItem.objects.filter(store__in=stores)
    orders = Order.objects.filter(store__in=stores)

    context = {
        'store_owner': store_owner,
        'stores': stores,
        'food_items': food_items,
        'orders': orders,
    }
    return render(request, 'store_owner/profile.html', context)


def logout(request):
    auth_logout(request)

    return HttpResponseRedirect(reverse('web:login'))


def currentOrder(request,id):
    
    order=Order.objects.get(id=id)

    
        
    
    context={
        'order':order,
    }
    return render(request, 'store_owner/currentOrder.html',context=context)

