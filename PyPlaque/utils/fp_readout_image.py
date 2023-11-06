import numpy as np
from skimage import measure
from PyPlaque.utils.fp_readout_object import PlaqueObjectReadout
### probably needs to somehow integrated 
from PyPlaque.utils.segment_plaque import get_plaque_mask


class PlaqueImageReadout():
    """
    **Class PlaqueImageReadout** is aimed to contain metadata of multiple instances of a plaques 
    of a single well of a Fluorescence Plaque.

    _Arguments_:

    nuclei_image_name - (str, required) name of nuclei image plate.

    nuclei_image - (np.array, required) image of the nuclei plate.

    nuclei_mask - (np.array, required) image of the nuclei plate mask.

    plaque_image_name - (str, required) name of plaque image plate.

    plaque_image - (np.array, required) image of the plaque plate.

    plaque_mask - (np.array, required) image of the plaque plate mask.
    """
    def __init__(self, 
                 nuclei_image_name, 
                 plaque_image_name,
                 nuclei_image, 
                 plaque_image,
                 nuclei_mask,
                 plaque_mask,
                 virus_params):
        #check data types
        if not type(nuclei_image_name) is str:
            raise TypeError("Expected nuclei_image_name argument to be str")
        if not type(plaque_image_name) is str:
            raise TypeError("Expected nuclei_image_name argument to be str")
        if (not type(nuclei_mask) is np.ndarray) or (not nuclei_mask.ndim == 2):
            raise TypeError("Mask attribute of well must be a 2D numpy array")
        if (not type(plaque_mask) is np.ndarray) or (not plaque_mask.ndim == 2):
            raise TypeError("Mask attribute of well must be a 2D numpy array")
        if (not type(nuclei_image) is np.ndarray) or (not nuclei_image.ndim == 2):
            raise TypeError("Image attribute of well must be a 2D numpy array")
        if (not type(plaque_image) is np.ndarray) or (not plaque_image.ndim == 2):
            raise TypeError("Image attribute of well must be a 2D numpy array")
        if (not type(virus_params) is dict):
            raise TypeError("Virus params attribute must be a dictionary")
        
        self.nuclei_mask = nuclei_mask
        self.nuclei_image = nuclei_image
        self.nuclei_image_name = nuclei_image_name
        self.plaque_mask = plaque_mask
        self.plaque_image = plaque_image
        self.plaque_image_name = plaque_image_name
        self.params = virus_params

    def get_nuclei_image_name(self):
        return self.nuclei_image_name
    
    def get_plaque_image_name(self):
        return self.plaque_image_name

    def get_row(self):
        return self.nuclei_image_name.split("_")[1][0]
    
    def get_column(self):
        return self.nuclei_image_name.split("_")[1][1:]

    def get_max_nuclei_intensity(self):
        return np.max(self.nuclei_image) #creating a masked image 

    def get_max_plaque_intensity(self):
        return np.max(self.plaque_image) #creating a masked image 
          
    def get_total_nuclei_intensity(self):
       return np.sum(self.nuclei_image.astype(np.float64)) #creating a masked image 

    def get_total_plaque_intensity(self):
       # Cast the image to a larger data type before summing to prevent overflow
        # Convert to int64 to avoid overflow in integer sum
       total_intensity = np.sum(self.plaque_image.astype(np.int64))
       return total_intensity
       
        
    def get_mean_nuclei_intensity(self):
        if len(np.nonzero(self.nuclei_image*self.nuclei_mask)[0])==0:
            return 0
        else:
            return np.mean(np.nonzero(self.nuclei_image.astype(np.float64))) #creating a masked image 

    def get_mean_plaque_intensity(self):
        if len(np.nonzero(self.plaque_image)[0])==0:
            return 0
        else:
            return np.mean(self.plaque_image.astype(np.float64)) #creating a masked image 

    def get_median_plaque_intensity(self):
        if len(np.nonzero(self.plaque_image)[0])==0:
            return 0
        else:
            return np.median(self.plaque_image.astype(np.float64))
    
    def get_nuclei_count(self):
        # mask = self.nuclei_mask
        # labelImage = measure.label(mask)
        # labelImage[~mask] = 0
        # props = measure.regionprops(labelImage)
        # nuclei_area_sum = 0
        # for prop in props:
        #     if  self.params['minCellArea'] < prop.area:
        #         nuclei_area_sum+=np.sum(prop.image)
        nuclei_area_sum = np.sum(self.nuclei_mask)
        return round(nuclei_area_sum/((self.params['minCellArea'] + self.params['maxCellArea'])/2))
    
    def get_plaque_count(self):
        plaqueRegionProperties ,globalPeakCoords = get_plaque_mask(self.plaque_image,self.params)
        numberOfPlaques =  len(globalPeakCoords)
        #below is the original code the problem was that it was calculating the number of plaque regions
        #and not summing the peaks of the individual plaques, hence it was inconsistent with  plaque 2.0
        # labelImage = measure.label(self.plaque_mask)
        # labelImage[~self.plaque_mask] = 0
        # props = measure.regionprops(labelImage)
        # plaqueRegionProperties = []
        # for prop in props:
        #     if  self.params['min_plaque_area'] < prop.area:
        #         plaqueRegionProperties.append(prop)
        # return len(plaqueRegionProperties)
        return numberOfPlaques

    def get_infected_nuclei_count(self):
        labelImage = measure.label(self.plaque_mask)
        labelImage[~self.plaque_mask] = 0
        props = measure.regionprops(labelImage)
        plaqueRegionProperties_area = 0
        for prop in props:
            if  self.params['min_plaque_area'] < prop.area:
                plaqueRegionProperties_area += prop.area
        return round(plaqueRegionProperties_area/
                     ((self.params['minCellArea'] + self.params['maxCellArea'])/2))
    
    def get_lesion_area(self):
        return np.sum(self.plaque_mask)
    
    def get_plaque_objects(self):
        labelImage = measure.label(self.plaque_mask)
        labelImage[~self.plaque_mask] = 0
        props = measure.regionprops(labelImage)
        plaqueRegionProperties = []
        for prop in props:
            if  self.params['min_plaque_area'] < prop.area:
                plaqueRegionProperties.append(prop)
        return plaqueRegionProperties
    
    def call_plaque_object_readout(self,plaque_object_properties, params):
        min_row, min_col, max_row, max_col = plaque_object_properties.bbox
        plq_object = PlaqueObjectReadout(self.nuclei_image_name, 
                                        self.plaque_image_name,
                                        self.nuclei_image[min_row:max_row, min_col:max_col], 
                                        self.plaque_image[min_row:max_row, min_col:max_col],
                                        self.nuclei_mask[min_row:max_row, min_col:max_col],
                                        self.plaque_mask[min_row:max_row, min_col:max_col],
                                        plaque_object_properties,
                                        params)

        return plq_object
    