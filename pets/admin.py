from django.contrib import admin
from .models import PetsInfo, PetsType, Adoption
# Register your models here.

class AdoptionInline(admin.TabularInline):
    model = Adoption
    extra = 0
    # '''设置列表可显示的字段'''
    # fields = ('title', 'author',  'status', 'mod_date',)


class PetsInfoAdmin(admin.ModelAdmin):
    list_display = ["name", "status"]
    list_editable = ("status",)
    inlines = [AdoptionInline, ]


class AdoptionAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "pet", "status"]
    list_editable = ("status", )


admin.site.register(PetsInfo, PetsInfoAdmin)
admin.site.register(PetsType)
admin.site.register(Adoption, AdoptionAdmin)


admin.site.site_title = "PetRehomes System Management"
admin.site.site_header = "PetRehomes System Management"