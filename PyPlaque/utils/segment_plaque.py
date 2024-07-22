import matplotlib.pyplot as plt
import numpy as np
import skimage
from scipy import ndimage as ndi
from skimage import measure

from PyPlaque.utils import remove_background, picks_area


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
        if virus_params['use_picks']:
            temp_area = picks_area(prop.image)
        else:
            temp_area = prop.area
        if  virus_params['min_plaque_area'] < temp_area:
            plaqueRegionProperties.append(prop)

    bBoxes = []
    bwPlqRegions = []
    cropPlqRegions = []
    globalPeakCoords=[]
    peakCounts = []


    labels = []
    finalPlqRegImage =np.zeros_like(labelImage) #this contains the final BW image of all plaque regions

    #fine detection
    if virus_params['fine_plaque_detection_flag']:
        for idx,region in enumerate(plaqueRegionProperties):
            (x1,y1,x2,y2) = region.bbox
            bBoxes.append(region.bbox)

            bwPlqRegions.append(region.image)
            curPlqRegion=inputImage[x1:x2,y1:y2]*region.image
            cropPlqRegions.append(curPlqRegion)
            labels.append(idx+1)

            for coord in region.coords:
                finalPlqRegImage[coord[0], coord[1]] = 1

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
    else:
        return finalPlqRegImage, None


def plot_virus_contours(inputImage,virus_params,save_path=None):
    _, bg_removed_img = remove_background(inputImage,
                                  radius=virus_params['correction_ball_radius'])
    finalPlqRegImage, globalPeakCoords = get_plaque_mask(inputImage,virus_params)
    _, ax = plt.subplots(figsize=(8, 8))

    # Display inputImage with custom colormap and intensity range
    ax.imshow(bg_removed_img, cmap=plt.get_cmap('gray'), vmin=500, vmax=6000, alpha=1, extent=[0, inputImage.shape[1], 
                                                                                inputImage.shape[0], 0])
    # ax.imshow(finalPlqRegImage, cmap=plt.cm.gray)

    # Find contours in finalPlqRegImage
    contours = measure.find_contours(finalPlqRegImage)

    # Plot contours with random colors
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2,color='yellow')

    ax.plot(globalPeakCoords[:, 1], globalPeakCoords[:, 0], 'r.', markersize=15)
    ax.axis('off')
    ax.set_title('Peak local max with contours')
    if save_path:
        plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()
    return