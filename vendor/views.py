from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer

# Create your views here.

@api_view()
def view_home(request):
    return Response({'success': 409, 'message': 'api'})

class StudentView(APIView):
    
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

    # PATCH method to partially update an existing student
    def patch(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete an existing student
    def delete(self, request, pk):
        vendor = Vendor.objects.get(pk=pk)
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)