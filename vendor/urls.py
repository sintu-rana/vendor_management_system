from django.urls import path
from vendor.views import *

urlpatterns = [

    path('api/vendors/', VendorView.as_view()),
    path('api/vendors/<int:pk>/', VendorView.as_view(), name='vendor-detail'),

    path('api/purchase_orders/', PurchaseOrderView.as_view()),
    path('api/purchase_orders/<int:pk>/', PurchaseOrderView.as_view(), name='purchaseorder-detail'),


    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor_performance'),


]
