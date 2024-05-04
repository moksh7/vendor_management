import django.dispatch
from django.db.models import Avg, Case, When, FloatField, F, Count, DurationField, ExpressionWrapper

from vendor_management.models import PurchaseOrder, HistoricalPerformance


metric_update = django.dispatch.Signal()

def process_po_info(sender, **kwargs):
    '''
    callback function that handles signal calls based on triggered events and processes and updates the metrics
    '''
    vendor = kwargs.get('vendor')
    if kwargs.get('event') == 'delivered':
        update_on_time_delivery_rate(vendor)
        update_fulfillment_rate(vendor)
    elif kwargs.get('event') == 'ack':
        update_resp_time(vendor)
    elif kwargs.get('event') == 'rating':
        update_avg_rating(vendor)
    HistoricalPerformance.objects.create(vendor=vendor, on_time_delivery_rate=vendor.on_time_delivery_rate,
        quality_rating_avg=vendor.quality_rating_avg, average_response_time=vendor.average_response_time, fulfillment_rate=vendor.fulfillment_rate)

def update_on_time_delivery_rate(vendor):
    on_time_delivery_rate = PurchaseOrder.objects.filter(status='completed', vendor=vendor).aggregate(
        on_time_delivery_rate=Avg(Case(When(delivery_date__lte=F('est_delivery_date'), then=1.0), default=0.0, output_field=FloatField())) * 100)['on_time_delivery_rate'] or 0
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.save()

def update_fulfillment_rate(vendor):
    fulfilment_meta = PurchaseOrder.objects.filter(vendor=vendor).aggregate(total_count=Count('*'), delivered=Count('delivery_date'))
    total_count, delivered = fulfilment_meta['total_count'], fulfilment_meta['delivered']
    fulfillment_rate = (delivered * 100) / total_count
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

def update_resp_time(vendor):
    conditions = {
        'vendor': vendor,
        'acknowledgment_date__isnull': False,
    }
    diff_days_expression = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
    result = PurchaseOrder.objects.filter(**conditions).aggregate(avg_diff_days=Avg(diff_days_expression))['avg_diff_days']
    vendor.average_response_time = result.days
    vendor.save()

def update_avg_rating(vendor):
    avg_rating = PurchaseOrder.objects.filter(vendor=vendor).aggregate(avg_rating=Avg('quality_rating'))['avg_rating']
    vendor.quality_rating_avg = avg_rating
    vendor.save()
