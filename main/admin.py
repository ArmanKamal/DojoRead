from django.contrib import admin
from .models import Review,Book,Author
# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Review)