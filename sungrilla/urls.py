from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('locations/', views.locations, name='locations'),
    path('family_zone/', views.locations, name='family_zone'),
    path('adult_zone/', views.locations, name='adult_zone'),
    path('bar_zone/', views.locations, name="bar_zone"),
    path('terrace_zone/', views.locations, name="terrace_zone"),
    path('menu/', views.menu, name='menu'),
    path('food_menu/', views.menu, name='food_menu'),
    path('bar_menu/', views.menu, name='bar_menu'),
    path('price/', views.price, name='price'),
    path('booking/', views.booking, name='booking'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/<int:cart_item_id>/<int:quantity>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('how_to_find_us/', views.how_to_find_us, name='how_to_find_us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)