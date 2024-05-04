from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from vendor_management.models import PurchaseOrder
from vendor_management.serializers import PurchaseOrderCreateSerializer, POListSerializer



class POCreateView(GenericAPIView):
    serializer_class = PurchaseOrderCreateSerializer

    def post(self, request):
        '''
        Create Purchase order  with validations applied from PurchaseOrderCreateSerializer
        '''
        serializer = PurchaseOrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        '''
        List all purchase orders and filter based on vendor_id
        query_param: vendor_id
        '''
        vendor_id = request.query_params.get('vendor_id', None)
        if vendor_id and not vendor_id.isnumeric():
            return Response({"error": 'vendor_id should be numeric'}, status=status.HTTP_400_BAD_REQUEST)
        po = PurchaseOrder.objects.all()
        if vendor_id:
            po = po.filter(vendor_id=vendor_id)
        serializer = POListSerializer(po, many=True)
        return Response(serializer.data)
