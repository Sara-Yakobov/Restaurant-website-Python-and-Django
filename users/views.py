from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login,authenticate,logout
from .models import Category,Dish
from django.contrib.auth.hashers import make_password
from orders.models import Cart
from .forms import CategoryForm, DishForm





def main(request):
    return render(request,'main.html')





def signup_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_view') 
    else:
        form = UserForm()
 
    context = {'form': form}
    return render(request, 'signup_user.html', context)




def login_view(request):
    if request.method == 'POST':
        # Get the username and password from the POST request
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # If the user is authenticated, log them in and redirect to a success page
        if user is not None:
            login(request, user)
            new_cart=Cart(user=user)
            new_cart.save()
            return redirect('category_user')
        # If the user is not authenticated, show an error message
        
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')







def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('category-admin')
        else:
            error_message = "Invalid login credentials or you are not authorized to access this page."
            return render(request, 'admin_login.html', {'error_message': error_message})
    else:
        return render(request, 'admin_login.html')




def update_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('login_view') # redirect to user profile page
    else:
        form = UserForm(instance=user)
 
    return render(request, 'update_user.html', {'form': form})


@login_required(login_url='admin_login')
def category_admin(request):
    categories=Category.objects.all()
    return render(request,'category_admin.html',{'categories': categories})



@login_required(login_url='login_view')
def category_user(request):
    categories=Category.objects.all()
    return render(request, 'category_user.html',{'categories': categories})

@login_required(login_url='login_view')
def dishes_user(request, id):
    category = Category.objects.get(id=id)
    dishes = Dish.objects.all()
    return render(request, 'dishes_user.html', {"category":category, "dishes":dishes})



@login_required(login_url='admin_login')
def edit_category(request,id):
    category=Category.objects.get(id=id)
    if request.method=='POST':
        category.name=request.POST['name']
        category.imageUrl=request.POST['imageUrl']
        category.save()
        return redirect('category-admin')
    category_form = CategoryForm(instance=category)
    return render(request,'edit_category.html',{"category": category_form, 'id': id})



@login_required(login_url='admin_login')
def delete_category(request,id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect('category-admin')


@login_required(login_url='admin_login')
def edit_dish(request, id):
    dish = Dish.objects.get(id=id)
    if request.method == 'POST':
        dish.name=request.POST['name']
        dish.price=request.POST['price']
        dish.description=request.POST['description']
        dish.imageUrl=request.POST['imageUrl']
        dish.is_gluten_free=True if request.POST.get('is_gluten_free') == 'on' else False
        dish.is_vegetarian=True if request.POST.get('is_vegetarian') == 'on' else False
        category_id = request.POST['categories']
        category = Category.objects.get(id=category_id)
        dish.category = category
        dish.save()
        return redirect('dishes-admin', id=category_id)

    categories = list(Category.objects.all()).copy()
    categories.remove(dish.category)
    categories.insert(0, dish.category)
    return render(request, 'edit_dish.html', {'dish_id': dish.id, 'categories': categories, 'dish': DishForm(instance=dish)})



@login_required(login_url='admin_login')
def delete_dish(request, id):
    dish = Dish.objects.get(id=id)
    category_id = dish.category.id
    dish.delete()
    return redirect('dishes-admin', id=category_id)



@login_required(login_url='admin_login')
def dishes_admin(request,id):
    category = Category.objects.get(id=id)
    dishes = Dish.objects.all()
    return render(request,'dishes_admin.html',{"id":category.id, "dishes":dishes})


@login_required(login_url='admin_login')
def add_category(request):
    if request.method=='POST':
        new_category=Category(
           name=request.POST['category_name'], 
           imageUrl=request.POST['imageUrl'] 
        )
        new_category.save()
        return redirect('category-admin')
    return render(request,'add_category.html')


@login_required(login_url='admin_login')
def add_dish(request):
    is_gluten_free = True if request.POST.get('is_gluten_free') == 'on' else False
    is_vegetarian = True if request.POST.get('is_vegetarian') == 'on' else False
    if request.method == 'POST':
        new_dish=Dish(
            name=request.POST['name'],
            price=request.POST['price'],
            description=request.POST['description'],
            imageUrl=request.POST['imageUrl'],
            is_gluten_free=is_gluten_free,
            is_vegetarian=is_vegetarian,
            category_id=request.POST['categories']
        )
        new_dish.save()
        return redirect('dishes-admin',id=request.POST['categories'])
    categories=Category.objects.all()
    return render(request, 'add_dish.html', {'categories': categories})


@login_required(login_url='signup_user')
def logout_user(request):
    logout(request)
    return redirect('signup_user')

@login_required(login_url='admin_login')
def logout_manager(request):
    logout(request)
    return redirect('admin_login')
