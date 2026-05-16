from django.contrib import admin

from .models import ContentSection, Crystal, CrystalEffect, CrystalEffectRelation, CrystalImage, ProductCrystal


class CrystalImageInline(admin.TabularInline):
    model = CrystalImage
    extra = 1


class ContentSectionInline(admin.TabularInline):
    model = ContentSection
    extra = 1


@admin.register(Crystal)
class CrystalAdmin(admin.ModelAdmin):
    list_display = ("id", "crystal_name", "hardness", "origin")
    search_fields = ("crystal_name", "description", "origin")
    inlines = [CrystalImageInline, ContentSectionInline]


@admin.register(CrystalEffect)
class CrystalEffectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name", "description")


admin.site.register(ProductCrystal)
admin.site.register(CrystalEffectRelation)
