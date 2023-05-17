from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from near_real_time.gee.lst_landsat import LandsatLst
from near_real_time.gee.lst_modis import ModisLst
from near_real_time.gee.ndvi_landsat8 import Landsat8Ndvi
from near_real_time.gee.ndvi_modis import ModisNdvi
from near_real_time.gee.ndvi_sentinel import Sentinel2Ndvi


class Landsat8NdviDownloadView(APIView):
    def post(self, request):
        landsat_ndvi = Landsat8Ndvi()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = landsat_ndvi.download(polygon, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class Landsat8LSTDownloadView(APIView):
    def post(self, request):
        landsatLst = LandsatLst()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = landsatLst.download(polygon, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class Sentinel2NdviDownloadView(APIView):
    def post(self, request):
        sentinel2Ndvi = Sentinel2Ndvi()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = sentinel2Ndvi.download(polygon, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class ModisNdviDownloadView(APIView):
    def post(self, request):
        modisNdvi = ModisNdvi()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = modisNdvi.download(polygon, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class ModisLSTDownloadView(APIView):
    def post(self, request):
        modisLst = ModisLst()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = modisLst.download(polygon, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)
