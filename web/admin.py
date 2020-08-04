from django.contrib import admin
from web.models import Good, Consumer, BillDetail, Bill

# Register your models here.


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




