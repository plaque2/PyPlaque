import numpy as np
import re
from skimage import measure

from PyPlaque.utils import get_plaque_mask
from PyPlaque.view import PlaqueObjectReadout
from PyPlaque.utils import picks_area


class WellImageReadout:
    """
    **WellImageReadout Class** 
    The WellImageReadout class encapsulates metadata related to multiple instances of plaques 
    within a single well of a fluorescence plate.
    
    Attributes:
        nuclei_image_name (str, required): The name of the nuclei image, which serves as an 
                                        identifier for the nuclei image data.

        nuclei_image (np.ndarray, required): A 2D numpy array representing the image data of the
                                            nuclei.

        nuclei_mask (np.ndarray, required): A 2D numpy array serving as a mask for the nuclei image.

        plaque_image_name (str, required): The name of the plaque image, which serves as an 
                                        identifier for the plaque image data.

        plaque_image (np.ndarray, required): A 2D numpy array representing the image data of the 
                                            plaque.

        plaque_mask (np.ndarray, required): A 2D numpy array serving as a mask for the plaque image.

        params (dict, required): A dictionary containing parameters specific to virus channels, 
                                which may be used in further analyses or experiments.
        
    Raises:
        TypeError: If the data types for any of the arguments do not match their expected types as 
        specified in the class definition.
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
        """
        **get_nuclei_image_name Method**
        This function returns the name of the nuclei image file. It retrieves and returns the 
        filename or path associated with the nuclei image, which is stored in the instance variable 
        `nuclei_image_name`.
        
        Args: 

        Returns:
            str: The name of the nuclei image file.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        return self.nuclei_image_name
    
    def get_plaque_image_name(self):
        """
        **get_plaque_image_name Method**
        This function returns the name of the plaque image file. It retrieves and returns the 
        filename or path associated with the plaque image, which is stored in the instance variable 
        `plaque_image_name`.
        
        Args:

        Returns:
            str: The name of the plaque image file.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        return self.plaque_image_name

    def get_row(self, row_pattern=None):
        """
        **get_row Method**
        This function extracts and returns the row identifier from the nuclei image name using a 
        regular expression pattern. It uses the given row pattern to search for matches within 
        the `nuclei_image_name`. The method assumes that the regex pattern will capture the 
        desired row identifier, which is typically part of the filename representing the 
        fluorescence plate image.
        
        Args:
            row_pattern (str or None, optional): A regular expression pattern string used to match 
                                                the row identifier in the nuclei image name. If not 
                                                provided, it defaults to `None`.
            
        Returns:
            str: The matched row identifier extracted from the `nuclei_image_name` using the 
            specified pattern.
            
        Raises:
            TypeError: If the input argument does not match its expected type as specified in 
            the method signature.
        """
        return re.findall(row_pattern, self.nuclei_image_name)[0]
    
    def get_column(self, column_pattern=None):
        """
        **get_column Method**
        This function extracts and returns the column identifier from the nuclei image name using a 
        regular expression pattern. It uses the given column pattern to search for matches within 
        the `nuclei_image_name`. The method assumes that the regex pattern will capture the 
        desired column identifier, which is typically part of the filename representing the 
        fluorescence plate image.
        
        Args:
            column_pattern (str or None, optional): A regular expression pattern string used to 
                                                match the column identifier in the nuclei image 
                                                name. If not provided, it defaults to `None`.
            
        Returns:
            str: The matched column identifier extracted from the `nuclei_image_name` using the 
            specified pattern.
            
        Raises:
            TypeError: If the input argument does not match its expected type as specified in 
            the method signature.
        """
        return re.findall(column_pattern, self.nuclei_image_name)[0]

    def get_max_nuclei_intensity(self):
        """
        **get_max_nuclei_intensity Method**
        This function computes and returns the maximum intensity of nuclei in the fluorescence 
        plate image. It calculates the maximum pixel intensity from the masked portion of the 
        nuclei image, which is assumed to represent the intensity of individual nuclei. 
        It does not filter out non-zero intensities to capture the highest possible value 
        if multiple nuclei are present.
        
        Args:

        Returns:
            float: The maximum intensity value of the nucleus pixels in the masked image.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        return np.max(self.nuclei_image) #creating a masked image 

    def get_max_plaque_intensity(self):
        """
        **get_max_plaque_intensity Method**
        This function computes and returns the maximum intensity of plaques in the fluorescence 
        plate image. It calculates the maximum pixel intensity from the plaque image, which is 
        assumed to represent the intensity of individual plaques.
        
        Args:

        Returns:
            float: The maximum intensity value of the plaque pixels in the image.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        return np.max(self.plaque_image) #creating a masked image 
        
          
    def get_total_nuclei_intensity(self):
        """
        **get_total_nuclei_intensity Method**
        This function computes and returns the total intensity of all nuclei in the fluorescence 
        plate image.It calculates the sum of pixel intensities across the entire nuclei image, 
        which is assumed to represent the combined intensity of individual nuclei. The image data 
        type is cast to float64 before summation to ensure that large values are not truncated due 
        to integer overflow.
        
        Args:

        Returns:
            float: The total intensity value of all nucleus pixels in the image.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        return np.sum(self.nuclei_image.astype(np.float64)) #creating a masked image 

    def get_total_plaque_intensity(self):
        """
        **get_total_plaque_intensity Method**
        This function computes and returns the total intensity of all plaques in the fluorescence 
        plate image. It calculates the sum of pixel intensities across the entire plaque image, 
        which is assumed to represent the combined intensity of individual plaques. The image data 
        type is cast to int64 before summation to prevent overflow errors that can occur with 
        large values.
        
        Args:

        Returns:
            float: The total intensity value of all plaque pixels in the image.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        # Cast the image to a larger data type before summing to prevent overflow
        # Convert to int64 to avoid overflow in integer sum
        total_intensity = np.sum(self.plaque_image.astype(np.int64))
        return total_intensity
       
        
    def get_mean_nuclei_intensity(self):
        """
        **get_mean_nuclei_intensity Method**
        This function computes and returns the mean intensity of nuclei in the fluorescence 
        plate image. It calculates the mean pixel intensity from the masked portion of the nuclei 
        image, which is assumed to represent the intensity of individual nuclei. It filters out 
        non-zero intensities to avoid bias due to background noise or other artifacts.
        
        Args:

        Returns:
            float: The mean intensity value of the nucleus pixels in the masked image. If no nuclei 
            are detected (based on non-zero pixel count), it returns 0.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        if len(np.nonzero(self.nuclei_image*self.nuclei_mask)[0])==0:
            return 0
        else:
            return np.mean(np.nonzero(self.nuclei_image.astype(np.float64))) 
            #creating a masked image 

    def get_mean_plaque_intensity(self):
        """
        **get_mean_plaque_intensity Method**
        This function computes and returns the mean intensity of plaques in the fluorescence plate 
        image. It calculates the mean pixel intensity from the plaque image, which is assumed to 
        represent the intensity of individual plaques. It filters out non-zero intensities to avoid 
        bias due to background noise or other artifacts.
        
        Args:

        Returns:
            float: The mean intensity value of the plaque pixels in the image. If no plaques are 
            detected (based on non-zero pixel count), it returns 0.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        if len(np.nonzero(self.plaque_image)[0])==0:
            return 0
        else:
            return np.mean(self.plaque_image.astype(np.float64)) #creating a masked image 

    def get_median_plaque_intensity(self):
        """
        **get_median_plaque_intensity Method**
        This function computes and returns the median intensity of plaques in the fluorescence 
        plate image. It filters out non-zero intensities to avoid bias due to background noise or 
        other artifacts.
        
        Args:

        Returns:
            float: The median intensity value of the plaque pixels in the image. If no plaques are 
            detected (based on non-zero pixel count), it returns 0.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        if len(np.nonzero(self.plaque_image)[0])==0:
            return 0
        else:
            return np.median(self.plaque_image.astype(np.float64))
    
    def get_nuclei_count(self):
        """
        **get_nuclei_count Method**
        This function estimates the number of nuclei in the fluorescence plate based on mask area 
        and average cell size parameters. It calculates the total area of all regions labeled as 
        nuclei within the nuclei mask, then divides this by an average cell area estimated from 
        minimum and maximum cell areas defined in params. It is used for estimating the overall 
        nucleus count in a sample.
        
        Args:

        Returns:
            int: The estimated number of nuclei based on the sum of the nuclei mask area divided by 
            the average cell area.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        nuclei_area_sum = np.sum(self.nuclei_mask)
        return round(nuclei_area_sum/((self.params['min_cell_area'] + 
                                        self.params['max_cell_area'])/2))
    
    def get_plaque_count(self):
        """
        **get_plaque_count Method**
        This function counts the number of plaques in the fluorescence plate image based on a 
        global peak detection. It uses an algorithm to detect plaque masks globally from the 
        plaque image, then counts the number of detected peaks which correspond to individual 
        plaques. It assumes that a peak represents a distinct plaque.
        
        Args:

        Returns:
            int: The total count of plaques as determined by the global peak detection in the 
            plaque image.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        _ ,global_peak_coords = get_plaque_mask(self.plaque_image,self.params)
        if global_peak_coords is None:
            number_of_plaques = 0
        else:
            number_of_plaques = len(global_peak_coords)
        return number_of_plaques

    def get_infected_nuclei_count(self):
        """
        **get_infected_nuclei_count Method**
        This function estimates the number of infected nuclei based on plaque area criteria. It 
        calculates the total area of all regions in the plaque mask that meet the specified 
        size criteria, then divides this by an average cell area estimated from minimum and 
        maximum cell areas defined in params. It can be used for estimating viral 
        load or infection density.
        
        Args:

        Returns:
            int: The estimated number of infected nuclei based on the total plaque area divided 
            by the average cell area.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as 
            specified in the method signature.
        """
        label_image = measure.label(self.plaque_mask)
        label_image[~self.plaque_mask] = 0
        props = measure.regionprops(label_image)
        plaque_region_properties_area = 0
        for prop in props:
            if self.params['use_picks']:
                plaque_area = picks_area(prop.image)
            else:
                plaque_area = prop.area
            if  self.params['min_plaque_area'] < plaque_area:
                plaque_region_properties_area += plaque_area
        return round(plaque_region_properties_area/
                     ((self.params['min_cell_area'] + self.params['max_cell_area'])/2))
    
    def get_lesion_area(self):
        """
        **get_lesion_area Method**
        This function calculates and returns the total area of lesions (plaques) in the fluorescence 
        plate based on the plaque mask. It computes the sum of pixel values within the plaque mask, 
        which corresponds to the total lesion area. It is assumed that a higher value indicates a 
        larger lesion.
        
        Args:

        Returns:
            int: The total area of lesions as calculated from the sum of pixels in the plaque mask.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        return np.sum(self.plaque_mask)
    
    def get_plaque_objects(self):
        """
        **get_plaque_objects Method**
        This function uses image processing techniques to label connected regions in the plaque 
        mask, then filters these regions by size if specified in the params dictionary. It is 
        designed to work with fluorescence plate images where plaques are identified through a mask.
        
        Args:

        Returns:
            list of regionprops objects: A list containing properties of all plaque objects that 
            meet the area criteria defined in params.
            
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
        label_image = measure.label(self.plaque_mask)
        label_image[~self.plaque_mask] = 0
        props = measure.regionprops(label_image)
        plaque_region_properties = []
        for prop in props:
            if self.params['use_picks']:
                plaque_area = picks_area(prop.image)
            else:
                plaque_area = prop.area
            if  self.params['min_plaque_area'] < plaque_area:
                plaque_region_properties.append(prop)
        return plaque_region_properties
    
    def call_plaque_object_readout(self,plaque_object_properties, params):
        """
        **all_plaque_object_readout Method**
        Generates a PlaqueObjectReadout instance by extracting relevant image and mask data from 
        the current WellImageReadout instance.
        
        Args:
            plaque_object_properties (regionprops object, required): The properties of the plaque 
                                                                    object obtained using 
                                                                    skimage.measure.

            params (dict, required): A dictionary containing parameters specific to virus channels, 
                                    which may be used in further analyses or experiments.
            
        Returns:
            PlaqueObjectReadout: An instance of PlaqueObjectReadout encapsulating the extracted 
            image and mask data along with plaque properties.
        
        Raises:
            TypeError: If any of the input arguments do not match their expected types as specified 
            in the method signature.
        """
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
