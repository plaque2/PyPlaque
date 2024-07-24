import cv2
import numpy as np
import re
import skimage

from PyPlaque.utils import picks_area, picks_perimeter

class PlaqueObjectReadout:
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

    plaque_object_properties - (object, required) regionprops properties of the plaque object.

    virus_params - (dict, required) dictionary of parameters for the virus channel. 
                    Same as in ExperimentFluorescencePlaque.
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

    def get_row(self, row_pattern=None):
        return re.findall(row_pattern, self.nuclei_image_name)[0]
        
    def get_column(self, column_pattern=None):
        return re.findall(column_pattern, self.nuclei_image_name)[0]
    
    def get_area(self):
        if self.params['use_picks']:
            return picks_area(self.plaque_object_properties.image)
        else:
            return np.sum(self.plaque_object_properties.image.astype(np.float64))
      
    def get_perimeter(self):
        if self.params['use_picks']:
            return picks_perimeter(self.plaque_object_properties.image)
        else:
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
    
    def eccentricity(self):
        """
        **eccentricity method** returns for an individual plaque object,the eccentricity of 
        the plaque which is found by fitting an ellipse to the plaque boundary and finding the 
        eccentricity given by sqrt(1-(b^2/a^2)) where b is the length of the semi-minor axis and 
        a is the length of the semi-major axis

        _Arguments_:
        """
        # find the contours
        contours,_ = cv2.findContours(self.plaque_object_properties.image.astype(np.uint8).copy(), 
                                                            cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        ecc = 0
        # select the first contour that has more than 5 points and fit an ellipse based on that
        if len(contours) != 0:
            for i in range(len(contours)):
                if len(contours[i]) >= 5:
                    # fit the ellipse
                    ellipse=cv2.fitEllipse(contours[i])
                    if ellipse[2] == 0: #if rotation angle is zero results are not reliable
                        ecc = 0
                    else:
                        semi_major_axis = ellipse[1][0]/2
                        semi_minor_axis = ellipse[1][1]/2

                        if semi_minor_axis > semi_major_axis:
                            temp = semi_minor_axis
                            semi_minor_axis = semi_major_axis
                            semi_major_axis = temp

                        if semi_minor_axis == 0:
                            semi_minor_axis = 0.1
                        if semi_major_axis == 0:
                            semi_major_axis = 0.1
                        ecc = np.sqrt(1-(semi_minor_axis**2/semi_major_axis**2))
                        break
        else:
            ecc = 0
        return ecc

    def get_eccentricity(self):
        return self.eccentricity()
    
    def get_convex_area(self):
        return self.plaque_object_properties.area_convex
    
    def roundness(self):
        if self.params['use_picks']:
            perimeter = picks_perimeter(self.plaque_object_properties.image)
            if perimeter != 0:
                roundness = 4 * np.pi * picks_area(self.plaque_object_properties.image) / \
                        ( perimeter ** 2 )
            else:
                roundness = 0
        else:
            area = self.plaque_object_properties.area
            bbox = self.plaque_object_properties.bbox  
            point1 = np.array((bbox[3],bbox[2]))
            point2 = np.array(((bbox[3]+bbox[1])/2,(bbox[2]+bbox[0])/2))
            radius = np.linalg.norm(point1 - point2)
            perimeter = 2 * np.pi * radius
            if perimeter != 0:
                roundness = 4 * np.pi * area / ( perimeter ** 2 )
            else:
                roundness = 0
            
        return roundness 

    def get_roundness(self):
        return self.roundness()
    
    def get_number_of_peaks(self):
        #fine detection 
        if self.params['fine_plaque_detection_flag']:
            global_peak_coords=[]
            (x1,y1,_,_) = self.plaque_object_properties.bbox
            cur_plq_region= self.plaque_object * self.plaque_object_properties.image
            
            
            blurred_image = skimage.filters.gaussian(cur_plq_region, 
                                            sigma=self.params['plaque_gaussian_filter_sigma'],
                                            truncate = self.params['plaque_gaussian_filter_size']/
                                                self.params['plaque_gaussian_filter_sigma'] )
            
            coordinates = skimage.feature.peak_local_max(blurred_image, 
                                                    min_distance=self.params['peak_region_size'],
                                                    exclude_border = False)

            global_peak_coords = np.array([coordinates[:, 0] + x1, coordinates[:, 1] + y1]).T
            
            return global_peak_coords
        else:
            return None
    
    def get_nuclei_in_plaque(self):
        mask = self.plaque_object_properties.image_convex * self.nuclei_object_mask
        if self.params['use_picks']:
            nuclei_area_sum = picks_area(mask)
        else:
            nuclei_area_sum = np.sum(mask)
        return nuclei_area_sum/((self.params['min_cell_area'] + self.params['max_cell_area'])/2)
    
    def get_infected_nuclei_in_plaque(self):
        mask = self.plaque_object_mask * self.nuclei_object_mask
        if self.params['use_picks']:
            nuclei_area_sum = picks_area(mask)
        else:
            nuclei_area_sum = np.sum(mask)
        return nuclei_area_sum/((self.params['min_cell_area'] + self.params['max_cell_area'])/2)
    
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
