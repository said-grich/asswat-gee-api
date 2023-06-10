Landsat8Ndvi
This class provides methods to download NDVI (Normalized Difference Vegetation Index) data from Landsat 8 images.

Methods
addNDVI(image)
Calculates the NDVI for the given Landsat 8 image.

Parameters:

image: An Earth Engine image object representing a Landsat 8 image.
Returns:

An Earth Engine image with the NDVI band added.
mask_out(image)
Masks out the image based on a specified polygon.

Parameters:

image: An Earth Engine image object.
Returns:

A masked image.
download(polygon, startDate, endDate)
Downloads Landsat 8 NDVI data within a specified date range and polygon.

Parameters:

polygon: A list of coordinate points representing the polygon.
startDate: The start date of the data acquisition period (e.g., 'YYYY-MM-dd').
endDate: The end date of the data acquisition period (e.g., 'YYYY-MM-dd').
Returns:

A list of dictionaries, where each dictionary represents an NDVI result with the following keys:
'ndvi': The NDVI values as a numpy array.
'date': The date of the NDVI result (e.g., 'YYYY-MM-dd').
'transform': The coordinate transformation information.
'product': The Landsat product type ('T1_L2').
//----------------------------------------------------------------------------------------------------//
ModisNdvi
This class provides methods to download NDVI data from MODIS (Moderate Resolution Imaging Spectroradiometer) images.

Methods
mask_out(image)
Masks out the image based on a specified polygon.

Parameters:

image: An Earth Engine image object.
Returns:

A masked image.
download(polygon, startDate, endDate)
Downloads MODIS NDVI data within a specified date range and polygon.

Parameters:

polygon: A list of coordinate points representing the polygon.
startDate: The start date of the data acquisition period (e.g., 'YYYY-MM-dd').
endDate: The end date of the data acquisition period (e.g., 'YYYY-MM-dd').
Returns:

A list of dictionaries, where each dictionary represents an NDVI result with the following keys:
'ndvi': The NDVI values as a numpy array.
'date': The date of the NDVI result (e.g., 'YYYY-MM-dd').
'transform': The coordinate transformation information.
'product': The MODIS product type ('MOD11A1').

//----------------------------------------------------------------------------------------------------//
Landsat5Ndvi
This class provides methods to download NDVI data from Landsat 5 images.

Methods
addNDVI(image)
Calculates the NDVI for the given Landsat 5 image.

Parameters:

image: An Earth Engine image object representing a Landsat 5 image.
Returns:

An Earth Engine image with the NDVI band added.
mask_out(image)
Masks out the image based on a specified polygon.

Parameters:

image: An Earth Engine image object.
Returns:

A masked image.
download(polygon, startDate, endDate)
Downloads Landsat 5 NDVI data within a specified date range and polygon.

Parameters:

polygon: A list of coordinate points representing the polygon.
startDate: The start date of the data acquisition period (e.g., 'YYYY-MM-dd').
endDate: The end date of the data acquisition period (e.g., 'YYYY-MM-dd').
Returns:

A list of dictionaries, where each dictionary represents an NDVI result with the following keys:
'ndvi': The NDVI values as a numpy array.
'date': The date of the NDVI result (e.g., 'YYYY-MM-dd').
'transform': The coordinate transformation information.
'product': The Landsat product type ('T1_L2').

//----------------------------------------------------------------------------------------------------//
Sentinel2Ndvi
This class provides methods to download NDVI data from Sentinel-2 images.

Methods
addNDVI(image)
Calculates the NDVI for the given Sentinel-2 image.

Parameters:

image: An Earth Engine image object representing a Sentinel-2 image.
Returns:

An Earth Engine image with the NDVI band added.
mask_out(image)
Masks out the image based on a specified polygon.

Parameters:

image: An Earth Engine image object.
Returns:

A masked image.
download(polygon, startDate, endDate)
Downloads Sentinel-2 NDVI data within a specified date range and polygon.

Parameters:

polygon: A list of coordinate points representing the polygon.
startDate: The start date of the data acquisition period (e.g., 'YYYY-MM-dd').
endDate: The end date of the data acquisition period (e.g., 'YYYY-MM-dd').
Returns:

A list of dictionaries, where each dictionary represents an NDVI result with the following keys:
'ndvi': The NDVI values as a numpy array.
'date': The date of the NDVI result (e.g., 'YYYY-MM-dd').
'transform': The coordinate transformation information.
'product': The Sentinel-2 product type ('S2_SR_HARMONIZED').

//----------------------------------------------------------------------------------------------------//
Landsat8Lst
Input:
polygon: A list of coordinates representing the polygon geometry to define the region of interest.
startDate: The start date of the date range for image retrieval, in the format "YYYY-MM-dd".
endDate: The end date of the date range for image retrieval, in the format "YYYY-MM-dd".
Output:
The download() method returns a list of dictionaries, where each dictionary represents an image within the specified date range and polygon. Each dictionary contains the following information:

"lst": An array representing the Land Surface Temperature (LST) values for the image. The LST values are in degrees Celsius.
"date": The date of the image in the format "YYYY-MM-dd".
"transform": The transformation matrix associated with the image.
"product": The product type, which in this case is 'T1_L2' indicating Landsat 8 data.
Functions:
mask_out(image): Clips the input image to the specified polygon and applies a mask to exclude invalid or masked pixels. It returns the masked image.

addLST(image): Calculates the Land Surface Temperature (LST) from the input image by applying various masks and corrections. It returns the input image with an added LST band.

download(polygon, startDate, endDate): Downloads Landsat 8 data within the specified date range and polygon. It retrieves the LST values for each image, applies masking and corrections, and returns a list of dictionaries representing the images.
//----------------------------------------------------------------------------------------------------//
ModisLst
Input:
polygon: A list of coordinates representing the polygon geometry to define the region of interest.
startDate: The start date of the date range for image retrieval, in the format "YYYY-MM-dd".
endDate: The end date of the date range for image retrieval, in the format "YYYY-MM-dd".
Output:
The download() method returns a list of dictionaries, where each dictionary represents an image within the specified date range and polygon. Each dictionary contains the following information:

"lst": An array representing the Land Surface Temperature (LST) values for the image. The LST values are in degrees Celsius.
"date": The date of the image in the format "YYYY-MM-dd".
"transform": The transformation matrix associated with the image.
"product": The product type, which in this case is 'MOD11A2' indicating MODIS data.
Functions:
mask_out(image): Clips the input image to the specified polygon and applies a mask to exclude invalid or masked pixels. It returns the masked image.

download(polygon, startDate, endDate): Downloads MODIS data within the specified date range and polygon. It retrieves the LST values for each image, applies masking, and returns a list of dictionaries representing the images.
//----------------------------------------------------------------------------------------------------//
Landsat5Lst
Input:
polygon: A list of coordinates representing the polygon geometry to define the region of interest.
startDate: The start date of the date range for image retrieval, in the format "YYYY-MM-dd".
endDate: The end date of the date range for image retrieval, in the format "YYYY-MM-dd".
Output:
The download() method returns a list of dictionaries, where each dictionary represents an image within the specified date range and polygon. Each dictionary contains the following information:

"lst": An array representing the Land Surface Temperature (LST) values for the image. The LST values are in degrees Celsius.
"date":