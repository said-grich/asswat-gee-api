from django.urls import path
from .views import Landsat8NdviDownloadView, Sentinel2NdviDownloadView, Landsat8LSTDownloadView, ModisLSTDownloadView, \
    ModisNdviDownloadView

urlpatterns = [
    path('landsat/ndvi/', Landsat8NdviDownloadView.as_view(), name='landsat_ndvi_download'),
    path('landsat/lst/',  Landsat8LSTDownloadView.as_view(), name='landsat_lst_download'),
    path('sentinel2/ndvi/', Sentinel2NdviDownloadView.as_view(), name='landsat_ndvi_download'),
    path('modis/ndvi/', ModisNdviDownloadView.as_view(), name='landsat_ndvi_download'),
    path('modis/lst/', ModisLSTDownloadView.as_view(), name='landsat_ndvi_download'),
]
