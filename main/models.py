from django.db import models
import re 
   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$") 

# Create your models here.
class UserManager(models.Manager):
 
    def registration_validator(self, postData):
        errors = {}
        if len(postData['name'])< 2:
            errors['name'] = "Name must be atleast two characters"
        
        if len(postData['alias']) <2:
            errors['alias'] = "Alias must be more than two characters"
        
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"

        users_email = User.objects.filter(email=postData['email'])
        if len(users_email) >=1:
            errors['duplicate'] = "Email already exists."
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Minimum eight characters, at least one letter, one number and one special character:"  
        if postData['password'] != postData['confirm_pw']:
            errors['pass_match'] = "Password must match!!!"
        
        return errors

class User(models.Model):
    name = models.CharField(max_length=120)
    alias = models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    password = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager):
    def book_validator(self,postData):
        errors={}
        if len(postData['title'])< 2:
            errors['title'] = "Title must be atleast two characters"
        return errors    

class Book(models.Model):
    title = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

class AuthorManager(models.Manager):
    def author_validator(self,postData):
        errors={}
        if len(postData['author_name'])< 2:
            errors['author_name'] = "Author name must be atleast two characters"
        author_db = Author.objects.filter(name=postData['author_name'])
        if len(author_db)>=1:
            errors['duplicate'] = "This author already exist in database"
        return errors

class Author(models.Model):
    name = models.CharField(max_length=120)
    books = models.ManyToManyField(Book,related_name="authors")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

class ReviewManager(models.Manager):
    def review_validator(self,postData):
        errors={}
        if len(postData['content'])<10:
            errors['content'] = "Please leave a review of atleast 10 characters"
        return errors

class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    user_review = models.ForeignKey(User,related_name="user_reviews",on_delete=models.CASCADE)
    book_reviewd = models.ForeignKey(Book, related_name="book_reviews",on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()