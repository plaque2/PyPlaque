import cv2
import numpy as np
import re
import skimage

from PyPlaque.utils import picks_area, picks_perimeter

class PlaqueObjectReadout:
    """
    **Class PlaqueObjectReadout** is designed to encapsulate data related to a single instance of a 
    plaque from a fluorescence plaque well.
    
    Attributes:
        nuclei_image_name (str, required): The name of the nuclei image, which serves as an 
                                        identifier for the nuclei image.

        nuclei_object (np.ndarray, required): A 2D numpy array representing the image of the nuclei 
                                            image.
        
        nuclei_object_mask (np.ndarray, required): A 2D numpy array serving as a mask for the nuclei 
                                                image.
        
        plaque_image_name (str, required): The name of the plaque image plate, which serves as an 
                                        identifier for the plaque image.
        
        plaque_object (np.ndarray, required): A 2D numpy array representing the image of the plaque 
                                            image.
        
        plaque_object_mask (np.ndarray, required): A 2D numpy array serving as a mask for the plaque 
                                                image.
        
        plaque_object_properties (regionprops object, required): Properties of the plaque object, 
                                                        typically obtained using `skimage.measure`.
        
        virus_params (dict, required): A dictionary containing parameters specific to the virus 
                                    channel, which can be used in further analyses or experiments.
        
    Raises:
        TypeError: If the data types for any of the arguments do not match their expected types 
        as specified in the class definition.
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
        """
        **get_row Method**
        
        Searches for and returns the first match of a specified row pattern in the nuclei image 
        name. The method uses the regular expression module `re` to find matches within the string 
        representing the nuclei image name. 
        
        Args:
            row_pattern (str or re.Pattern, optional): A regular expression pattern as a string or 
                                                    compiled regular expression object used for 
                                                    matching against the nuclei image name. If not 
                                                    provided, the default pattern associated with 
                                                    the object is used.
                                            
        Returns:
            str: The first match found in the nuclei image name based on the given row pattern.
            
        Raises:
            IndexError: If there are no matches found and the function tries to access an element 
                        of a non-existing list, this error may be raised. Ensure that the pattern 
                        provided is appropriate for the string format or consider adding checks 
                        before accessing results.
        """
        return re.findall(row_pattern, self.nuclei_image_name)[0]
        
    def get_column(self, column_pattern=None):
        """
        **get_column Method**
        
        Searches for and returns the first match of a specified column pattern in the nuclei 
        image name. The method uses the regular expression module `re` to find matches within the 
        string representing the nuclei image name. If no pattern is provided, it defaults to using 
        the one stored with the object.
        
        Args:
            column_pattern (str or re.Pattern, optional): A regular expression pattern as a string 
                                                or compiled regular expression object used for 
                                                matching against the nuclei image name. If not 
                                                provided, the default pattern associated with the 
                                                object is used.
                                                
        Returns:
            str: The first match found in the nuclei image name based on the given column pattern.
            
        Raises:
            IndexError: If there are no matches found and the function tries to access an element 
            of a non-existing list, this error may be raised. Ensure that the pattern provided is 
            appropriate for the string format or consider adding checks before accessing results.
        """
        return re.findall(column_pattern, self.nuclei_image_name)[0]
    
    def get_area(self):
        """
        **get_area Method**
        
        Returns the area of the plaque object. If the parameter 'use_picks' is set to True, 
        this method uses Pick's measurements to calculate the area; otherwise, it calculates the 
        area by summing the pixel values of the binary representation of the plaque object.
        
        Args:

        Returns:
            float or int: The calculated or retrieved area of the plaque object.
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        if self.params['use_picks']:
            return picks_area(self.plaque_object_properties.image)
        else:
            return np.sum(self.plaque_object_properties.image.astype(np.float64))
      
    def get_perimeter(self):
        """
        **get_perimeter Method**
        
        Returns the perimeter of the plaque object. If the parameter 'use_picks' is set to True, 
        this method uses Picks' measurements to calculate the perimeter; otherwise, it returns the 
        stored perimeter value from the properties of the plaque object's image.
        
        Args:

        Returns:
            float or int: The calculated or retrieved perimeter of the plaque object. 
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        if self.params['use_picks']:
            return picks_perimeter(self.plaque_object_properties.image)
        else:
            return self.plaque_object_properties.perimeter

    def get_centroid(self):
        """
        **get_centroid Method**
        
        Returns the centroid coordinates of the plaque object. The centroid is a property derived 
        from the properties of the plaque object's image, specifically its moments which are used 
        to calculate the center of mass.
        
        Args:

        Returns:
            tuple: A tuple (x_coordinate, y_coordinate) representing the centroid coordinates of 
            the plaque object.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        return self.plaque_object_properties.centroid
    
    def get_bbox(self):
        """
        **get_bbox Method**
        
        Returns the bounding box coordinates of the plaque object. The bounding box is derived 
        from the properties of the plaque object's image, specifically its minimum bounding 
        rectangle. This method returns a tuple containing the x-coordinate and y-coordinate of the 
        top-left corner of the bounding box, followed by the width and height of the box.
        
        Args:
        
        Returns:
            tuple: A tuple (x1, y1, width, height) where (x1, y1) is the coordinate of the top-left 
            corner of the bounding box, and width and height are its dimensions.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        return (self.plaque_object_properties.bbox[0], \
                self.plaque_object_properties.bbox[3], \
                self.plaque_object_properties.bbox[2] - self.plaque_object_properties.bbox[0], \
                self.plaque_object_properties.bbox[3] - self.plaque_object_properties.bbox[1])

    def get_major_minor_axis_length(self):
        """
        **get_major_minor_axis_length Method**
        
        Returns the lengths of the major and minor axes of the ellipse fitted to the plaque 
        object's contour. These lengths are properties derived from the convex hull transformation 
        of the plaque object's image.
        
        Args:
        
        Returns:
            tuple: A tuple containing two float values, the first being the length of the major 
            axis and the second being the length of the minor axis.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        return self.plaque_object_properties.axis_major_length, \
                self.plaque_object_properties.axis_minor_length
    
    def eccentricity(self):
        """
        **eccentricity Method**
        
        Calculates and returns the eccentricity of the plaque object. The eccentricity is 
        determined by fitting an ellipse to the contour of the plaque and calculating it based on 
        the ratio of the semi-major axis (a) to the semi-minor axis (b), using the formula 
        sqrt(1 - (b^2 / a^2)). This method finds the first contour with more than five points, 
        fits an ellipse to it, and computes the eccentricity. If no suitable contours are found or 
        if the rotation angle of the fitted ellipse is zero, resulting values may not be reliable.
        
        Args:
        
        Returns:
            float: The calculated eccentricity value of the plaque object.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
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
        """
        **get_eccentricity Method**
        
        Calls and returns the result of the eccentricity calculation for the plaque object. 
        This method simply wraps a call to the private method `eccentricity()` to retrieve the 
        eccentricity value of the plaque object.
        
        Args:
        
        Returns:
            float: The calculated eccentricity value of the plaque object as obtained from the 
            `eccentricity()` method.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """

        return self.eccentricity()
    
    def get_convex_area(self):
        """
        **get_convex_area Method**
        
        Returns the convex area of the plaque object, which is a property derived from its convex 
        hull transformation.
        
        Args:
        
        Returns:
            float: The convex area of the plaque object.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """

        return self.plaque_object_properties.area_convex
    
    def roundness(self):
        """
        **roundness Method**
        
        Calculates and returns the roundness of the plaque object. The roundness is determined 
        based on the perimeter and area of the plaque object, using either Pick's measurements or 
        bounding box calculations if Pick's is not used.
        
        Args:
        
        Returns:
            float: The calculated roundness value of the plaque object.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
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
        """
        **get_roundness Method**
        
        Calls and returns the result of the roundness calculation for the plaque object. 
        This method simply wraps a call to the private method `roundness()` to retrieve the 
        roundness value of the plaque object.
        
        Args:
        
        Returns:
            float: The calculated roundness value of the plaque object as obtained from the 
            `roundness()` method.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        return self.roundness()
    
    def get_number_of_peaks(self):
        """
        **get_number_of_peaks Method**
        
        Identifies and returns the coordinates of peaks in the plaque object based on a 
        Gaussian-blurred image. The method applies a Gaussian filter to enhance peak detection, 
        then uses skimage.feature.peak_local_max to find local maxima.
        
        Args:
        
        Returns:
            numpy.ndarray or None: An array of shape (N, 2) containing the coordinates of peaks if 
            fine plaque detection is enabled; otherwise, returns None.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
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
        """
        **get_nuclei_in_plaque Method**
        
        Calculates and returns the number of nuclei in the plaque. The method uses a mask to 
        identify areas where both the plaque object (after convex hull transformation) and 
        the nuclei object are non-zero, then calculates the sum of these areas to estimate the 
        number of cells. It optionally uses Pick's measurements for cell area if specified.

        Args:
        
        Returns:
            float: The estimated number of nuclei in the plaque based on the masked areas.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        mask = self.plaque_object_properties.image_convex * self.nuclei_object_mask
        if self.params['use_picks']:
            nuclei_area_sum = picks_area(mask)
        else:
            nuclei_area_sum = np.sum(mask)
        return nuclei_area_sum/((self.params['min_cell_area'] + self.params['max_cell_area'])/2)
    
    def get_infected_nuclei_in_plaque(self):
        """
        **get_infected_nuclei_in_plaque Method**
        
        Calculates and returns the number of infected nuclei in the plaque. The method uses a mask 
        to identify areas where both the plaque object and the nuclei object are non-zero, then 
        calculates the sum of these areas to estimate the number of infected cells. It optionally 
        uses Pick's measurement for cell area if specified.

        Args:
        
        Returns:
            float: The estimated number of infected nuclei in the plaque based on the masked areas.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be handled 
            here, but this method does not explicitly raise any errors itself.
        """
        mask = self.plaque_object_mask * self.nuclei_object_mask
        if self.params['use_picks']:
            nuclei_area_sum = picks_area(mask)
        else:
            nuclei_area_sum = np.sum(mask)
        return nuclei_area_sum/((self.params['min_cell_area'] + self.params['max_cell_area'])/2)
    
    def get_max_intensity_GFP(self):
        """
        **get_max_intensity_GFP Method**
        
        Calculates and returns the maximum intensity of GFP in the plaque object.

        Args:
        
        Returns:
            float: The maximum intensity of GFP in the plaque object, calculated as the 
            maximum value after applying the mask to the plaque image.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        return np.max(self.plaque_object*self.plaque_object_mask) #creating a masked image 
    
    def get_total_intensity_GFP(self):
        """
        **get_total_intensity_GFP Method**
        
        Calculates and returns the total intensity of GFP in the plaque object.

        Args:
        
        Returns:
            float: The total intensity of GFP in the plaque object, calculated as the sum of 
            non-zero values after applying the mask.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can 
            be handled here, but this method does not explicitly raise any errors itself.
        """
        return np.sum(self.plaque_object*self.plaque_object_mask) #creating a masked image 

    def get_mean_intensity_GFP(self):
        """
        **get_mean_intensity_GFP Method**
        
        Calculates and returns the mean intensity of GFP in the plaque object.

        Args:
        
        Returns:
            float: The mean intensity of GFP in the plaque object, or 0 if no non-zero values 
            are found.
            
        Raises:
            Any exceptions that might be raised by the operations within this method can be 
            handled here, but this method does not explicitly raise any errors itself.
        """
        if len(np.nonzero(self.plaque_object*self.plaque_object_mask)[0])==0:
            return 0
        else:
            return np.mean(np.nonzero(self.plaque_object*self.plaque_object_mask)) 
            #creating a masked image 
