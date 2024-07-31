import numpy as np
import pandas as pd
from tqdm.auto import tqdm

from PyPlaque.view import WellImageReadout

class PlateReadout:
    """
    **PlateReadout Class** 
    The PlateReadout Class is aimed to contain readouts of multiple wells of a single plate 
    of a Fluorescence Plaque.

    Attributes:
        experiment (object, required): FluorescenceMicroscopy class object initialized with 
                    parameters and data of well plate of Fluorescence Plaques loaded.
        
        plate_id (int, optional): Identifier for the plate. Default is 0.
        
        well_level_readouts (bool, optional): Flag to indicate whether to include well-level 
                    readouts. Default is True.
        
        object_level_readouts (bool, optional): Flag to indicate whether to include object-level 
                    readouts. Default is True.

    Raises:
        ValueError: If both types of readouts are set to False. At least one should be True. 
        Please check again.
    """

    def __init__(self,
                experiment,
                plate_id = 0,
                well_level_readouts=True,
                object_level_readouts=True):
        self.experiment = experiment
        self.plate_id = plate_id
        self.well_level_readouts = well_level_readouts
        self.object_level_readouts = object_level_readouts

        if well_level_readouts == False and object_level_readouts==False:
            raise ValueError("Both types of readouts are set to False. At least one should be \
            True. Please check again.")

    def generate_readouts_dataframe(self, 
                                    row_pattern = r'([A-Z]{1})[0-9]{2}', 
                                    column_pattern = r'[A-Z]{1}([0-9]{2})'):
        """
        **generate_readouts_dataframe Method**
        
        Processes a list of plaque object readouts to generate summary statistics at both levels.

        Args:
            row_pattern (regex, optional): A regular expression to find the row identifier in the 
                                        well name.
            column_pattern (regex, optional): A regular expression to find the column identifier in 
                                            the well name.

        Returns:
            - If both well and object level readouts are present:
                abs_df_well (pd.DataFrame): A DataFrame containing well-level summary statistics.
                abs_df_object (pd.DataFrame): A DataFrame containing object-level summary statistics.
            - If only well level readouts are present:
                abs_df_well (pd.DataFrame): A DataFrame containing well-level summary statistics.
            - If only object level readouts are present:
                abs_df_object (pd.DataFrame): A DataFrame containing object-level summary statistics.
        Raises:
            Any exceptions that might be raised by the methods called on plq_object_readouts 
            or during dataframe creation can be handled here, but this method does not explicitly 
            raise any errors itself.
        """
        d = self.experiment.plate_indiv_dir[self.plate_id]
        if len(self.experiment.plate_dict_w1[d]['img']) != len(
                                                        self.experiment.plate_dict_w2[d]['img']):
            raise ValueError("Expected equal number of image names, images and masks for \
            both channels.Please check again.")
        
        abs_df_well = pd.DataFrame()
        abs_df_object = pd.DataFrame()

        # For readouts at the well level
        virus_image_name = [] 
        nuclei_image_name = []
        max_nuclei_intensity_abs = []
        total_nuclei_intensity_abs = []
        mean_nuclei_intensity_abs = []
        nuclei_count_abs = []
        max_plaque_intensity_abs = []
        total_plaque_intensity_abs = []
        mean_plaque_intensity_abs = []
        plaque_count_abs = []
        infected_nuclei_count_abs = []

        # For readouts at the object level
        well_row = []
        well_column = []
        area_abs = []
        centroid_1_abs = []
        centroid_2_abs = []
        major_axis_length_abs = []
        minor_axis_length_abs = []
        eccentricity_abs = []
        convex_area_abs = []
        roundness_abs = []
        peak_counts_abs = []
        nuclei_in_plaque_abs = []
        infected_nuclei_in_plaque_abs = []
        max_intensity_GFP_abs = []
        total_intensity_GFP_abs = []
        mean_intensity_GFP_abs = []

        #Assuming that w1 is the nuclei channel and w2 as the plaque channel
        for i in tqdm(range(len(self.experiment.plate_dict_w2[d]['img']))):
            plq_image_readout = WellImageReadout(nuclei_image_name=
            str(self.experiment.plate_dict_w1[d]['image_name'][i]).split("/")[-1],
            plaque_image_name=str(self.experiment.plate_dict_w2[d]['image_name'][i]).split("/")[-1],
            nuclei_image=np.array(self.experiment.plate_dict_w1[d]['img'][i]),
            plaque_image=np.array(self.experiment.plate_dict_w2[d]['img'][i]),
            nuclei_mask=np.array(self.experiment.plate_dict_w1[d]['mask'][i]),
            plaque_mask=np.array(self.experiment.plate_dict_w2[d]['mask'][i]),
            virus_params = self.experiment.params['virus'])

            if self.well_level_readouts:
                virus_image_name.append(plq_image_readout.plaque_image_name)
                nuclei_image_name.append(plq_image_readout.nuclei_image_name)
                max_nuclei_intensity_abs.append(plq_image_readout.get_max_nuclei_intensity())
                total_nuclei_intensity_abs.append(plq_image_readout.get_total_nuclei_intensity())
                mean_nuclei_intensity_abs.append(plq_image_readout.get_mean_nuclei_intensity())
                nuclei_count_abs.append(plq_image_readout.get_nuclei_count())
                max_plaque_intensity_abs.append(plq_image_readout.get_max_plaque_intensity())
                total_plaque_intensity_abs.append(plq_image_readout.get_total_plaque_intensity())
                mean_plaque_intensity_abs.append(plq_image_readout.get_mean_plaque_intensity())
                plaque_count_abs.append(plq_image_readout.get_plaque_count())
                infected_nuclei_count_abs.append(plq_image_readout.get_infected_nuclei_count())
            if self.object_level_readouts:
                plq_objects = plq_image_readout.get_plaque_objects()

                well_row.append(plq_image_readout.get_row(row_pattern = row_pattern))
                well_column.append(plq_image_readout.get_column(column_pattern = column_pattern))

                if len(plq_objects) != 0:
                    plq_object_readouts = [plq_image_readout.call_plaque_object_readout(plq_object,
                    self.experiment.params['virus']) for plq_object in plq_objects]

                

                if len(plq_objects) != 0:
                    area_abs.append(np.mean([plq_object_readout.get_area() 
                    for plq_object_readout in plq_object_readouts]))
                    centroid_1_abs.append(np.mean([plq_object_readout.get_centroid()[0] 
                    for plq_object_readout in plq_object_readouts]))
                    centroid_2_abs.append(np.mean([plq_object_readout.get_centroid()[1] 
                    for plq_object_readout in plq_object_readouts]))
                    major_axis_length_abs.append(np.mean([
                        plq_object_readout.get_major_minor_axis_length()[0] 
                        for plq_object_readout in plq_object_readouts]))
                    minor_axis_length_abs.append(np.mean([
                        plq_object_readout.get_major_minor_axis_length()[1] 
                        for plq_object_readout in plq_object_readouts]))
                    eccentricity_abs.append(np.mean([plq_object_readout.get_eccentricity() 
                    for plq_object_readout in plq_object_readouts]))
                    convex_area_abs.append(np.mean([plq_object_readout.get_convex_area() 
                    for plq_object_readout in plq_object_readouts]))
                    roundness_abs.append(np.mean([plq_object_readout.get_roundness() 
                    for plq_object_readout in plq_object_readouts]))
                    peak_counts_abs.append(np.mean([len(plq_object_readout.get_number_of_peaks()) 
                    for plq_object_readout in plq_object_readouts]))
                    nuclei_in_plaque_abs.append(np.mean([plq_object_readout.get_nuclei_in_plaque() 
                    for plq_object_readout in plq_object_readouts]))
                    infected_nuclei_in_plaque_abs.append(np.mean([
                        plq_object_readout.get_infected_nuclei_in_plaque() 
                        for plq_object_readout in plq_object_readouts]))
                    max_intensity_GFP_abs.append(np.mean([plq_object_readout.get_max_intensity_GFP() 
                    for plq_object_readout in plq_object_readouts]))
                    total_intensity_GFP_abs.append(np.mean([
                        plq_object_readout.get_total_intensity_GFP() 
                        for plq_object_readout in plq_object_readouts]))
                    mean_intensity_GFP_abs.append(np.mean([
                        plq_object_readout.get_mean_intensity_GFP() 
                        for plq_object_readout in plq_object_readouts]))
                else:
                    area_abs.append(0)
                    centroid_1_abs.append(0)
                    centroid_2_abs.append(0)
                    major_axis_length_abs.append(0)
                    minor_axis_length_abs.append(0)
                    eccentricity_abs.append(0)
                    convex_area_abs.append(0)
                    roundness_abs.append(0)
                    peak_counts_abs.append(0)
                    nuclei_in_plaque_abs.append(0)
                    infected_nuclei_in_plaque_abs.append(0)
                    max_intensity_GFP_abs.append(0)
                    total_intensity_GFP_abs.append(0)
                    mean_intensity_GFP_abs.append(0)
        
        if self.well_level_readouts:
            abs_df_well['NucleiImageName'] = nuclei_image_name
            abs_df_well['VirusImageName'] = virus_image_name
            abs_df_well['maxNucleiIntensity'] = max_nuclei_intensity_abs
            abs_df_well['totalNucleiIntensity'] = total_nuclei_intensity_abs
            abs_df_well['meanNucleiIntensity'] = mean_nuclei_intensity_abs
            abs_df_well['numberOfNuclei'] = nuclei_count_abs
            abs_df_well['maxVirusIntensity'] = max_plaque_intensity_abs
            abs_df_well['totalVirusIntensity'] = total_plaque_intensity_abs
            abs_df_well['meanVirusIntensity'] = mean_plaque_intensity_abs
            abs_df_well['numberOfPlaques'] = plaque_count_abs
            abs_df_well['numberOfInfectedNuclei'] = infected_nuclei_count_abs
        if self.object_level_readouts:
            abs_df_object['wellRow'] = well_row
            abs_df_object['wellColumn'] = well_column
            abs_df_object['Area'] = area_abs
            abs_df_object['Centroid_1'] = centroid_1_abs
            abs_df_object['Centroid_2'] = centroid_2_abs
            abs_df_object['MajorAxisLength'] = major_axis_length_abs
            abs_df_object['MinorAxisLength'] = minor_axis_length_abs
            abs_df_object['Eccentricity'] = eccentricity_abs
            abs_df_object['ConvexArea'] = convex_area_abs
            abs_df_object['Roundness'] = roundness_abs
            abs_df_object['numberOfPeaks'] = peak_counts_abs
            abs_df_object['numberOfNucleiInPlaque'] = nuclei_in_plaque_abs
            abs_df_object['numberOfInfectedNucleiInPlaque'] = infected_nuclei_in_plaque_abs
            abs_df_object['maxIntensityGFP'] = max_intensity_GFP_abs
            abs_df_object['totalIntensityGFP'] = total_intensity_GFP_abs
            abs_df_object['meanIntensityGFP'] = mean_intensity_GFP_abs


        if (self.well_level_readouts and self.object_level_readouts):
            return abs_df_well, abs_df_object
        elif (self.well_level_readouts and not self.object_level_readouts):
            return abs_df_well
        elif (not self.well_level_readouts and self.object_level_readouts):
            return abs_df_object
            


