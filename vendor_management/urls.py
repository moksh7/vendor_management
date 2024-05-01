from django.urls import path

from vendor_management import views

urlpatterns = [
    path('vendors', views.VendorListCreateView.as_view(), name='vendor_list_create'),
    path('vendors/<int:vendor_id>', views.VendorDetailUpdateView.as_view(), name='vendor_detail_update'),
]
