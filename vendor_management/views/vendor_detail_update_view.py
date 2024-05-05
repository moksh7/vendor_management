from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from vendor_management.models import Vendor
from vendor_management.serializers import VendorSerializer


class VendorDetailUpdateView(GenericAPIView):
    serializer_class = VendorSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, vendor_id):
        '''
        Get detail about a single vendor based on vendor_id
        '''
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if not vendor:
            return Response({'error': 'Invalid vendor_id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, vendor_id):
        '''
        Update name, contact_details and address of a vendor. Partial updates are allowed.
        '''
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if not vendor:
            return Response({'error': 'Invalid vendor_id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, vendor_id):
        '''
        Delete a vendor based on its ID
        '''
        vendor = Vendor.objects.filter(id=vendor_id).first()
        if not vendor:
            return Response({'error': 'Invalid vendor_id'}, status=status.HTTP_400_BAD_REQUEST)
        vendor.delete()
        return Response({'data': 'Vendor deleted'}, status=status.HTTP_400_BAD_REQUEST)
