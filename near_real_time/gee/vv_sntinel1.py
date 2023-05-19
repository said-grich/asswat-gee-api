import ee
import pandas as pd
import numpy as np

class Sentinel1:
    def __init__(self):
        ee.Initialize()
        self.polygon = None
    def mask_out(self,image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples
    def download(self,polygon,band,startDate,endDate):
        results_ = []
        self.polygon = ee.Geometry.Polygon(polygon)
        collection = ee.ImageCollection('COPERNICUS/S1_GRD')\
                        .filterBounds(self.polygon) \
                        .filterDate(startDate, endDate)
        collection_size=collection.size().getInfo();
        
        if collection_size > 0:
            for image in collection.toList(collection_size).getInfo():
                sentinel_image = ee.Image(image['id']).select([band])
                date_string_sentinel = ee.Date(sentinel_image.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                masked_image = self.mask_out(sentinel_image)
                array_sentinel = masked_image.getInfo()
                array_sentinel = np.array(array_sentinel["properties"][band])
                array_sentinel = np.where(array_sentinel == -999, np.nan, array_sentinel)
                results_.append({band: array_sentinel, "date": date_string_sentinel, "product": 'COPERNICUS/S1_GRD'})
            return results_
        else:
            raise Exception("No data found in the entered date range")