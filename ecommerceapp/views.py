import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Order
from .forms import UserRegisterForm, ProductForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden


# Home page - product list with optional category filter
@login_required
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'ecommerceapp/index.html', {
        'products': products,
        'categories': categories,
        'selected_category': category
    })

# Register view
# def register_view(request):
#     # user jodi form submit kore mane email username password post kore
#     if request.method == 'POST':
#         # user theke data nibo jemon email username password
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']        
#         # chack korbo ai user age register korche ki na
#         if User.objects.filter(username=username). exists():
#             # jodi thake user register ag theke thahole abar register page dekhabo
#             # r akta error dibo
#             return render(request, 'ecommerceapp/register.html', {'error': 'already an account present'})
#          # jodi user notun hoi tahole create kora hobe 
#         user = User.objects.create_user(username=username, email=email, password=password)
#         # user er data save korbo data base a
#         user.save()
#             # jodi shofol hoi register tahole pathabo login page a 
#         return redirect('login')
#     return render(request, 'ecommerceapp/register.html') 


def register_view(request):
    if request.method == "POST": # user submit korbe
        form = UserRegisterForm(request.POST) # data niya form banano hoiteche
        if form.is_valid(): # user er totto jodi thik hoi tahole 
            user = form.save(commit=False) # user object banano hoiteche kintu save kortese na
            user.user_type = form.cleaned_data['user_type'] # user set kora hoiteche buyer naki seller
            user.save() # abar buyer naki seller  save kora holo
            return redirect('login') # login page a pathano hocche
    else:
        form = UserRegisterForm() # faka form kora hoiteche
    return render(request, 'ecommerceapp/register.html', {'form': form}) # register.htm a pathano hoiteche            

    

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # যদি username না থাকে, তাহলে register এ পাঠাবে
        if not User.objects.filter(username=username).exists():
            return redirect("register")

        # এখন password মিলিয়ে দেখা
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'ecommerceapp/login.html', {'error': 'Invalid credentials'})

    # ✅ GET method হলে login form দেখানো
    return render(request, 'ecommerceapp/login.html')

# login page a pathai deoar jonno
def profile_redirect(request):
    return redirect('/')    


# Logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Product detail
@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'ecommerceapp/product_detail.html', {'product': product})

# Add product (seller only)
@login_required
def add_product(request):
    if request.user.user_type != 'seller':
        return HttpResponseForbidden("Only sellers can add products.")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'ecommerceapp/add_product.html', {'form': form})


# Edit product (seller only)
@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'ecommerceapp/product_form.html', {'form': form})

# Delete product (seller only)
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    product.delete()
    return redirect('product_list')

# Buy Now (create simple order)
@login_required
def buy_now(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order = Order.objects.create(buyer=request.user, product=product)
    return render(request, 'ecommerceapp/order_confirm.html', {'order': order})



from django.shortcuts import render, redirect
from .forms import ProductForm
from django.contrib.auth.decorators import login_required

# @login_required
# def add_product(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)  # ছবির জন্য request.FILES দরকার
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.seller = request.user
#             product.save()
#             return redirect('home')
#     else:
#         form = ProductForm()
#     return render(request, 'ecommerceapp/add_product.html', {'form': form})
# @login_required
# def home(request):
#     return render(request, 'ecommerceapp/home.html')

@login_required
def about_view(request):
    products = Product.objects.all()  # এখানে Product বড় হাতের P তে হবে
    return render(request, 'ecommerceapp/about.html', {'products': products})

# user er product tar icon e ana hocche
@login_required
def profile_view(request):
    if request.user.user_type == 'seller':
        user_products = Product.objects.filter(seller=request.user)
        return render(request, 'ecommerceapp/profile.html', {'products': user_products})
    else:
        # buyer হলে order list দেখাতে পারো, অথবা আলাদা template
        orders = Order.objects.filter(buyer=request.user)
        return render(request, 'ecommerceapp/buyer_profile.html', {'orders': orders})




@login_required
def my_products(request):
    products = Product.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'ecommerceapp/my_products.html', {'products': products})

    
@login_required
def home_view(request):
    products = Product.objects.all().order_by('-created_at')  
    return render(request, 'ecommerceapp/index.html', {'products': products})
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.user.user_type != 'seller':
        return render(request, 'ecommerceapp/unauthorized.html', {'error': 'Only sellers can delete products'})

    if product.seller != request.user:
        return render(request, 'ecommerceapp/unauthorized.html', {'error': 'You can only delete your own product'})

    if request.method == 'POST':
        # ✅ ফাইল ডিলিট করার অংশ
        if product.image and hasattr(product.image, 'path'):
            image_path = product.image.path
            if os.path.exists(image_path):
                os.remove(image_path)

        product.delete()
        return redirect('home')

    return render(request, 'ecommerceapp/confirm_delete.html', {'product': product})
      
         

        



    
