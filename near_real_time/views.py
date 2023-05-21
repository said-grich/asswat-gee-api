import base64
import numpy as np
import io
import matplotlib.pyplot as plt
import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import folium
from folium.plugins import Draw
from django.http import JsonResponse
from near_real_time.gee.SMAP10KM_soil_moisture import SMAP10KM_soil_moisture
from near_real_time.gee.SMAP_soil_moisture import SMAP_soil_moisture
from near_real_time.gee.era_5_land import ERA5_LAND
from near_real_time.gee.lst_landsat8 import Landsat8Lst
from near_real_time.gee.lst_modis import ModisLst
from near_real_time.gee.ndvi_landsat5 import Landsat5Ndvi
from near_real_time.gee.ndvi_landsat8 import Landsat8Ndvi
from near_real_time.gee.ndvi_modis import ModisNdvi
from near_real_time.gee.ndvi_sentinel import Sentinel2Ndvi
from near_real_time.gee.vv_sntinel1 import Sentinel1


def map_view(request):

    product_list = [
        "NDVI LANDSAT-5 (1984-012)",
        "NDVI LANDSAT-8 (2013-Present)",
        "LST LANDSAT-8 (2013-Present)",
        "NDVI MODIS (2013-Present)",
        "LST MODIS (2013-Present)",
        "NDVI SENTINEL-2 (2015-Present)",
        "SENTINEL-1 (2014-Present)",
        "ERA5-Land Daily Aggregated (1963-2023)",
    ]
    # Create a Folium map centered at a specific location
    m = folium.Map(location=[-8.469759582233934,
                             33.14811080869278], zoom_start=8, crs='EPSG4326', control_scale=True)
    # Add a satellite tile layer to the map
    folium.TileLayer(
        'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite', name='Satellite').add_to(m)

    # Add a Draw control to enable polygon selection
    draw = Draw(export=True)
    draw.add_to(m)

    # Save the map as an HTML file
    m.save('map.html')
    context = {
        'product_list': product_list,
    }
    # Render the HTML file in the Django template
    return render(request, 'map.html' ,context)


def to_image(numpy_img):
    # Normalize the NDVI data to 0-255 range
    normalized_img = (numpy_img+1) * 127.5
    normalized_img = normalized_img.astype('uint8')

    # Create a figure and axis
    fig, ax = plt.subplots()
    # Display the NDVI image
    ax.imshow(normalized_img, cmap='RdYlGn', vmin=0, vmax=255)

    # Remove the axis ticks and labels
    ax.set_xticks([])
    ax.set_yticks([])
    ax.axis('off')

    # Convert the plot to a base64-encoded PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0)
    buffer.seek(0)

    # Convert the buffer to base64-encoded bytes
    image_bytes = buffer.getvalue()
    buffer.close()
    base64_image = base64.b64encode(image_bytes).decode('utf-8')

    # Construct the data URI string
    image_uri = f"data:image/png;base64,{base64_image}"

    return image_uri


def get_polygon_coordinates(request):
    if request.method == 'POST':
        coordinates = request.POST.get('coordinates')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        coordinates = json.loads(coordinates)
        selectedProduct = request.POST.get('selectedProduct')
        
        product = None
        variable=None
        title=None
        if selectedProduct == 'NDVI LANDSAT-5 (1984-012)':
            title="Ndvi By Date"
            variable="ndvi"
            # Handle NDVI LANDSAT-5 (1984-012) case
            product = Landsat5Ndvi()
            result = product.download(coordinates, start_date, end_date)
            numpy_image = result[0]["ndvi"]
            
            
            
        elif selectedProduct == 'NDVI LANDSAT-8 (2013-Present)':
            title="Ndvi By Date"
            variable="ndvi"
            # Handle NDVI LANDSAT-8 (2013-Present) case
            product = Landsat8Ndvi()
            result = product.download(coordinates, start_date, end_date)
        
            numpy_image = result[0]["ndvi"]
        elif selectedProduct == 'LST LANDSAT-8 (2013-Present)':
            title="LST By Date"
            variable="lst"
            
            product = Landsat8Lst()

            # Handle LST LANDSAT-8 (2013-Present) case
            result = product.download(coordinates, start_date, end_date)
            numpy_image = result[0]["lst"]
        elif selectedProduct == 'NDVI MODIS (2013-Present)':
            product = ModisNdvi()

            title="Ndvi By Date"
            variable="ndvi"
            # Handle NDVI MODIS (2013-Present) case
            result = product.download(coordinates, start_date, end_date)
            numpy_image = result[0]["ndvi"]
        elif selectedProduct == 'LST MODIS (2013-Present)':
            title="LST By Date"
            variable="lst"
            # Handle LST MODIS (2013-Present) case
            product = ModisLst()
            result = product.download(coordinates, start_date, end_date)
            numpy_image = result[0]["lst"]
        elif selectedProduct == 'NDVI SENTINEL-2 (2015-Present)':
            title="Ndvi By Date"
            variable="ndvi"
            # Handle NDVI SENTINEL-2 (2015-Present) case
            product = Sentinel2Ndvi()
            result = product.download(coordinates, start_date, end_date)
            numpy_image = result[0]["ndvi"]
        elif selectedProduct == 'SENTINEL-1 (2014-Present)':
            pass
            product = Sentinel1()
        elif selectedProduct == 'ERA5-Land Daily Aggregated (1963-2023)':
            pass
            # Handle ERA5-Land Daily Aggregated (1963-2023) case
            product = Sentinel1()
        else:
            # Handle unknown product case
            raise ValueError('No product selected!')


        numpy_image = np.where(numpy_image == None, 0, numpy_image)

        ndvi_data = {}
        for data in result:
            tmp_array = np.where(data[variable] == None, np.nan, data[variable])
            ndvi_data[data['date']] = np.nanmean(tmp_array)
        # Sort the NDVI data by date
        sorted_ndvi_data = {k: v for k, v in sorted(ndvi_data.items(), key=lambda item: item[0])}


        # Convert the NumPy array to a PIL Image and save it temporarily
        image_uri = to_image(numpy_image)
        transform=result[0]['transform']

        # Return the image URI and NDVI data in the JSON response
        return JsonResponse({'image_uri': image_uri, 'ndvi_data': sorted_ndvi_data, "transform":transform , "title":title , "variable":variable}   )
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)


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
        landsatLst = Landsat8Lst()
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


class Sentinel1DownloadView(APIView):
    def post(self, request):
        sentinel1 = Sentinel1()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        band = request.data.get('band', None)
        result = sentinel1.download(polygon, band, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class ERA5_LAND_D_DownloadView(APIView):
    def post(self, request):
        era5 = ERA5_LAND()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        bands = request.data.get('bands', None)
        result = era5.download(polygon, bands, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class SMAP_DownloadView(APIView):
    def post(self, request):
        smap_soil_moisture = SMAP_soil_moisture()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = smap_soil_moisture.download(
            polygon, ["ssm"], start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)


class SMAP10KM_soil_moistureView(APIView):
    def post(self, request):
        smap_soil_moisture = SMAP10KM_soil_moisture()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        result = smap_soil_moisture.download(
            polygon, ["ssm"], start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)
