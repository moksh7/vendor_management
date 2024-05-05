from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vendor_management.models import Vendor
from vendor_management.serializers import VendorPerformanceSerializer


class VendorPerformanceView(GenericAPIView):
    serializer_class = VendorPerformanceSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        '''
        Fetch vendor performance stats
        '''
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if not vendor:
            return Response({'error': 'Invalid vendor_id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)
