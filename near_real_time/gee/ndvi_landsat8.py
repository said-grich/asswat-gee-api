import ee
import numpy as np


class Landsat8Ndvi:
    def __init__(self):

        self.polygon = None

    def addNDVI(self, image):
        scaled_sr_b5 = image.select('SR_B5').multiply(2.75e-5).add(-0.2)
        scaled_sr_b4 = image.select('SR_B4').multiply(2.75e-5).add(-0.2)

        # Mask non-corrected values
        qa_aerosol = image.select('SR_QA_AEROSOL')
        valid_mask = qa_aerosol.bitwiseAnd(1 << 1).eq(0)  # Valid aerosol mask
        scaled_sr_b5 = scaled_sr_b5.updateMask(valid_mask)
        scaled_sr_b4 = scaled_sr_b4.updateMask(valid_mask)

        ndvi = scaled_sr_b5.subtract(scaled_sr_b4).divide(scaled_sr_b5.add(scaled_sr_b4)).rename('NDVI')
        return image.addBands(ndvi)

    def mask_out(self, image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def download(self, polygon, startDate, endDate):
        self.polygon = ee.Geometry.Polygon(polygon)

        # Create an image collection and apply filters
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(self.polygon) \
            .filterDate(startDate, endDate) \
            .filterMetadata('CLOUD_COVER', 'less_than', 20)

        # Empty list to store results
        landsat_resault = []

        # Iterate over the collection and calculate NDVI mean and LST for each image
        for image in collection.toList(collection.size()).getInfo():
            image = ee.Image(image['id'])
            image = self.addNDVI(image).select(['NDVI'])
            date_string = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd').getInfo()

            masked_image = self.mask_out(image)
            array = masked_image.getInfo()
            array = np.array(array["properties"]["NDVI"])
            array = np.where(array == -999, None, array)
            landsat_resault.append({"ndvi": array, "date": date_string, "product": 'T1_L2'})
        return landsat_resault
