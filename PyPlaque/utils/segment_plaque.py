import cv2
import matplotlib.pyplot as plt
import numpy as np
import skimage
from scipy import ndimage as ndi
from skimage import measure


def getAllPlaqueRegions(image,threshold,plqConnect):
    BW =  image > threshold
    distance = ndi.distance_transform_edt(~BW)
    BW2 = distance <= plqConnect
     # Label connected regions
    labelImage = measure.label(BW2)
    # Remove elements from the label matrix which were not present in the original binary image
    labelImage[~BW] = 0

    return labelImage


def get_plaque_mask(inputImage,virus_params):
    labelImage =  getAllPlaqueRegions(inputImage,
                              virus_params['virus_threshold'],
                              virus_params['plaque_connectivity'])


    # Calculate various region properties of the image
    props = measure.regionprops(labelImage)

    # Filter out objects with area smaller than minPlaqueArea or larger than maxPlaqueArea
    plaqueRegionProperties = []
    for prop in props:
        if  virus_params['min_plaque_area'] < prop.area:
            plaqueRegionProperties.append(prop)

    bBoxes = []
    bwPlqRegions = []
    cropPlqRegions = []
    globalPeakCoords=[]
    peakCounts = []


    labels = []
    finalPlqRegImage =np.zeros_like(labelImage) #this contains the final BW image of all plaque regions

    for idx,region in enumerate(plaqueRegionProperties):
        (x1,y1,x2,y2) = region.bbox
        bBoxes.append(region.bbox)

        bwPlqRegions.append(region.image)
        curPlqRegion=inputImage[x1:x2,y1:y2]*region.image
        cropPlqRegions.append(curPlqRegion)
        labels.append(idx+1)

        for coord in region.coords:
            finalPlqRegImage[coord[0], coord[1]] = 1

        #fine detection

        blurredImage = skimage.filters.gaussian(
                                            curPlqRegion,
                                            sigma=virus_params['plaque_gaussian_filter_sigma'],
                                            truncate = virus_params['plaque_gaussian_filter_size']/
                                                    virus_params['plaque_gaussian_filter_sigma'])

        coordinates = skimage.feature.peak_local_max(blurredImage,
                                                     min_distance=virus_params['peak_region_size'],
                                                     exclude_border = False)
        peakCounts.append(len(coordinates))
        if idx == 0:
            globalPeakCoords = np.array([coordinates[:, 0] + x1, coordinates[:, 1] + y1]).T
        else:
            globalPeakCoords = np.vstack((globalPeakCoords, np.array([coordinates[:, 0] + x1,
                                                                      coordinates[:, 1] + y1]).T))

    return finalPlqRegImage, globalPeakCoords
