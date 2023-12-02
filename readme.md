# Vendor Management System with Performance Metrics

## Core Features:- 

### 1. Vendor Profile Management:-

● POST /api/vendors/: Create a new vendor.

● GET /api/vendors/: List all vendors.

● GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.

● PUT /api/vendors/{vendor_id}/: Update a vendor's details.

● DELETE /api/vendors/{vendor_id}/: Delete a vendor.

### 2. Purchase Order Tracking:-

● POST /api/purchase_orders/: Create a purchase order.

● GET /api/purchase_orders/: List all purchase orders with an option to filter by
vendor.

● GET /api/purchase_orders/{po_id}/: Retrieve details of a specific purchase order.

● PUT /api/purchase_orders/{po_id}/: Update a purchase order.

● DELETE /api/purchase_orders/{po_id}/: Delete a purchase order.

### 3. Vendor Performance Evaluation:-

● GET /api/vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.

