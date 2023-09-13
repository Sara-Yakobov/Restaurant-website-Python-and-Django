from django.shortcuts import render,redirect
from users.models import *
from .models import *
from django.contrib.auth.decorators import login_required
from users.models import Item,Dish



@login_required(login_url='login_user')
def cart(requsets, id):
    list_item = Item.objects.filter(cart=Cart.objects.last())
    dish=Dish.objects.get(id=id)
    flag=False
    for item in list_item:
        if item.dish.id == id:
            item.amount=item.amount+1
            item.save()
            flag=True

    if flag==False:
        new_item=Item()
        new_item.dish=dish
        new_item.cart = Cart.objects.last()
        new_item.amount = 1
        new_item.save()
        list_item = Item.objects.filter(cart=Cart.objects.last())



    return render(requsets,'cart.html',{'list_item':list_item})


@login_required(login_url='login_user')
def order_history(request):
    orders=Order.objects.all()

    order_list = []
    for orderli in orders:
        if orderli.order.user == request.user:
            cart_id = orderli.order.id
            items = Item.objects.filter(cart_id=cart_id)
            order_list.append({'order': orderli, 'payment': sum(x.amount * x.dish.price for x in items)})
    print(order_list)
    return render(request,'order_history.html',{"order_list": order_list})


@login_required(login_url='login_user')
def delete(request,id):
    last_cart=Cart.objects.last()
    items=Item.objects.all()
    for item in items:
        if item.dish.id==id and item.cart==last_cart:
            item.delete()

    return render(request,'cart.html',{"list_item": Item.objects.filter(cart=Cart.objects.last())})

@login_required(login_url='login_user')
def order(request):

    if request.method=='POST':

        new_order=Order(
            order=Cart.objects.last(),
            address=request.POST['adress'],
            comment=request.POST['comment']
        )
        new_order.save()
           
        return redirect(pay)
    return render(request,'order.html')    
         
@login_required(login_url='login_user')
def pay(request): 
    total=0
    my_order=Order.objects.last()
    list_item=Item.objects.all()
    for item in list_item:
         if item.cart==Cart.objects.last():
             total+=item.amount*item.dish.price
    Cart(user=request.user).save()
    return render(request,'pay.html',{"total":total,'my_order':my_order})

@login_required(login_url='login_manage')
def delivery_manage(request):
    if request.method == 'POST':
        new_chack = request.POST.copy()
        new_chack.pop('csrfmiddlewaretoken')
        for k, v in new_chack.items():
            order = Order.objects.get(pk=int(k))
            if order:
                order.is_delivered = True
                order.save()

    orders = Order.objects.all()
    list_order = []
    for orderli in orders:
        cart_id = orderli.order.id
        items = Item.objects.filter(cart_id=cart_id)
        list_order.append({'order': orderli, 'payment': sum(x.amount * x.dish.price for x in items)})
    print(list_order)
    return render(request, 'delivery_manage.html', {'list_order': list_order})
