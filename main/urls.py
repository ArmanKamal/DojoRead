from django.urls import path
from .views import index,create_user,dashboard,login,logout,book_form,create_book,list_book,detail_book,add_review,detail_user

urlpatterns = [
    path('', index,name="home"),
    path('user/create', create_user),
    path('user/<int:user_id>',detail_user),
    path('user/dashboard', dashboard),
    path('user/login',login),
    path('user/logout',logout),
    path('books/', list_book),
    path('books/book_form',book_form),
    path('books/create',create_book),
    path('books/<int:id>',detail_book),
    path('books/add_review',add_review)
]
