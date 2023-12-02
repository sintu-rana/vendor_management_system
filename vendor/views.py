from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer, HistoricalPerformanceSerializer


# Create your views here.

class VendorView(APIView):
    
    # GET method to retrieve single vendor data
    def get(self, request, pk=None):  # 'pk' is optional and defaults to None
        if pk is not None:
            # Retrieve a single vendor by primary key
            try:
                vendor = Vendor.objects.get(pk=pk)
                serializer = VendorSerializer(vendor)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response({"detail": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all vendors
            vendors = Vendor.objects.all()
            serializer = VendorSerializer(vendors, many=True)
            return Response(serializer.data)
        
    # POST method to create a new student
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "Vendor successfully added."
        return Response({"message": message, "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    # PUT method to update an existing student (whole object)
    def put(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DELETE method to delete an existing student
    def delete(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class PurchaseOrderView(APIView):
    
    # GET method to retrieve single vendor data
    def get(self, request, pk=None):  # 'pk' is optional and defaults to None
        if pk is not None:
            # Retrieve a single purchase order by primary key
            try:
                purchaseorder = PurchaseOrder.objects.get(pk=pk)
                serializer = PurchaseOrderSerializer(purchaseorder)
                return Response(serializer.data)
            except PurchaseOrder.DoesNotExist:  # Fix: Use PurchaseOrder.DoesNotExist instead of Vendor.DoesNotExist
                return Response({"detail": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Retrieve all purchase orders
            purchaseorders = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(purchaseorders, many=True)
            return Response(serializer.data)
        
    # POST method to create a new purchase order
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            message = "PurchaseOrder successfully added."
            return Response({"message": message, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT method to update an existing purchase order (whole object)
    def put(self, request, pk):
        purchaseorder = PurchaseOrder.objects.get(pk=pk)
        serializer = PurchaseOrderSerializer(purchaseorder, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

    # DELETE method to delete an existing purchase order
    def delete(self, request, pk):
        purchaseorder = PurchaseOrder.objects.get(pk=pk)
        purchaseorder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# Vendor Performance
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import HistoricalPerformance
from .serializers import HistoricalPerformanceSerializer

class VendorPerformanceView(APIView):
    serializer_class = HistoricalPerformanceSerializer

    def get(self, request, vendor_id):
        # Retrieve historical performance data for the specified vendor_id
        queryset = HistoricalPerformance.objects.filter(vendor_id=vendor_id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
