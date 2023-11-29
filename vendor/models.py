from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"
    
    @property
    def delivery_on_time(self):
        return (
            self.status == 'completed' 
            and self.acknowledgment_date is not None 
            and self.delivery_date <= self.acknowledgment_date
        )


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Performance record for {self.vendor.name} on {self.date}"
    
@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    vendor = instance.vendor

    # On-Time Delivery Rate Calculation
    completed_purchases = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
    on_time_deliveries = sum(po.delivery_on_time for po in completed_purchases)
    total_completed_purchases = completed_purchases.count()
    vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_purchases) * 100 if total_completed_purchases > 0 else 0.0

    # Quality Rating Average Calculation
    completed_quality_ratings = [po.quality_rating for po in completed_purchases if po.quality_rating is not None]
    vendor.quality_rating_avg = sum(completed_quality_ratings) / len(completed_quality_ratings) if completed_quality_ratings else 0.0

    # Average Response Time Calculation
    acknowledged_purchases = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False)
    average_response_time = acknowledged_purchases.aggregate(models.Avg(models.F('acknowledgment_date') - models.F('issue_date')))['acknowledgment_date__avg']
    vendor.average_response_time = average_response_time.total_seconds() if average_response_time else 0.0

    # Fulfillment Rate Calculation
    successful_fulfillments = completed_purchases.filter(status='completed without issues')
    vendor.fulfillment_rate = (successful_fulfillments.count() / total_completed_purchases) * 100 if total_completed_purchases > 0 else 0.0

    vendor.save()