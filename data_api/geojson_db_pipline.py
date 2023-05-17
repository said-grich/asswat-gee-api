import pymongo
import pandas as pd
import rasterio
from shapely.geometry import Polygon
import pyproj
from shapely.ops import transform


class GeojsonDbPipline():
    def __init__(self, db_name, collection_name):
        self.client = pymongo.MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def searchNdviPipLine(self, polygon):
        pipeline = [
            # Match documents that intersect with the small polygon
            {"$match": {"geometry": {"$geoIntersects": {"$geometry": polygon}}}},
            # Unwind the ndvi array
            {"$unwind": "$ndvi"},
            # Match ndvi array elements that intersect with the small polygon
            {"$match": {"ndvi.geometry": {"$geoIntersects": {"$geometry": polygon}}}},
            # Project only the id, ndvi.path, and ndvi.date fields
            {"$project": {"_id": 0, "ndvi.geometry": 1, "ndvi.path": 1, "ndvi.date": 1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        result = []
        for doc in cursor:
            result.append(doc["ndvi"])
        return result

    def polygon_4326ToPolygon_32629(self, polygon_4326):
        # Define the EPSG codes for the source and target coordinate reference systems
        src_crs = "EPSG:4326"
        dst_crs = "EPSG:32629"

        # Define the small_polygon geometry in EPSG:4326
        coords = polygon_4326["coordinates"][0]

        # Create a Polygon object from the coordinates
        small_polygon_geom = Polygon(coords)

        # Create a pyproj transformer object to transform from EPSG:4326 to EPSG:32629
        transformer = pyproj.Transformer.from_crs(src_crs, dst_crs, always_xy=True)

        # Use shapely.ops.transform to apply the coordinate transformation to the small_polygon geometry
        polygon_32629 = transform(lambda x, y: transformer.transform(x, y), small_polygon_geom)
        return polygon_32629

    def clipRaster(self, raster_path, polygon_32629):
        with rasterio.open(raster_path) as rasterfile:
            # Get the row and column indices of the pixels that intersect with the small polygon
            row_start, col_start = rasterfile.index(polygon_32629.bounds[0], polygon_32629.bounds[3])
            row_stop, col_stop = rasterfile.index(polygon_32629.bounds[2], polygon_32629.bounds[1])

            # Define the window to read
            window = rasterio.windows.Window.from_slices((row_start, row_stop + 1), (col_start, col_stop + 1))

            # Read the raster data within the window
            data = rasterfile.read(1, window=window)
            return data

    def plot_ndvi_per_date(self, rs, polygon_32629):
        resault_lits = []
        for dict_ in rs:
            cliped_ndvi = test.clipRaster(dict_["path"], polygon_32629)
            resault_lits.append({"date": dict_["date"], "ndvi": cliped_ndvi.mean()})
        return pd.DataFrame(resault_lits)