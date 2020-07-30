from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from .models import Hall, Challenge, File, Profile, Request, Solution, Payment
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Hall)
admin.site.register(Challenge)
admin.site.register(Profile)
admin.site.register(File)
admin.site.register(Solution)
admin.site.register(Request)
admin.site.register(Payment)
