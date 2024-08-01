import matplotlib.pyplot as plt
import numpy as np
import skimage
from scipy import ndimage as ndi
from skimage import measure

from PyPlaque.utils import remove_background, picks_area


def get_all_plaque_regions(image,threshold,plq_connect):
    """
    **get_all_plaque_regions Function**
    This function identifies and labels all connected regions in a binary image that are likely to 
    contain virus plaques. It processes the input grayscale `image` by applying a threshold to 
    create a binary mask, then computes the distance transform of the inverted binary mask to 
    identify plaque candidates. Connected components within this distance-transformed image are 
    labeled and returned as a label matrix. The original background pixels in the label matrix are 
    set to 0 where they were not present in the input binary mask.
    
    Args:
        image (np.ndarray, required): A 2D numpy array representing the grayscale image of the 
                                    tissue section.
        threshold (float, required): A float value that determines the pixel intensity below which 
                                    pixels are considered part of the background.
        plq_connect (int, required): An integer specifying the maximum distance within which 
                                    connected components are grouped to be considered as potential 
                                    virus plaques.
    
    Returns:
        np.ndarray: A 2D numpy array of integers where each unique value represents a different 
        connected region in the input image, likely containing virus plaques. Pixels not part of any 
        plaque or background are set to 0.
        
    Raises:
        TypeError: If `image` is not a 2D numpy array, `threshold` is not a float, or `plq_connect` 
        is not an integer.
        ValueError: If `threshold` is outside the valid range for pixel intensities in `image` or 
        if `plq_connect` is less than or equal to zero.
    """
    bw =  image > threshold
    distance = ndi.distance_transform_edt(~bw)
    bw2 = distance <= plq_connect
     # Label connected regions
    label_image = measure.label(bw2)
    # Remove elements from the label matrix which were not present in the original binary image
    label_image[~bw] = 0

    return label_image


def get_plaque_mask(input_image,virus_params):
    """
    **get_plaque_mask Function**
    This function generates a mask of virus plaques in an input image based on specified parameters.
    It processes the input image to identify and segment regions that are likely to contain virus 
    plaques. It uses thresholding and morphological operations to create a binary mask where plaque 
    regions are white (1) and background is black (0). The function optionally performs fine-grained 
    plaque detection if enabled in `virus_params`.
    
    Args:
        input_image (np.ndarray, required): A 2D numpy array representing the grayscale image of the 
                                            tissue section.
        virus_params (dict, required): A dictionary containing parameters for virus plaque 
                                    detection, including threshold value, connectivity, and other
                                     morphological operations settings.
    
    Returns:
        tuple: A tuple containing two elements:
            - final_plq_reg_image (np.ndarray): A 2D numpy array of the same size as `input_image` 
            with plaque regions marked by white pixels (1) and background by black pixels (0).
            - global_peak_coords (np.ndarray or None): An array of coordinates where local peaks 
            were detected in the final mask, if fine detection is enabled; otherwise, returns None.
        
    Raises:
        TypeError: If `input_image` is not a 2D numpy array or `virus_params` is not a dictionary.
        ValueError: If any parameter within `virus_params` does not match its expected type or value 
        range as specified in the method signature.
    """
    label_image =  get_all_plaque_regions(input_image,
                              virus_params['virus_threshold'],
                              virus_params['plaque_connectivity'])


    # Calculate various region properties of the image
    props = measure.regionprops(label_image)

    # Filter out objects with area smaller than min_plaque_area or larger than max_plaque_area
    plaque_region_properties = []
    for prop in props:
        if virus_params['use_picks']:
            temp_area = picks_area(prop.image)
        else:
            temp_area = prop.area
        if  virus_params['min_plaque_area'] < temp_area:
            plaque_region_properties.append(prop)

    bboxes = []
    bw_plq_regions = []
    crop_plq_regions = []
    global_peak_coords=[]
    peak_counts = []


    labels = []
    final_plq_reg_image =np.zeros_like(label_image) 
    #this contains the final bw image of all plaque regions

    #fine detection
    if virus_params['fine_plaque_detection_flag']:
        for idx,region in enumerate(plaque_region_properties):
            (x1,y1,x2,y2) = region.bbox
            bboxes.append(region.bbox)

            bw_plq_regions.append(region.image)
            cur_plq_region=input_image[x1:x2,y1:y2]*region.image
            crop_plq_regions.append(cur_plq_region)
            labels.append(idx+1)

            for coord in region.coords:
                final_plq_reg_image[coord[0], coord[1]] = 1

            blurred_image = skimage.filters.gaussian(
                                            cur_plq_region,
                                            sigma=virus_params['plaque_gaussian_filter_sigma'],
                                            truncate = virus_params['plaque_gaussian_filter_size']/
                                                    virus_params['plaque_gaussian_filter_sigma'])

            coordinates = skimage.feature.peak_local_max(blurred_image,
                                                    min_distance=virus_params['peak_region_size'],
                                                    exclude_border = False)
            peak_counts.append(len(coordinates))
            if idx == 0:
                global_peak_coords = np.array([coordinates[:, 0] + x1, coordinates[:, 1] + y1]).T
            else:
                global_peak_coords = np.vstack((global_peak_coords, np.array([coordinates[:, 0] + 
                                                                x1, coordinates[:, 1] + y1]).T))

        return final_plq_reg_image, global_peak_coords
    else:
        return final_plq_reg_image, None


def plot_virus_contours(input_image,virus_params,save_path=None):
    """
    **plot_virus_contours Function**
    This function plots contours of virus plaques on a modified grayscale image. It processes an 
    input image to remove its background and then generates a mask for the plaque region. It uses 
    these masks to find and plot the contours of the virus plaques using custom colors and markers. 
    The final image is displayed interactively or saved to disk if a save path is provided.
    
    Args:
        input_image (np.ndarray, required): A 2D numpy array representing the grayscale input image 
                                            of the tissue section containing virus plaques.
        virus_params (dict, required): A dictionary containing parameters for virus plaque detection 
                                        and correction, including 'correction_ball_radius'.    
        save_path (str or None, optional): The file path where the plot will be saved if provided; 
                                        otherwise, it is displayed interactively. Defaults to None.
    
    Returns:
        None: The function generates a matplotlib plot based on the arguments provided and 
        optionally saves it to disk.
        
    Raises:
        TypeError: If any of the input arguments do not match their expected types as specified 
        in the method signature.
    """
    _, bg_removed_img = remove_background(input_image,
                                  radius=virus_params['correction_ball_radius'])
    final_plq_reg_image, global_peak_coords = get_plaque_mask(input_image,virus_params)
    _, ax = plt.subplots(figsize=(8, 8))

    # Display input_image with custom colormap and intensity range
    ax.imshow(bg_removed_img, cmap=plt.get_cmap('gray'), vmin=500, vmax=6000, alpha=1, 
    extent=[0, input_image.shape[1],input_image.shape[0], 0])
    # ax.imshow(final_plq_reg_image, cmap=plt.cm.gray)

    # Find contours in final_plq_reg_image
    contours = measure.find_contours(final_plq_reg_image)

    # Plot contours with random colors
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=2,color='yellow')

    ax.plot(global_peak_coords[:, 1], global_peak_coords[:, 0], 'r.', markersize=15)
    ax.axis('off')
    ax.set_title('Peak local max with contours')
    if save_path:
        plt.savefig(save_path,bbox_inches='tight', dpi=300)
    plt.show()
    return