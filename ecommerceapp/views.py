from django.shortcuts import render, redirect, get_object_or_404
from .models import Ecommerce, Category
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, SellerRegisterForm
from django.contrib.auth.models import User

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Ecommerce.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)  # এখানে Categoryategory ছিল যা ভুল

    context = {
        'category': category,
        'categories': categories,
        'products': products,
    }
    return render(request, 'ecommerceapp/index.html', context)

def seller_register(request):
    if request.method == 'POST':
        form = SellerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('product_list')  # নামযুক্ত URL ব্যবহার করা ভালো
    else:
        form = SellerRegisterForm()
    return render(request, 'ecommerceapp/seller_register.html', {'form': form})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'ecommerceapp/add_product.html', {'form': form})

@login_required
def edit_product(request, id):
    product = get_object_or_404(Ecommerce, id=id, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('seller_products')  # সেলারের প্রোডাক্ট লিস্টে রিডাইরেক্ট
    else:
        form = ProductForm(instance=product)
    return render(request, 'ecommerceapp/edit_product.html', {'form': form})

@login_required
def seller_products(request):
    products = Ecommerce.objects.filter(seller=request.user)
    return render(request, 'ecommerceapp/seller_products.html', {'products': products})

def about(request):
    return render(request, 'ecommerceapp/about.html')

@login_required
def deleteproduct(request, id):
    product = get_object_or_404(Ecommerce, id=id, seller=request.user)  # শুধু মালিকই ডিলিট করতে পারবে
    product.delete()
    return redirect('seller_products')  # সেলারের প্রোডাক্ট লিস্টে রিডাইরেক্ট

def wishlist(request):
    return render(request, 'ecommerceapp/wishlist.html')  # টেমপ্লেট পাথ সম্পূর্ণ করা

def cart(request):
    return render(request, 'ecommerceapp/cart.html')

def product_search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    
    results = Ecommerce.objects.all()
    
    if query:
        results = results.filter(name__icontains=query)
    
    if category_id:
        results = results.filter(category__id=category_id)
    
    return render(request, 'ecommerceapp/search_results.html', {  # টেমপ্লেট পাথ সম্পূর্ণ করা
        'results': results,
        'query': query
    })




        
         

        



    
