from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from .form import CustomUserForm
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json
from django.http import JsonResponse

from .models import Products, Cart
import json

# Home page view
def Home(request):
    category = Category.objects.filter(status=0)
    products=Products.objects.filter(trending=1)
    product_count=Cart.objects.count()

    Count=0
    if request.user.is_authenticated:
        Count=Cart.objects.filter(user=request.user).count()
    return render(request, "shopclues_app/index.html",{"category":category,"products":products,"product_count":product_count})

# Register page view
def Register(request):
    form =CustomUserForm()
    product_count=Cart.objects.count()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registeration Succes You can Login Now')
            return redirect('login')
    return render(request, "shopclues_app/register.html",{"form":form,"product_count":product_count})

def Logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Logout SuccesFully")
        return redirect("home")

# Login page view
def Login(request):
  product_count=Cart.objects.count()
  if request.user.is_authenticated:
     return redirect("home")
  else:
    if request.method =="POST":
        name=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=name,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login in successfully")
            return redirect('home')
        else:
            messages.error(request,"Invalid User name or Password")
            return redirect('login')
    return render(request, "shopclues_app/Login.html",{"product_count":product_count})


# Cart page view
def Carts(request):
    product_count=Cart.objects.count()
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user)
        return render(request, "shopclues_app/cart.html",{"cart":cart,"product_count":product_count})
    else:
        return redirect("login")


def whislist(request):
    product_count=Cart.objects.count()
    if request.user.is_authenticated:
        favourites = Favourite.objects.filter(user=request.user)
        return render(request, "shopclues_app/whislist.html", {"favourites": favourites, "product_count": product_count})
    else:
        return redirect('login')  # Redirect to login page if not authenticated


# Collection page (Categories)
def Collection(request):
    product_count=Cart.objects.count()
    category = Category.objects.filter(status=0)
    return render(request, "shopclues_app/collections.html", {"category": category,"product_count":product_count})

# Products under a category
def Collectionview(request, cid):
    product_count=Cart.objects.count()
    products = Products.objects.filter(category_id=cid, status=0)
    return render(request, "shopclues_app/products/index.html", {"products": products,"product_count":product_count})

# Product Details
def product_details(request, cid, pid):
    product_count=Cart.objects.count()

    category = Category.objects.filter(id=cid, status=0).first()  # Fetch category by id
    if category:
        product = Products.objects.filter(id=pid, category_id=cid, status=0).first()  # Fetch product by id
        if product:
            return render(request, "shopclues_app/products/product_details.html", {
                "product": product,  # Pass the product data
                "category": category,  # Pass the category data correctly
                "product_count":product_count
            })
        else:
            messages.error(request, "Product not found.")
            return redirect("collection")  # Redirect if product not found
    else:
        messages.error(request, "No such category found.")
        return redirect("collection")  # Redirect if category not found

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Products, Cart
import json





def Add_to_Cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)  # Read and parse JSON from the request body
                product_qty = data.get('product_qty')
                product_id = data.get('pid')

                # Check if the necessary data is provided
                if not product_qty or not product_id:
                    return JsonResponse({'status': 'Missing product_qty or pid'}, status=400)
                # Get the product using get_object_or_404 to handle missing product more gracefully

                product = get_object_or_404(Products, id=product_id)
                # Check if the product is already in the user's cart

                if Cart.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': 'Product already in cart'}, status=200)

                # If the product is available in sufficient quantity
                if product.quantity >= product_qty:
                    # Add to the cart with the specified quantity
                    Cart.objects.create(user=request.user, product_id=product_id, quantity=product_qty)

                    # Optionally, reduce the product quantity in stock
                    product.quantity -= product_qty
                    product.save()

                    return JsonResponse({'status': 'Product added to cart'}, status=200)
                else:
                    return JsonResponse({'status': 'Product stock not available'}, status=200)

            except json.JSONDecodeError:
                logger.error("Invalid JSON data received in the request.")
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)
            
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)
            
        else:
            return JsonResponse({'status': 'Please log in to add to cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=400)
   
def remove_cart(request,cid):
    cartitem=Cart.objects.get(id=cid)
    cartitem.delete()
    return redirect('cart')

from django.http import JsonResponse
import json
from .models import Favourite

def Fav_Page(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check for AJAX request
        if request.user.is_authenticated:
            try:
                data = json.loads(request.body)  # Read and parse JSON from the request body
                product_id = data.get('pid')
                if not product_id:
                    return JsonResponse({'status': 'Missing product ID'}, status=400)

                # Check if the product is already in the user's favourites
                if Favourite.objects.filter(user=request.user, product_id=product_id).exists():
                    return JsonResponse({'status': "Product already added to Favourite"}, status=200)
                else:
                    Favourite.objects.create(user=request.user, product_id=product_id)
                    return JsonResponse({'status': "Product added successfully"}, status=200)

            except json.JSONDecodeError:
                return JsonResponse({'status': 'Invalid JSON data'}, status=400)

            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                return JsonResponse({'status': f'Error: {str(e)}'}, status=500)

        else:
            return JsonResponse({'status': 'Please log in to add to Favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid access'}, status=400)

def remove_Fav(request,cid):
    cartitem=Favourite.objects.get(id=cid)
    cartitem.delete()
    return redirect('home')

def Search_Products(request):
    product_count=Cart.objects.count()
    search_query=request.GET.get('search', '')
    if search_query:
          products=Products.objects.filter(name__icontains=search_query)
    else:
        return JsonResponse({"No Products Found"},status=200)
    return render(request,"shopclues_app/products/SearchProducts.html",{"products":products,product_count:"product_count"})

