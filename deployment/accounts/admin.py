from django.contrib import admin
from .models import UserProfile
# Register your models here.
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import Group

admin.site.unregister(Group)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
    fieldsets = (
        ['User Information', {
            'fields': ('username', 'mpassword'),
        }],

    )

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.password = make_password(obj.mpassword)
        super().save_model(request, obj, form, change)


admin.site.register(UserProfile, UserProfileAdmin)