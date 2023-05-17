import ee
import geemap
import time

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
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 0.1))
        sentinel_resault = []
        for image in collection.toList(collection.size()).getInfo():
            sentinel_image = ee.Image(image['id'])
            sentinel_image = self.addNDVI(sentinel_image).select(['NDVI'])
            date_string_sentinel = ee.Date(sentinel_image.get('system:time_start')).format('YYYY-MM-dd').getInfo()
            masked_image = self.mask_out(sentinel_image)
            array_sentinel = masked_image.getInfo()
            array_sentinel = np.array(array_sentinel["properties"]["NDVI"])
            array_sentinel = np.where(array_sentinel == -999,None, array_sentinel)
            sentinel_resault.append(
                {"ndvi": array_sentinel, "date": date_string_sentinel, "product": 'S2_SR_HARMONIZED'})
        return sentinel_resault
