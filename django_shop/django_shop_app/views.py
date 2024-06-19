from django.shortcuts import render, redirect
from .models import Product, Rating
from .forms import RatingForm, ProductForm


def overview_list(request):

    all_products = Product.objects.all()  # fetch all housings objects in a QuerySet data type

    context = {'all_products': all_products}

    return render(request, 'overview-list.html', context)


def rate(request, pk: str, up_or_down: str):

    user = request.user

    product = Product.objects.get(id=int(pk))
    product.rate(user, up_or_down)

    return redirect('product-detail', pk=pk)


def product_detail(request, **kwargs):

    housing_id = kwargs['pk']  # pk refers to "primary key"
    current_product = Product.objects.get(id=product_id)  # fetch the single housing that is requested
    current_user = request.user

    # COMMENTS
    if request.method == 'POST':
        comment_form = RatingForm(request.POST)
        comment_form.instance.user = current_user
        comment_form.instance.product = current_product

        if comment_form.is_valid():
            comment_form.save()
        else:
            print(comment_form.errors)

    ratings = Rating.objects.filter(holiday_housing=current_product)

    context = {
        'single_housing': current_product,
        'ratings_on_the_product': ratings,
        'rating_form': RatingForm
    }

    return render(request, 'product-detail.html', context)


def product_create(request):

    if request.method == 'POST':

        form_in_function_based_view = ProductForm(request.POST)
        form_in_function_based_view.instance.user = request.user  # add also user to data

        if form_in_function_based_view.is_valid():
            form_in_function_based_view.save()
            # print('SAVED a new housing in DB')
        else:
            # print(form_in_function_based_view.errors)
            pass

        return redirect('overview-list')

    else:  # request.method == 'GET'

        form_in_my_function_based_view = ProductForm()
        context = {'form': form_in_my_function_based_view}

        return render(request, 'product-create.html', context)
