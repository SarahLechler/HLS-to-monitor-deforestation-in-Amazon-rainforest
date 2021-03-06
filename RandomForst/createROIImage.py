# Import Python 3 print function
from __future__ import print_function
# Import OGR -
from osgeo import ogr
import gdal
import numpy as np


"""
creates polygons from training data point layer
inout:  index name String (NDVI, RNSDI, SAVI, GEMI EVI)
        path String path to training data
        year: year of training data

"""

def createROIImage(index, path, year):
    # 1) opening the shapefile
    # First we will open our raster image, to understand how we will want to rasterize our vector
    raster_ds = gdal.Open(path+index+'.tif', gdal.GA_ReadOnly)

    # Fetch projection and extent
    proj = raster_ds.GetProjectionRef()
    ext = raster_ds.GetGeoTransform()
    source_ds = ogr.Open('trainingData/21LYG'+year+'_trainingData.shp')
    source_layer = source_ds.GetLayer()

    # 2) Creating the destination raster data source

    target_ds = gdal.GetDriverByName('GTiff').Create(
        path + 'training_data'+index+'.gtif', 3660, 3660, 1,
        gdal.GDT_Float32)  ##COMMENT 2

    target_ds.SetGeoTransform(ext)  # COMMENT 3
    target_ds.SetProjection(proj)

    band = target_ds.GetRasterBand(1)
    band.SetNoDataValue(-9999)  ##COMMENT 5

    status = gdal.RasterizeLayer(target_ds, [1], source_layer,
                                 options=['ALL_TOUCHED=TRUE',  # rasterize all pixels touched by polygons
                                          'ATTRIBUTE=id'])  ##COMMENT 6
    #out_img, out_transform = mask(status, shapes=bbox, crop=True) #How to cut the rasterlayer?

    target_ds = None  ##COMMENT 7

    if status != 0:
        print("I don't think it worked...")
    else:
        print("Success")

    roi_ds = gdal.Open(path + 'training_data'+index+'.gtif', gdal.GA_ReadOnly)
    roi = roi_ds.GetRasterBand(1).ReadAsArray()

    # How many pixels are in each class?
    classes = np.unique(roi)
    classes = classes
    # Iterate over all class labels in the ROI image, printing out some information
    for c in classes:
        print('Class {c} contains {n} pixels'.format(c=c,
                                                     n=(roi == c).sum()))
