from django.urls import path
from .views import ERA5_LAND_D_DownloadView, Landsat8NdviDownloadView, Sentinel1DownloadView, Sentinel2NdviDownloadView, Landsat8LSTDownloadView, ModisLSTDownloadView, \
    ModisNdviDownloadView, map_view, get_polygon_coordinates

urlpatterns = [
    path('landsat/ndvi/', Landsat8NdviDownloadView.as_view(),
         name='landsat_ndvi_download'),
    path('landsat/lst/', Landsat8LSTDownloadView.as_view(),
         name='landsat_lst_download'),
    path('sentinel2/ndvi/', Sentinel2NdviDownloadView.as_view(),
         name='sentinel_ndvi_download'),
    path('modis/ndvi/', ModisNdviDownloadView.as_view(),
         name='modis_ndvi_download'),
    path('modis/lst/', ModisLSTDownloadView.as_view(), name='modis_lst_download'),
    path('sentinel1/', Sentinel1DownloadView.as_view(),
         name='sentinel_download'),
    path('era5/', ERA5_LAND_D_DownloadView.as_view(),
         name='era_download'),
    path('', map_view, name='gee_map'),
    
    path('get_polygon_coordinates/', get_polygon_coordinates,
         name='get_polygon_coordinates'),
]
