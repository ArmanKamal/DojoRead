from django.shortcuts import render, redirect
from .models import User,Author,Book,Review
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")


def create_user(request):
    if request.method == "POST":
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            name=request.POST['name'],
            alias=request.POST['alias'],
            email=request.POST['email'],
            password=hash_pw,
        )
        request.session['logged_user'] = new_user.id
        return redirect('/user/dashboard')
    return redirect('/')

def login(request):
    if request.method == "POST":
        user = User.objects.filter(email=request.POST['email'])

        if user:
            logged_user = user[0]

            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['logged_user'] = logged_user.id
                return redirect('/user/dashboard')
            messages.error(request, "email or password are incorrect")
    return redirect('/')


def logout(request):
    request.session.flush()
    return redirect('/')

def detail_user(request,user_id):
    user = User.objects.get(id=user_id)
    context = {
        "user": user
    }
    return render(request,"detail_user.html",context)

def dashboard(request):
    context = {
        "logged_user": User.objects.get(id=request.session['logged_user'])
    }
    return render(request, "dashboard.html",context)


def book_form(request):
    if 'logged_user' not in request.session:
        return redirect('/')
    context = {
        'authors': Author.objects.all()
    }
    return render(request, "add_book.html",context)

def create_book(request):
    if request.method == "POST":
        book_errors = Book.objects.book_validator(request.POST)
        review_errors = Review.objects.review_validator(request.POST)
        errors = list(book_errors.values()) + list(review_errors.values())
        if request.POST['author_dropdown'] == "-1":
            if request.POST['author_name'] == "":
                messages.error(request, "Please either choose or add author")
            else:
                author_errors = Author.objects.author_validator(request.POST)
                errors += list(author_errors.values())   
        if errors:
            for error in errors:
                messages.error(request,error)
            return redirect('/books/book_form')
        if request.POST['author_dropdown'] == "-1":
            author = Author.objects.create(name=request.POST['author_name'])
        else:
            author = Author.objects.get(id=request.POST['author_dropdown'])
        book = Book.objects.create(title=request.POST['title'])
        user = User.objects.get(id=request.session['logged_user'])
        review = Review.objects.create(content=request.POST['content'],rating= int(request.POST['rating']),book_reviewd=book,user_review=user)
        book.authors.add(author)
        return redirect(f'/books/{book.id}')
    return redirect('/books/book_form')   

def detail_book(request,id):
    book = Book.objects.get(id=id)
    context = {
        "book":book
    }
    return render(request, 'detail_book.html',context)

def add_review(request):
    errors = Review.objects.review_validator(request.POST)
    book = Book.objects.get(id= request.POST['book_reviewed'])

    if errors:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect(f'/books/{book.id}')
    user = User.objects.get(id=request.session['logged_user'])
    Review.objects.create(content=request.POST['content'],rating= int(request.POST['rating']),book_reviewd=book,user_review=user)
    return redirect(f'/books/{book.id}')

def list_book(request):
    books = Book.objects.all()
    context = {
        "logged_user": User.objects.get(id=request.session['logged_user']),
        "books": books,
        "recent_reviews": Review.objects.order_by('-created_at')[:3]
    }
    return render(request,"list_book.html",context)