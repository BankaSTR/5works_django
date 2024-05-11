from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Basket, In_Basket, Order, In_Order, Category, User
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def main(request):
    latest_products = Product.objects.all().order_by('-id')[:5]
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    sort_by = request.GET.get('sort_by')
    direction = request.GET.get('direction', 'asc')
    keyword = request.GET.get('keyword')

    products = Product.objects.filter(categories__id=selected_category) if selected_category else Product.objects.all()

    if keyword:
        products = products.filter(title__icontains=keyword.capitalize())

    if sort_by:
        products = products.order_by(sort_by if direction == 'asc' else f'-{sort_by}')

    return render(request, "home.html", {'latest_products': latest_products, 'products': products, 'categories': categories, 'selected_category': selected_category, 'sort_by': sort_by, 'direction': 'desc' if direction == 'asc' else 'asc'})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    basket, _ = Basket.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))

    existing_item = In_Basket.objects.filter(basket=basket, prodcut=product).first()
    if existing_item:
        existing_item.quantity += quantity
        existing_item.save()
    else:
        In_Basket.objects.create(basket=basket, prodcut=product, quantity=quantity)

    return redirect("cart")

@login_required
def cart(request):
    basket, _ = Basket.objects.get_or_create(user=request.user)
    items = In_Basket.objects.filter(basket=basket)
    return render(request, 'cart.html', {'items': items, "basket": basket})

@login_required
def increase(request, cart_id, product_id):
    basket = Basket.objects.get(id=cart_id)
    in_basket = In_Basket.objects.filter(basket=basket)
    prod = get_object_or_404(Product, id=product_id)

    if prod.availability > 0 and prod.availability > in_basket.count():
        product, _ = In_Basket.objects.get_or_create(basket=basket, prodcut=prod)
        product.quantity += 1
        product.save()

    return redirect('cart')

@login_required
def decrease(request, cart_id, product_id):
    basket = Basket.objects.get(id=cart_id)
    in_bask = In_Basket.objects.filter(basket=basket)
    prod = get_object_or_404(Product, id=product_id)

    products = in_bask.filter(prodcut=prod)
    if products.exists():
        product = products.first()
        if product.quantity > 1:
            product.quantity -= 1
            product.save()
        else:
            product.delete()

    return redirect('cart')

@login_required
def checkout(request):
    order = Order.objects.create(user=request.user)
    order_last = Order.objects.filter(user=request.user).order_by('-id').first()
    return redirect('checkoutcont', order_id=order_last.id)

@login_required
def check_continue(request, order_id):
    basket = Basket.objects.get(user=request.user)
    basket_items = In_Basket.objects.filter(basket=basket)

    for basket_item in basket_items:
        order_item = In_Order.objects.create(order_id=order_id, prodcut=basket_item.prodcut, quantity=basket_item.quantity)
        basket_item.prodcut.availability -= basket_item.quantity
        basket_item.prodcut.save()
        basket_item.delete()

    order_items = In_Order.objects.filter(order_id=order_id)
    return render(request, "checkout.html", {"order_items": order_items})


@login_required
def orders_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order_list.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_objects = In_Order.objects.filter(order=order)
    return render(request, "order_detail.html", {'order_objects': order_objects})

def about(request):
    latest_products = Product.objects.all().order_by('-id')[:5]
    return render(request, "about.html", {'latest_products': latest_products})

def admins_orders(request):
    orders = Order.objects.all()
    return render(request, 'admins_orders.html', {'orders': orders})

def admin_order_response(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        if '_confirm' in request.POST:
            order.status = 'Подтверждён'
            order.save()
        elif '_decline' in request.POST:
            order.status = 'Отменён'
            order.save()
        massage = request.POST.get('massage')  # Предполагается, что у вас есть поле формы с именем 'admin_notes'
        order.massage = massage

        total_cost = sum(item.prodcut.price * item.quantity for item in order.order_of_user.all())
        order.total_cost = total_cost

        order.save()
        return redirect('admins_orders')  # Перенаправление к списку всех заказов
    return render(request, 'admins_order_response.html', {'order': order})