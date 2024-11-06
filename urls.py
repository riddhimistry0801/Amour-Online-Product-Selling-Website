from django.urls import path from .views import (
HomeView, index, ProductDetail, CheckoutView,
AllProductsView,
CartView,
register, products, add_to_cart, remove_from_cart,
remove_single_from_cart, login1,
logout1,
)

urlpatterns = [
path('', HomeView.as_view(), name='index'),
path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'), path('remove-from-
cart/<slug>/', remove_from_cart, name='remove_from_cart'), path('remove-single-from-
cart/<slug>/', remove_single_from_cart, name='remove_single_from_cart'), path('purchase/', CheckoutView.as_view(), name='purchase'), path('products/', AllProductsView.as_view(), name = 'products'), path('product/<slug>/', ProductDetail.as_view(), name = 'product'), path('cart/', CartView.as_view(), name='cart'),
path('register/', register, name = 'register'), path('login/', login1, name='login'), path('logout1/', logout1, name = 'logout1'),

]
