from django.contrib import admin

from .models import DevappsApplication, DevappsVersion


@admin.register(DevappsApplication)
class DevappsApplicationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(DevappsVersion)
class DevappsVersionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
