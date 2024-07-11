import datetime
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart, CartItem, Category
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.utils import timezone


def home(request):
    return render(request, 'sungrilla/home.html')


def locations(request):
    return render(request, 'sungrilla/locations.html')


def menu(request):
    return render(request, 'sungrilla/menu.html')


def price(request):
    return render(request, 'sungrilla/price.html')


def booking(request):
    products = Product.objects.all().order_by('category')
    paginator = Paginator(products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    request.session['last_visited_page'] = request.get_full_path()

    selected_category = request.GET.get('category', '')

    if selected_category:
        products = Product.objects.filter(category__name=selected_category).order_by('category')
        paginator = Paginator(products, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()

    return render(request, 'sungrilla/booking.html',
                  {'products': page_obj, 'categories': categories, 'selected_category': selected_category})


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')
    else:
        user_form = UserRegisterForm()
    return render(request, 'sungrilla/register.html', {'user_form': user_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('booking')
    else:
        form = AuthenticationForm()
    return render(request, 'sungrilla/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def create_cart(request):
    naive_datetime = datetime.datetime.now()
    aware_datetime = timezone.make_aware(naive_datetime)
    cart = Cart(created_at=aware_datetime)
    cart.save()


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, 'Товар успішно додано до корзини.')
    return redirect('cart')


def update_cart(request, cart_item_id):
    if request.method == 'POST':

        if request.user.is_authenticated:
            cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
                total_price = cart_item.quantity * cart_item.product.price
            else:
                cart_item.delete()
                total_price = 0
            return JsonResponse({'total_price': total_price, 'quantity': quantity})
        else:
            return JsonResponse({'error_message': 'Для перезамовлення товару потрібно увійти в систему.'}, status=403)


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    messages.success(request, 'Товар успішно видалено з корзини.')
    return redirect('cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_amount = sum(item.total_price for item in cart_items)
    last_visited_page = request.session.get('last_visited_page', reverse('booking'))

    return render(request, 'sungrilla/cart.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'last_visited_page': last_visited_page,
    })


@login_required
def confirm_payment(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart__user=request.user)
    total_amount = sum(item.total_price for item in cart_items)

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            context = {
                'total_amount': total_amount,
                'phone_number': phone_number,
            }
            return HttpResponse(request, 'sungrilla/confirm_payment.html', context)

    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'total_amount': total_amount,
    }
    return render(request, 'sungrilla/confirm_payment.html', context)


@csrf_exempt
@login_required
def process_payment(request):
    user = request.user
    payment_data = request.POST.get('payment_data')
    cart_items = request.POST.get('cart_items')
    total_price = request.POST.get('total_price')

    cart, created = Cart.objects.get_or_create(user=user)

    if not created:
        cart.items.clear()
        for item in cart_items:
            product_id, quantity = item.split(':')
            product = get_object_or_404(Product, id=product_id)
            cart_item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity = int(quantity)
            cart_item.save()
        cart.total_price = total_price

    cart.paid = True
    cart.save()

    return HttpResponse("Payment processed successfully!")


def how_to_find_us(request):
    return render(request, 'sungrilla/find_us.html')
