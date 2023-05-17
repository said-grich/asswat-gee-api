import ee
import numpy as np


class ModisLst:
    def __init__(self):

        self.polygon = None

    def mask_out(self, image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def download(self, polygon, startDate, endDate):
        self.polygon = ee.Geometry.Polygon(polygon)
        # Load the image collection
        collection = ee.ImageCollection('MODIS/006/MOD11A2') \
            .filterBounds(polygon) \
            .filterDate(startDate, startDate)

        # Select the desired band
        band_name = "LST_Day_1km"
        i = 0
        modis_resault = []
        # Check if the collection has any images
        if collection.size().getInfo() == 0:
            print("No images available for the specified region and time range.")
        else:
            for image in collection.toList(collection.size()).getInfo():
                image_modis = ee.Image(image['id']).select([band_name])
                date_string_modis = ee.Date(image_modis.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                acquisition_time = ee.Date(image_modis.get('system:time_start')).getInfo()
                masked_ = self.mask_out(image_modis)
                array_modis = np.array(masked_.getInfo()["properties"]["LST_Day_1km"])
                array_modis = np.where(array_modis == -999, None, array_modis)
                modis_resault.append({"lst": array_modis * 0.02, "date": date_string_modis, "product": 'MOD11A2',

                                      })
            return modis_resault
