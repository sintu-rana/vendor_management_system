from django.contrib import admin
from .models import *



admin.site.register([Vendor,HistoricalPerformance])

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'vendor', 'order_date', 'delivery_date', 'status')

admin.site.register(PurchaseOrder, PurchaseOrderAdmin)

# Register your models here.