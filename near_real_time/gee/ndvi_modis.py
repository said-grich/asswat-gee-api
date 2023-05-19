import ee
import numpy as np


class ModisNdvi:
    def __init__(self):
        self.polygon = None

    def mask_out(self, image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def download(self, polygon, startDate, endDate):
        self.polygon = ee.Geometry.Polygon(polygon)
        # Load the image collection
        collection = ee.ImageCollection('MODIS/006/MOD13Q1') \
            .filterBounds(self.polygon) \
            .filterDate(startDate, endDate)

        # Select the desired band
        band_name = "NDVI"
        modis_resault = []
        # Check if the collection has any images
        if collection.size().getInfo() == 0:
            raise Exception("No data found in the entered date range")
        else:
            for image in collection.toList(collection.size()).getInfo():
                image_modis = ee.Image(image['id']).select([band_name])
                date_string_modis = ee.Date(image_modis.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                masked_ = self.mask_out(image_modis)
                array_modis = np.array(masked_.getInfo()["properties"]["NDVI"])
                array_modis = array_modis * 0.0001
                array_modis = np.where(array_modis == -999, np.nan, array_modis)
                
                modis_resault.append({"ndvi": array_modis, "date": date_string_modis, "product": 'MOD11A1'})
            return modis_resault
