import json

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
import folium
from folium.plugins import Draw

from django.http import JsonResponse

from near_real_time.gee.lst_landsat import LandsatLst
from near_real_time.gee.lst_modis import ModisLst
from near_real_time.gee.ndvi_landsat8 import Landsat8Ndvi
from near_real_time.gee.ndvi_modis import ModisNdvi
from near_real_time.gee.ndvi_sentinel import Sentinel2Ndvi


def map_view(request):
    # Create a Folium map centered at a specific location
    m = folium.Map(location=[-8.469759582233934,
                             33.14811080869278], zoom_start=8, crs='EPSG4326', control_scale=True)
    # Add a satellite tile layer to the map
    folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite', name='Satellite').add_to(m)

    # Add a Draw control to enable polygon selection
    draw = Draw(export=True)
    draw.add_to(m)

    # Save the map as an HTML file
    m.save('map.html')

    # Render the HTML file in the Django template
    return render(request, 'map.html')


import matplotlib.pyplot as plt
import io

import io
import matplotlib.pyplot as plt
import numpy as np
import base64


def to_image(numpy_img):
    # Normalize the NDVI data to 0-255 range
    normalized_img = (numpy_img + 1) * 127.5
    normalized_img = normalized_img.astype('uint8')

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(5, 5))

    # Display the NDVI image
    ax.imshow(normalized_img,  vmin=0, vmax=255)

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
        print(coordinates)
        sentinel2Ndvi = Sentinel2Ndvi()

        result = sentinel2Ndvi.download(coordinates, start_date, end_date)
        numpy_image = result[0]["ndvi"]
        # Create a boolean mask for NaN values
        mask = np.isnan(numpy_image)

        # Replace NaN values with 0 using the mask
        numpy_image[mask] = 0

        ndvi_data = {}
        for data in result:
            ndvi_data[data['date']] = np.nanmean(data['ndvi'])

        # Convert the NumPy array to a PIL Image and save it temporarily
        image_uri = to_image(numpy_image)
        
        # Return the image URI and NDVI data in the JSON response
        return JsonResponse({'image_uri': image_uri, 'ndvi_data': ndvi_data})
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



class Sentinel1DownloadView(APIView):
    def post(self, request):
        modisLst = ModisLst()
        polygon = request.data.get('polygon', None)
        start_date = request.data.get('start_date', None)
        end_date = request.data.get('end_date', None)
        band=request.data.get('band',None)
        result = modisLst.download(polygon, start_date, end_date)
        return Response(result, status=status.HTTP_200_OK)
