import ee
import numpy as np


class ERA5_LAND:
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
        collection = ee.ImageCollection('ECMWF/ERA5_LAND/DAILY_AGGR') \
                        .filterBounds(self.polygon) \
                        .filterDate(self.start_date, self.end_date)
        er5_resault=[]
        # Check if the collection has any images
        if collection.size().getInfo() == 0:
            print("No images available for the specified region and time range.")
        else:
            for image in collection.toList(collection.size()).getInfo():
                era5_modis = ee.Image(image['id']).select([band])
                projection = era5_modis.select(0).projection()
                transform = projection.getInfo()['transform']
                date_string_era5 = ee.Date(era5_modis.get('system:time_start')).format('YYYY-MM-dd').getInfo()
                masked_=self.mask_out(era5_modis)
                array_era5=np.array(masked_.getInfo()["properties"][band]) 
                array_era5= np.where(array_era5 == -999, np.nan, array_era5)
                er5_resault.append({band: array_era5-273.5, "date": date_string_era5 ,"transform":transform ,"product":'ERA5'})
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
                