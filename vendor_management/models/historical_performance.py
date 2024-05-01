from django.db import models
from django.utils import timezone

from vendor_management.models import Vendor


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=timezone.now)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        db_table = 'historical_performance'
