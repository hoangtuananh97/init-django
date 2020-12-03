from django.contrib import admin


# Register your models here.
from app.web.models import Good, BillDetail


class GoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status']
    list_filter = ['name']
    search_fields = ['name']
    readonly_fields = ['name', 'status']


class BillDetailAdmin(admin.ModelAdmin):
    list_display = ['id']
    list_filter = ['id']


admin.site.register(Good, GoodAdmin)
admin.site.register(BillDetail, BillDetailAdmin)
