from django.urls import path

from vendor_management import views

urlpatterns = [
    path('vendors', views.VendorListCreateView.as_view(), name='vendor_list_create'),
    path('vendors/<int:vendor_id>', views.VendorDetailUpdateView.as_view(), name='vendor_detail_update'),
    path('purchase_orders', views.POCreateView.as_view(), name='po_list_create'),
    path('purchase_orders/<int:po_id>', views.PODetailUpdate.as_view(), name='po_detail_update'),
    path('purchase_orders/<int:po_id>/acknowledge', views.AckPO.as_view(), name='po_acknowledge'),
    path('vendors/<int:vendor_id>/performance)', views.VendorPerformanceView.as_view(), name='vendor_performance'),
]
