from django.contrib import admin
from .models import CottagePhoto, Cottage, Construction, Additional

# Register your models here.


class CottagePhotoInline(admin.TabularInline):
    model = CottagePhoto

@admin.register(Cottage)
class CottageAdmin(admin.ModelAdmin):
    model = Cottage
    inlines = [CottagePhotoInline,]
    prepopulated_fields = {'slug': ('name',)}

@admin.register(CottagePhoto)
class CottagePhotoAdmin(admin.ModelAdmin):
    model = CottagePhoto

@admin.register(Construction)
class ConstructionAdmin(admin.ModelAdmin):
    model = Construction
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Additional)
class AdditionalAdmin(admin.ModelAdmin):
    model = Additional
    prepopulated_fields = {'slug': ('name',)}

