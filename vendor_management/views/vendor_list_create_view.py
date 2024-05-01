from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from vendor_management.models import Vendor
from vendor_management.serializers import VendorSerializer


class VendorListCreateView(GenericAPIView):
    serializer_class = VendorSerializer

    def post(self, request):
        '''
        Create vendor instance with validations applied from VendorSerializer
        '''
        serializer = VendorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        '''
        Get list of all vendors.
        '''
        vendor_list = Vendor.objects.all()
        serializer = VendorSerializer(vendor_list, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
