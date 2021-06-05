from django.contrib import admin

# Register your models here.
from users.models import UserProfile

admin.site.register(UserProfile)
