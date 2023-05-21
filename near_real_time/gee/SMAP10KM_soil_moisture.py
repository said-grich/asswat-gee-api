import ee
import numpy as np


class SMAP10KM_soil_moisture:
    def __init__(self) -> None:
        self.polygon=None
        self.varialbles_list=[]
        self.start_date=None
        self.end_date=None
        

    def mask_out(self,image):
        bounds = self.polygon.bounds()
        clipped_image = image.clip(bounds)
        samples = clipped_image.unmask(-999).sampleRectangle(region=bounds, defaultValue=-999)
        return samples

    def download_band(self,band):
        # Load the image collection
        collection = ee.ImageCollection('NASA_USDA/HSL/SMAP10KM_soil_moisture') \
                        .filterBounds(self.polygon) \
                        .filterDate(self.start_date, self.end_date)
        smap_resault=[]
        # Check if the collection has any images
        if collection.size().getInfo() == 0:
            print("No images available for the specified region and time range.")
        else:
            for image in collection.toList(collection.size()).getInfo():
                image_smap = ee.Image(image['id']).select([band])
                date_string_smap = ee.Date(image_smap.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                masked_=self.mask_out(image_smap)
                array_smap=np.array(masked_.getInfo()["properties"][band]) 
                smap_resault.append({band: array_smap, "date": date_string_smap , "product":'SMAP10'})
            return smap_resault
    
    def download(self,polygon,variables_lists,start_date,end_date):
        self.polygon = ee.Geometry.Polygon(polygon)
        self.varialbles_list=variables_lists
        self.start_date=start_date
        self.end_date=end_date
        variables_resualt={}
        for band in variables_lists:
            variables_resualt[band]=self.download_band(band)            
        return variables_resualt             
                