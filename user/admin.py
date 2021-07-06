from django.contrib import admin
from .models import User, Payment, Bookmark, Reviews

# Register your models here.
admin.site.register(User)
admin.site.register(Payment)
admin.site.register(Bookmark)
admin.site.register(Reviews)
