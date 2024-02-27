import numpy as np
import skimage


class PlaqueObjectReadout():
    """
    **Class PlaqueObjectReadout** is aimed to contain data of a single instance of a plaque/nuclei 
    of a single well of a Fluorescence Plaque.

    _Arguments_:

    nuclei_image_name - (str, required) name of nuclei image plate.

    nuclei_object - (np.array, required) image of the nuclei plate.

    nuclei_object_mask - (np.array, required) image of the nuclei plate mask.

    plaque_image_name - (str, required) name of plaque image plate.

    plaque_object - (np.array, required) image of the plaque plate.

    plaque_object_mask - (np.array, required) image of the plaque plate mask.
    """
    def __init__(self, 
                 nuclei_image_name, 
                 plaque_image_name,
                 nuclei_object, 
                 plaque_object,
                 nuclei_object_mask,
                 plaque_object_mask,
                 plaque_object_properties,
                 virus_params):
        
        #check data types
        if not type(nuclei_image_name) is str:
            raise TypeError("Expected nuclei_image_name argument to be str")
        if not type(plaque_image_name) is str:
            raise TypeError("Expected nuclei_image_name argument to be str")
        if (not type(nuclei_object_mask) is np.ndarray) or (not nuclei_object_mask.ndim == 2):
            raise TypeError("Mask atribute of well must be a 2D numpy array")
        if (not type(plaque_object_mask) is np.ndarray) or (not plaque_object_mask.ndim == 2):
            raise TypeError("Mask atribute of well must be a 2D numpy array")
        if (not type(nuclei_object) is np.ndarray) or (not nuclei_object.ndim == 2):
            raise TypeError("Image atribute of well must be a 2D numpy array")
        if (not type(plaque_object) is np.ndarray) or (not plaque_object.ndim == 2):
            raise TypeError("Image atribute of well must be a 2D numpy array")
        if (not type(virus_params) is dict):
            raise TypeError("Virus params attribute must be a dictionary")
        
        self.nuclei_object_mask = nuclei_object_mask
        self.nuclei_object = nuclei_object
        self.nuclei_image_name = nuclei_image_name
        self.plaque_object_mask = plaque_object_mask
        self.plaque_object = plaque_object
        self.plaque_image_name = plaque_image_name
        self.params = virus_params
        self.plaque_object_properties = plaque_object_properties

    def get_row(self):
        return self.nuclei_image_name.split("_")[1][0]
        
    def get_column(self):
        return self.nuclei_image_name.split("_")[1][1:]
    
    def get_area(self):
        return np.sum(self.plaque_object_properties.image.astype(np.float64))
      
    def get_perimeter(self):
        return self.plaque_object_properties.perimeter

    def get_centroid(self):
        return self.plaque_object_properties.centroid
    
    def get_bbox(self):
        return (self.plaque_object_properties.bbox[0], \
                self.plaque_object_properties.bbox[3], \
                self.plaque_object_properties.bbox[2] - self.plaque_object_properties.bbox[0], \
                self.plaque_object_properties.bbox[3] - self.plaque_object_properties.bbox[1])

    def get_major_minor_axis_length(self):
        return self.plaque_object_properties.axis_major_length, \
                self.plaque_object_properties.axis_minor_length
    
    def get_custom_eccentricity(self,):
        # Calculate the image moments
        y_indices, x_indices = np.nonzero(binary_image)
        x_mean = x_indices.mean()
        y_mean = y_indices.mean()
        x_indices_centered = x_indices - x_mean
        y_indices_centered = y_indices - y_mean

        # Calculate central moments
        mu11 = (x_indices_centered * y_indices_centered).sum()
        mu20 = (x_indices_centered * x_indices_centered).sum()
        mu02 = (y_indices_centered * y_indices_centered).sum()

        # Calculate the axis lengths of the ellipse (major_axis_length, minor_axis_length)
        # The math comes from the eigenvalues of the covariance matrix of the object's x and y pixel coordinates
        a = mu20 + mu02
        b = np.sqrt((mu20 - mu02) ** 2 + 4 * mu11 ** 2)
        major_axis_length = np.sqrt(2) * np.sqrt(a + b)
        minor_axis_length = np.sqrt(2) * np.sqrt(a - b)

        # Calculate eccentricity
        eccentricity = np.sqrt(1 - (minor_axis_length / major_axis_length) ** 2)

        return eccentricity


    def get_eccentricity(self):
        
        return self.plaque_object_properties.eccentricity
    
    def get_convex_area(self):
        return self.plaque_object_properties.area_convex
    
    def roundness(self):

        image = self.plaque_object_properties.image_convex 
        area = self.plaque_object_properties.area_convex
        #  Find contours
        contours = skimage.measure.find_contours(image)

        # Assuming the largest contour corresponds to the object
        contour = max(contours, key=len)

        # Calculate the perimeter
        perimeter = np.sum(np.sqrt(np.sum(np.diff(contour, axis=0)**2, axis=1)))
        perimeter = self.plaque_object_properties.perimeter
        
        roundness = (4 * np.pi * area) / ( (perimeter ** 2))
        
        return perimeter,area
    
    def get_number_of_peaks(self):
        globalPeakCoords=[]
        (x1,y1,x2,y2) = self.plaque_object_properties.bbox
        curPlqRegion= self.plaque_object * self.plaque_object_properties.image
        
        #fine detection 
        blurredImage = skimage.filters.gaussian(curPlqRegion, 
                                                sigma=self.params['plaque_gaussian_filter_sigma'],
                                                truncate = self.params['plaque_gaussian_filter_size']/
                                                    self.params['plaque_gaussian_filter_sigma'] )
        
        coordinates = skimage.feature.peak_local_max(blurredImage, 
                                                     min_distance=self.params['peak_region_size'],
                                                     exclude_border = False)

        globalPeakCoords = np.array([coordinates[:, 0] + x1, coordinates[:, 1] + y1]).T
        
        return globalPeakCoords
    
    def get_nuclei_in_plaque(self):
        mask = self.plaque_object_properties.image_convex * self.nuclei_object_mask
        # labelImage = measure.label(mask)
        # labelImage[~mask] = 0
        # props = measure.regionprops(labelImage)
        # nuclei_area_sum = 0
        # for prop in props:
        #     if  self.params['minCellArea'] < prop.area:
        #         nuclei_area_sum+=np.sum(prop.image)
        nuclei_area_sum = np.sum(mask)
        return nuclei_area_sum/((self.params['minCellArea'] + self.params['maxCellArea'])/2)
    
    def get_infected_nuclei_in_plaque(self):
        mask = self.plaque_object_mask * self.nuclei_object_mask
        # labelImage = measure.label(mask)
        # labelImage[~mask] = 0
        # props = measure.regionprops(labelImage)
        # nuclei_area_sum = 0
        # for prop in props:
        #     if  self.params['minCellArea'] < prop.area:
        #         nuclei_area_sum+=np.sum(prop.image)
        nuclei_area_sum = np.sum(mask)
        return nuclei_area_sum/((self.params['minCellArea'] + self.params['maxCellArea'])/2)
    
    def get_max_intensity_GFP(self):
        return np.max(self.plaque_object*self.plaque_object_mask) #creating a masked image 
    
    def get_total_intensity_GFP(self):
        return np.sum(self.plaque_object*self.plaque_object_mask) #creating a masked image 

    def get_mean_intensity_GFP(self):
        if len(np.nonzero(self.plaque_object*self.plaque_object_mask)[0])==0:
            return 0
        else:
            return np.mean(np.nonzero(self.plaque_object*self.plaque_object_mask)) 
    #creating a masked image 
