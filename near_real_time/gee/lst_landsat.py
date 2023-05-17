import ee
import numpy as np


class LandsatLst:
    def __init__(self):
        self.polygon = None
    def mask_out(self,image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def addLST(self,image):
        st_b10 = image.select('ST_B10').multiply(0.00341802).add(149.0)
        emissivity = image.select('ST_EMIS').multiply(0.0001)
        qa = image.select('QA_PIXEL')  # Assuming L1 QA_Pixel band is available for quality information

        # Apply valid range mask to exclude invalid values
        valid_range_mask = st_b10.gt(0).And(st_b10.lt(65535))

        # Apply quality mask to exclude low-quality pixels
        quality_mask = qa.bitwiseAnd(0x03).eq(0)  # Assuming 00-Valid data, 01-Cloud, 10-Cloud shadow, 11-Snow/Ice

        # Combine masks
        valid_data_mask = valid_range_mask.And(quality_mask)

        # Apply emissivity correction
        st_b10_corrected = st_b10.multiply(emissivity)

        # Calculate LST
        lst = st_b10_corrected.subtract(273.15)

        # Apply masks to LST
        lst = lst.updateMask(valid_data_mask)

        # Add the corrected LST band to the image
        image_with_corrected_lst = image.addBands(lst.rename('LST'))

        return image_with_corrected_lst

    def mask_out(self, image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def download(self, polygon, startDate, endDate):
        self.polygon = ee.Geometry.Polygon(polygon)
        # Load the image collection
        # Create an image collection and apply filters
        collection = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2') \
            .filterBounds(self.polygon) \
            .filterDate(startDate, endDate) \
            .filterMetadata('CLOUD_COVER', 'less_than', 20)

        # Empty list to store results
        landsat_result = []

        # Iterate over the collection and calculate NDVI mean and LST for each image
        for image in collection.toList(collection.size()).getInfo():
            image = ee.Image(image['id'])
            image = self.addLST(image).select(['LST'])
            date_string = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd').getInfo()

            masked_image = self.mask_out(image)
            array = masked_image.getInfo()
            array = np.array(array["properties"]["LST"])
            array = np.where(array == -999, None, array)
            landsat_result.append({"lst": array, "date": date_string, "product": 'T1_L2'})

        return landsat_result
