from django.utils import timezone
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vendor_management.models import PurchaseOrder
from vendor_management.serializers import POListSerializer, POUpdateSerializer
from vendor_management.signals import metric_update



class PODetailUpdate(GenericAPIView):
    serializer_class = POUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, po_id):
        '''
        Get detail about a purchase order based on po_id
        '''
        po = PurchaseOrder.objects.filter(id=po_id).first()
        if not po:
            return Response({'error': 'Invalid po_id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = POListSerializer(po)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, po_id):
        po = PurchaseOrder.objects.filter(id=po_id).first()
        if not po:
            return Response({'error': 'Invalid po_id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = POUpdateSerializer(po, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.data.get('status') == 'completed':
            metric_update.send(__class__, event='delivered', vendor=po.vendor)
        if request.data.get('quality_rating'):
            metric_update.send(__class__, event='rating', vendor=po.vendor)
        return Response({'data': 'PO updated'}, status=status.HTTP_200_OK)

    def delete(self, request, po_id):
        '''
        Delete a vendor based on its ID
        '''
        po = PurchaseOrder.objects.filter(id=po_id).first()
        if not po:
            return Response({'error': 'Invalid po_id'}, status=status.HTTP_400_BAD_REQUEST)
        po.delete()
        return Response({'data': 'Purchase order deleted'}, status=status.HTTP_200_OK)


class AckPO(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, po_id):
        po = PurchaseOrder.objects.filter(id=po_id).first()
        if not po:
            return Response({'error': 'Invalid po_id'}, status=status.HTTP_400_BAD_REQUEST)
        elif po.acknowledgment_date is not None:
            return Response({'error': 'PO Already acknowledged'}, status=status.HTTP_400_BAD_REQUEST)
        po.acknowledgment_date = timezone.now()
        po.save()
        metric_update.send(__class__, event='ack', vendor=po.vendor)
        return Response({'data': 'Order acknowledged'}, status=status.HTTP_200_OK)