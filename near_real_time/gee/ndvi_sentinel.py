import ee
import numpy as np


class Sentinel2Ndvi:
    def __init__(self):
        self.polygon = None

    def addNDVI(self, image):
        scaled_b8 = image.select('B8').multiply(0.0001).add(0)
        scaled_b4 = image.select('B4').multiply(0.0001).add(0)
        ndvi = scaled_b8.subtract(scaled_b4).divide(scaled_b8.add(scaled_b4)).rename('NDVI')
        return image.addBands(ndvi)

    def mask_out(self, image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def download(self, polygon, startDate, endDate):
        self.polygon = ee.Geometry.Polygon(polygon)
        collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED') \
            .filterBounds(self.polygon) \
            .filterDate(startDate, endDate) \
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 1))
        sentinel_resault = []
        collection_size=collection.size().getInfo();
        if collection_size > 0:
            for image in collection.toList(collection.size()).getInfo():
                sentinel_image = ee.Image(image['id'])
                projection = sentinel_image.select(0).projection()
                transform = projection.getInfo()['transform']
                sentinel_image = self.addNDVI(sentinel_image).select(['NDVI'])
                date_string_sentinel = ee.Date(sentinel_image.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                masked_image = self.mask_out(sentinel_image)
                array_sentinel = masked_image.getInfo()
                array_sentinel = np.array(array_sentinel["properties"]["NDVI"])
                sentinel_resault.append(
                    {"ndvi": array_sentinel, "date": date_string_sentinel,"transform":transform ,"product": 'S2_SR_HARMONIZED'})
            return sentinel_resault
        else:
            raise Exception("No data found in the entered date range")