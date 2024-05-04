from rest_framework import serializers

from vendor_management.models import PurchaseOrder


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'vendor', 'order_date', 'items', 'quantity', 'issue_date', 'po_number', 'status']
        read_only_fields = ('order_date', 'issue_date', 'po_number', 'status')

    def create(self, validated_data):
        po = super().create(validated_data)
        po.po_number = 'PO{:02d}'.format(po.id)
        po.save()
        return po

class POListSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class POUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseOrder
        fields = ['est_delivery_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating']


    def validate(self, data):
        if (data.get('status') == 'completed' and not data.get('delivery_date')) or (data.get('delivery_date') and data.get('status') != 'completed'):
            raise serializers.ValidationError("delivery date must be set at time of completing the PO")
        return data