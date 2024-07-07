from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView
from .forms import ProductForm, RatingEditForm
from django_shop_app.models import Product, Rating
from UserAdmin.models import MyUser


def is_kundenservice(user):
    return user.groups.filter(name='Kundenservice').exists() or user.is_superuser



    
# class CommentDeleteView(LoginRequiredMixin, ListView):
#     login_url = '/useradmin/login/'
class CommentDeleteView(ListView):

    model = Rating
    context_object_name = 'all_comments'
    template_name = 'comment-delete.html'

    def get_context_data(self, **kwargs):

        context = super(CommentDeleteView, self).get_context_data(**kwargs)
        myuser = self.request.user

        context['has_delete_permission'] = not myuser.is_anonymous and myuser.has_delete_permission()

        return context

    def post(self, request, *args, **kwargs):

        comment_id = request.POST['comment_id']

        if 'delete' in request.POST:
            Rating.objects.get(id=comment_id).delete()

            return redirect('comment-delete')


class CommentEditView(UpdateView):

    model = Rating
    form_class = RatingEditForm
    template_name = 'comment-edit.html'
    success_url = reverse_lazy('comment-delete')

    def get_context_data(self, **kwargs):

        context = super(CommentEditView, self).get_context_data(**kwargs)

        myuser = self.request.user

        context['has_delete_permission'] = not myuser.is_anonymous and myuser.has_delete_permission()

        return context


# @staff_member_required(login_url='/useradmin/login/')
@login_required
@user_passes_test(is_kundenservice, login_url='/useradmin/login/')
def comment_edit_delete(request, pk: str):

    comment_id = pk

    if request.method == 'POST':
        print('-------------', request.POST)

        if 'edit' in request.POST:
            form = RatingEditForm(request.POST)

            if form.is_valid():
                comment = Rating.objects.get(id=comment_id)
                new_text = form.cleaned_data['text']
                comment.text = new_text
                comment.save()

        elif 'delete' in request.POST:
            Rating.objects.get(id=comment_id).delete()

        return redirect('comment-delete')

    else:  # GET case

        comment = Rating.objects.get(id=comment_id)
        form = RatingEditForm(request.POST or None, instance=comment)

        myuser = request.user
        has_delete_permission = not myuser.is_anonymous and myuser.has_delete_permission()

        context = {
            'form': form,
            'comment': comment,
            'has_delete_permission': has_delete_permission,
        }

        return render(request, 'comment-edit-delete.html', context)


class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'edit-product.html'
    success_url = reverse_lazy('overview')

class ProductAddView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'add-product.html'
    success_url = reverse_lazy('overview')
    
    
