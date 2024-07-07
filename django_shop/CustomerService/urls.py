from django.urls import path
from . import views

urlpatterns = [
    path('products/add/<int:pk>/', views.ProductAddView.as_view(), name='add-product'),
    path('products/edit/<int:pk>/', views.ProductEditView.as_view(), name='edit-product'),
    path('delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('edit/<int:pk>/', views.CommentEditView.as_view(), name='comment-edit'),
    path('editdelete/<int:pk>/', views.comment_edit_delete, name='comment-edit-delete'),
]