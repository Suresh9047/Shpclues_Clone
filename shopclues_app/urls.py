from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name="home"),
    path('register', views.Register, name="register"),
    path('login', views.Login, name="login"),
    path('cart', views.Carts, name="cart"),
    path('add_to_wishlist/', views.Fav_Page, name='fav'),
    path('logout', views.Logout_page, name="logout"),
    path('collections', views.Collection, name="collection"),
    path('collections/<int:cid>', views.Collectionview, name="collection_view"),
    path('collections/<int:cid>/<int:pid>', views.product_details, name="product_details"),
    path('addtocart', views.Add_to_Cart, name="addtocart"),
    path('removecart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('removefav/<str:cid>', views.remove_Fav, name="remove_Fav"),
    path('whislist', views.whislist, name="whislist"),
    path('SearchProducts', views.Search_Products, name="searchproducts"),
   
]
