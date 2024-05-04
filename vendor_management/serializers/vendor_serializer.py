from rest_framework import serializers

from vendor_management.models import Vendor


class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['id', 'vendor_code', 'name', 'contact_details', 'address']
        read_only_fields = ('vendor_code',)

    def create(self, validated_data):
        vendor = super().create(validated_data)
        vendor.vendor_code = 'VC{:02d}'.format(vendor.id)
        vendor.save()
        return vendor


class VendorPerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
