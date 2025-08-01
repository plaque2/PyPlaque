# PyPlaque
We introduce PyPlaque, an open-source Python package focusing on flexibility and modularity rather than a bulky graphic user interface. Unlike previous methods, an abstracted architecture using object-oriented programming allows accommodation of various experimental containers and specimen carriers as data structures while focusing on phenotype-specific information. Aligned with the logical flow of experimental design and desired quantifications, it delivers insights at multiple granularity levels, facilitating detailed analysis. Furthermore, similar design is generalisable to diverse datasets in various biological contexts that fit our structural paradigm.

For further details please look at our paper: [https://www.biorxiv.org/content/10.1101/2024.08.07.603274v1]
___________
## Documentation
The documentation has been added in our GitHub Wiki page [https://github.com/plaque2/PyPlaque/wiki](https://github.com/plaque2/PyPlaque/wiki). Please refer to it for links to our modules and subsequent links to classes and methods/functions for their descriptions.

___________
## Installation
The instructions apply for MacOS, Linux and Windows

You can also look at the project's PyPi page [https://pypi.org/project/PyPlaque/](https://pypi.org/project/PyPlaque/)

```
pip install PyPlaque
```
___________
## Local devloper installation

- Clone repo
- run `pip install -e .`

___________
## Links to Google Colab notebooks for important workflows using the software

- The ```load_data.ipynb``` notebook shows briefly steps to download programmatically the sample data used for analysis in the following notebooks. It specifically used ```curl``` to download the data from publicly published website links. This notebook can be opened in Colab here. <a href="https://colab.research.google.com/github/plaque2/PyPlaque/blob/master/notebooks/load_data.ipynb)" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

- The ```synth.ipynb``` notebook in PyPlaque generates synthetic shapes at random locations (that are seeded for reproducibility) to emulate segmentation masks. These simulated images are wrapped in standard PyPlaque classes like ```FluorescenceMicroscopy``` that treats each image of consisting of synthetic shapes as a fluorescence plate well, enabling seamless integration with the package's analysis and visualization pipelines. This allows us to compare image analysis algorithms' area and perimeter calculations on standard known shapes without relying on real irregular shapes where the true measurements could be ambiguous. This notebook can be tried in Colab here. <a href="https://colab.research.google.com/github/plaque2/PyPlaque/blob/master/notebooks/synthetic_data/synth.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

- The ```example_analysis.ipynb``` notebook demonstrates a systematic and comprehensive analysis workflow using real plaque assay data. It illustrates how to load fluorescence microscopy images of viral plaques using the ```FluorescenceMicroscopy``` class, generate plate level readouts (readouts for all wells of a plate) and filter them into viral and control groups based on well identifier metadata additionally stored in the class. We then use internal visualisation tools to validate our analysis by showcasing comparison barplots for readouts that indicate infectivity that should be different between viral and control wells. This notebook can be tried in Colab here. <a href="https://colab.research.google.com/github/plaque2/PyPlaque/blob/master/notebooks/visualization/example_analysis.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

- The ```cvp_detailed.ipynb``` notebook demonstrates functionality provided by PyPlaque for the analysis of the crystal violet stained plaques using the ```CrystalViolet``` class to load and store crystal violet stained, mobile photography images of viral plaques in 6-well plates available as individual wells. Using inbuilt classes and functions, steps are demonstrated to generate rudimentary binary detection masks for plaques if they are unavailable, stitching individual wells to create partial composite overviews of the plate, detection of plaques based on size criteria from available or generated detection masks, getting measures that describe the shape characteristics and spread of plaques in a well, visualise the spread of plaque measures in a well and finally generate individual well images and well and plaque detection masks from full plate images and full plate well and plaque detection masks in case they are unavailable. This notebook can be tried in Colab here. <a href="https://colab.research.google.com/https://github.com/plaque2/PyPlaque/blob/master/notebooks/cvp_detailed.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

- The ```fp_detailed.ipynb``` notebook demonstrates functionality provided by PyPlaque for the analysis of the fluorescence microscopy plaques using the ```FluorescenceMicroscopy``` class to load and store fluorescence microscopy images of viral plaques in 384-well plates available as individual wells. Using inbuilt classes and functions, steps are demonstrated to load virus and nuclei channel images for the wells, generate binary detection masks for both channels if unavailable, stitching individual wells to create partial composite overviews of the plate, and generation of plate level, well level and plaque level readouts at these 3 granularity levels. This notebook can be tried in Colab here. <a href="https://colab.research.google.com/https://github.com/plaque2/PyPlaque/blob/master/notebooks/fp_detailed.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

  
Note : In notebooks, custom packages and additional data need to be loaded. Load your own data into the Colab environment by connecting via Google Drive or direct upload or using our sample analysis data using the code in the `load_data.ipynb` notebook above and then run the analysis.
  
## Usage
### Fluorescence Plaques

#### 1. Loading packages
```
import matplotlib.pyplot as plt
import numpy as np

from PyPlaque.experiment import FluorescenceMicroscopy
from PyPlaque.utils import remove_background, plot_virus_contours
from PyPlaque.view import PlateReadout

np.random.seed(0)
```
#### 2. Initialising parameters and data
```
base_dir = '../../../data_backup/samples_fluorescent_plaques/'
exp = FluorescenceMicroscopy(base_dir+'images', base_dir+'masks', params = None) 
```

```
plate_dirs, plate_mask_dirs = exp.get_individual_plates(folder_pattern=r'^200601')
print(plate_dirs, plate_mask_dirs)
print(exp.get_number_of_plates())
```
['200601-zplate-g2'] ['200601-zplate-g2']<br/>
1

#### 3. Loading and displaying an example image from the nuclei channel <br/>(plate_id indicates which one of the above read plates are chosen for further analysis)
```
plate_dict_w1 = exp.load_wells_for_plate_nuclei(plate_id=0, additional_subfolders='2020-06-03/2072',
                                                                        file_pattern=r'_A01_s1_w1')
plt.imshow(plate_dict_w1['200601-zplate-g2']['img'][0])
```
![fp_original_image_w1](https://github.com/user-attachments/assets/306d1c9e-3abc-48ba-916d-5f0fb01ef5b4)

#### 4. Display the nuclei mask that is inferred based on flourescence microscopy image and pararmeters default in exp when we do exp.load_wells_for_plate_nuclei():

```
_, ax = plt.subplots(figsize=(8, 8))
ax.imshow(plate_dict_w1[plate_dirs[0]]['mask'][0], cmap='gray')
plt.show()
```
![fp_nuclei_mask_w1](https://github.com/user-attachments/assets/fb573cca-38c3-4026-b2d3-d17f8c25ecda)

#### 5. Similarly for the virus channel
```
plate_dict_w2 = exp.load_wells_for_plate_virus(plate_id=0, additional_subfolders='2020-06-03/2072',
                                                file_pattern=r'_A01_s1_w2')
plt.imshow(plate_dict_w2['200601-zplate-g2']['img'][0])


_, ax = plt.subplots(figsize=(8, 8))
ax.imshow(plate_dict_w2[plate_dirs[0]]['mask'][0],cmap='gray')
plt.show()
```
![fp_original_image_w2](https://github.com/user-attachments/assets/97cc94b1-ceea-4b92-84ac-8d143d87d823)
![fp_plaque_mask_w2](https://github.com/user-attachments/assets/736dac7b-62da-45bb-97dc-8c144257021c)

#### 6. We can also plot the contours of the virus and a local maxima for each plaque

```
plot_virus_contours(img, virus_params=exp.params['virus'])

```
![fp_plaque_mask_outline_w2](https://github.com/user-attachments/assets/ef0730e0-581c-48f6-aae2-959dc4d211eb)

### Crystal Violet Plaques

#### 1. Loading packages
```
import matplotlib.pyplot as plt
import pandas as pd
from tqdm.auto import tqdm

from PyPlaque.experiment import CrystalViolet
from PyPlaque.specimen import PlaquesMask
from PyPlaque.utils import plot_bbox_plaques_mask, boxplot_quants
```
#### 2. Initialising parameters and data
```
base_dir = '../../../data_backup/samples_crystal_violet_plaques/'

exp = CrystalViolet(base_dir+'plaques_image_png/', base_dir+'plaques_mask_png/',
                                        params = None)
```
```
plate_dirs, plate_mask_dirs = exp.get_individual_plates(folder_pattern=r'6446$')
print(plate_dirs, plate_mask_dirs)
print(exp.get_number_of_plates())
```
['IMG_6446'] ['IMG_6446']<br/>
1

#### 3. Loading and displaying an example image from the plate <br/>(plate_id indicates which one of the above read plates are chosen for further analysis)
```
plate_dict = exp.load_well_images_and_masks_for_plate(plate_id=0, additional_subfolders=None,
                                                            all_grayscale=True, file_pattern=None)
plt.figure()
plt.imshow(plate_dict[plate_dirs[0]]['img'][0], cmap='gray')

plt.figure()
plt.imshow(plate_dict[plate_dirs[0]]['mask'][0],cmap='gray')
```
![grayscale_well_image_6446_00](https://github.com/user-attachments/assets/5388ef1e-48c3-4539-84d7-e9a57a8dc749)<br/>
![plaque_mask_6446_00](https://github.com/user-attachments/assets/f1daa850-1807-415b-8148-4f48ef128aec)

#### 4. Display masked plaques based on flourescence microscopy image and mask stored when we ran in exp when we do exp.load_well_images_and_masks_for_plate():
```
plate_dict = exp.extract_masked_wells(plate_id=0)
i = 0
j = 0
plt.figure()
plt.axis('off')
plt.title(plate_dirs[0]+"-"+str(i)+","+str(j))
plt.imshow(plate_dict[plate_dirs[0]]['masked_img'][0], cmap='gray')
```
![masked_plaques_6446_00](https://github.com/user-attachments/assets/9a27415d-bca7-4d1e-a025-1dc2e177e4a1)

#### 5. Getting plaque counts
```
plaques_mask_gt_list = [PlaquesMask(name = str(plate_dict[plate_dirs[0]]['image_name'][i]),
                                plaques_mask = plate_dict[plate_dirs[0]]['mask'][i]) 
                    for i in tqdm(range(len(plate_dict[plate_dirs[0]]['img'])))]
plaques_count_gt_list = [len(plq_mask.get_plaques()) for plq_mask in tqdm(plaques_mask_gt_list)]

[print(plq_mask.name, " : ", plq_count, "\n") 
        for (plq_mask, plq_count) in tqdm(list(zip(plaques_mask_gt_list, plaques_count_gt_list)))]
```
100%|██████████| 6/6 [00:00<00:00, 127745.30it/s]<br/>
100%|██████████| 6/6 [00:01<00:00,  3.48it/s]<br/>
100%|██████████| 6/6 [00:00<00:00, 70690.52it/s]<br/>
../../../data_backup/samples_crystal_violet_plaques/plaques_image_png/IMG_6446/IMG_6446.png_1.png  :  116 <br/>

../../../data_backup/samples_crystal_violet_plaques/plaques_image_png/IMG_6446/IMG_6446.png_2.png  :  143 <br/>

../../../data_backup/samples_crystal_violet_plaques/plaques_image_png/IMG_6446/IMG_6446.png_3.png  :  223 <br/>

../../../data_backup/samples_crystal_violet_plaques/plaques_image_png/IMG_6446/IMG_6446.png_4.png  :  61 <br/>

../../../data_backup/samples_crystal_violet_plaques/plaques_image_png/IMG_6446/IMG_6446.png_5.png  :  3 <br/>

../../../data_backup/samples_crystal_violet_plaques/plaques_image_png/IMG_6446/IMG_6446.png_6.png  :  1 

#### 6. Generating and displaying generated mask of plaques in case one isn't available<br/>
(simply set read_mask=False in exp.load_well_images_and_masks_for_plate())
```
exp2 = CrystalViolet(base_dir+'plaques_image_png/', base_dir+'plaques_mask_png/',
                                        params = None) # default values in class, option to update
_, _ = exp2.get_individual_plates(folder_pattern=r'6446$')
plate_dict_no_mask = exp2.load_well_images_and_masks_for_plate(plate_id=0,
                additional_subfolders=None, read_mask=False, all_grayscale=True, 
                file_pattern=r'png_1')
print(plate_dict_no_mask[plate_dirs[0]]['image_name'][0])
plt.imshow(plate_dict_no_mask[plate_dirs[0]]['mask'][0], cmap='gray')
```
![generated_plaque_mask_6446_00](https://github.com/user-attachments/assets/4d7cf0f6-60c9-4488-b7ed-00cf79fe659b)

___________

## Hierarchical Class Structure

![fig1](https://github.com/user-attachments/assets/65f4d2c5-2be0-44fd-8fdb-09a0507f16ea)
![fig2](https://github.com/user-attachments/assets/da0dda26-d7fb-4bed-85a6-1e4d0a4f5dac)


## For further clarifications or queries, please contact:
1. Trina De (https://orcid.org/0000-0003-1111-9851)
2. Dr. Artur Yakimovich (https://orcid.org/0000-0003-2458-4904)
3. Dr. Vardan Andriasyan (https://orcid.org/0000-0002-9619-6655)
