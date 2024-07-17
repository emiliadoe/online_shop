from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Rating, CartItem, ReviewVote
from .forms import RatingForm, SearchForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Q


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
    current_product = Product.objects.get(id=product_id) 
    current_user = request.user

    # COMMENTS
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if Rating.objects.filter(user=current_user, product=current_product).exists():
            rating_form.add_error(None, "You have already rated this product.")
        else:
            rating_form.instance.user = current_user
            rating_form.instance.product = current_product
            if rating_form.is_valid():
                rating_form.save()
                return redirect('product-detail', pk=product_id)
            else:
                print(rating_form.errors)
    else:
        rating_form = RatingForm()

    ratings = Rating.objects.filter(product_id=current_product).annotate(
        helpful_count=Count('reviewvote', filter=Q(reviewvote__vote_type='helpful')),
        not_helpful_count=Count('reviewvote', filter=Q(reviewvote__vote_type='not_helpful'))
    )

    context = {
        'single_product': current_product,
        'ratings_on_the_product': ratings,
        'rating_form': rating_form
    }

    return render(request, 'product-detail.html', context)

def vote_review(request, rating_id, vote_type):
    rating = get_object_or_404(Rating, id=rating_id)
    user = request.user

    try:
        review_vote = ReviewVote.objects.get(user=user, rating=rating)
        if review_vote.vote_type == vote_type:
            # If the user clicks again on the same vote, remove the vote
            review_vote.delete()
        else:
            # If the user changes the vote type, update the vote
            review_vote.vote_type = vote_type
            review_vote.save()
    except ReviewVote.DoesNotExist:
        # If the user hasn't voted yet, create a new vote
        ReviewVote.objects.create(user=user, rating=rating, vote_type=vote_type)

    helpful_count = ReviewVote.objects.filter(rating=rating, vote_type='helpful').count()
    not_helpful_count = ReviewVote.objects.filter(rating=rating, vote_type='not_helpful').count()

    return JsonResponse({
        'helpful_count': helpful_count,
        'not_helpful_count': not_helpful_count,
        'vote_type': vote_type
    })

def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    current_user = request.user

    # session - Sitzungen, um Daten zwischen Anfragen zu speichern
    cart = request.session.get('cart', [])
    for item in cart:
        if item['product_id'] == product.id:
            item['quantity'] += 1
            break
    else:
        cart.append({'product_id': product.id, 'quantity': 1})
    request.session['cart'] = cart
    # return HttpResponse('Product added to cart')
    current_product = Product.objects.get(id=product.id) 
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


def product_search(request):

    if request.method == 'POST':

        search_title = request.POST['title']
        search_description = request.POST['description']
        # search_rating = request.POST['rating']
        # searched_rating = int(search_rating) if search_rating else 0


        products_found = Product.objects.filter(
            Q(title__contains=search_title)
            & Q(description__contains=search_description)
            # & Q(ratings__gte=searched_rating)
        )

        # alternative:
        # housings_found = (
        #         HolidayHousing.objects.filter(title__contains=search_string_title)
        #         & HolidayHousing.objects.filter(specials__contains=search_string_specials)
        #         & HolidayHousing.objects.filter(rooms__gte=searched_rooms)
        # )

        form_in_function_based_view = SearchForm()

        context = {
            'show_search_results': True,
            'form': form_in_function_based_view,
            'products_found': products_found
        }

    else:  # GET

        form_in_function_based_view = SearchForm()

        context = {
            'show_search_results': False,
            'form': form_in_function_based_view,
        }

    return render(request, 'product-search.html', context)
