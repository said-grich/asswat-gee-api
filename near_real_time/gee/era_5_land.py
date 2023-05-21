import ee
import numpy as np


class ERA5_LAND:
    def __init__(self) -> None:
        self.polygon=None
        self.varialbles_list=[]
        self.start_date=None
        self.end_date=None
        

    def mask_out(self,image):
        clipped_image = image.clip(self.polygon)
        samples = clipped_image.unmask(-999).sampleRectangle(region=self.polygon, defaultValue=-999)
        return samples

    def download_band(self,band):
        # Load the image collection
        collection = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR') \
                        .filterBounds(self.polygon) \
                        .filterDate(self.start_date, self.end_date)
        er5_resault=[]
        # Check if the collection has any images
        if collection.size().getInfo() == 0:
            print("No images available for the specified region and time range.")
        else:
            for image in collection.toList(collection.size()).getInfo():
                image_modis = ee.Image(image['id']).select([band])
                date_string_era5 = ee.Date(image_modis.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                masked_=self.mask_out(image_modis)
                array_era5=np.array(masked_.getInfo()["properties"][band]) 
                array_era5= np.where(array_era5 == -999, np.nan, array_era5)
                er5_resault.append({band: array_era5-273.5, "date": date_string_era5 , "product":'MOD11A2'})
            return er5_resault
    
    def download(self,polygon,variables_lists,start_date,end_date):
        self.polygon = ee.Geometry.Polygon(polygon)
        self.varialbles_list=variables_lists
        self.start_date=start_date
        self.end_date=end_date
        variables_resualt={}
        for band in variables_lists:
            variables_resualt[band]=self.download_band(band)            
        return variables_resualt             
                