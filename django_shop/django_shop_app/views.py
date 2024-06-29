from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Rating, CartItem
from .forms import RatingForm



def overview_list(request):
    products = Product.objects.all()
    context = {'all_products': products}
    return render(request, 'overview.html', context)


def rate(request, pk: str, up_or_down: str):

    user = request.user

    product = Product.objects.get(id=int(pk))
    product.rate(user, up_or_down)

    return redirect('product-detail', pk=pk)


def product_detail(request, **kwargs):

    product_id = kwargs['pk']  # pk refers to "primary key"
    current_product = Product.objects.get(id=product_id)  # fetch the single housing that is requested
    current_user = request.user

    # COMMENTS
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        rating_form.instance.user = current_user
        rating_form.instance.product = current_product

        if rating_form.is_valid():
            rating_form.save()
        else:
            print(rating_form.errors)

    ratings = Rating.objects.filter(product_id=current_product)

    context = {
        'single_product': current_product,
        'ratings_on_the_product': ratings,
        'rating_form': RatingForm
    }

    return render(request, 'product-detail.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    # session - Sitzungen, um Daten zwischen Anfragen zu speichern
    cart = request.session.get('cart', [])
    for item in cart:
        if item['product_id'] == product.id:
            item['quantity'] += 1
            break
    else:
        cart.append({'product_id': product.id, 'quantity': 1})
    request.session['cart'] = cart
    return redirect('cart-detail')

def cart_detail(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total_price = 0
    for item in cart:
        product = get_object_or_404(Product, id=item['product_id'])
        quantity = item['quantity']
        total_price += product.price * quantity
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })

    context = {'cart_items': cart_items, 
               'total_price': total_price}
    
    return render(request, 'cart-detail.html', context)