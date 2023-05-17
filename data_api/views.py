from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from data_api.geojson_db_pipline import GeojsonDbPipline


# Create your views here.

class Ndvi(APIView):
    def post(self, request):
        geometry = request.data["geometry"]
        pipline = GeojsonDbPipline("assewat", "ndvi")
        result = pipline.searchNdviPipLine(geometry)
        pp = pipline.polygon_4326ToPolygon_32629(geometry)

        # Set the page size and create a paginator object
        page_size = 5  # Change this to the desired page size
        paginator = Paginator(result, page_size)

        # Get the current page number from the request query parameters
        page_number = request.query_params.get('page', 1)

        # Get the page object for the current page number
        page_obj = paginator.get_page(page_number)

        # Create a list to store the ndvi values for the current page
        ndvi_list = []
        for item in page_obj:
            ndvi = pipline.clipRaster(item["path"], pp)
            ndvi_list.append({"ndvi":ndvi.tolist(),"date":item["date"]})

        # Set the response headers and content type
        response = Response(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="ndvi_list.json"'

        # Set the pagination headers in the response
        response['X-Total-Count'] = paginator.count
        response['X-Total-Pages'] = paginator.num_pages
        response['X-Page-Number'] = page_number
        response['X-Page-Size'] = page_size

        # Set the response content
        response.data = {"ndvi_list": ndvi_list}

        return response
