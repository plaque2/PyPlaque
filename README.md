# PyPlaque
We introduce PyPlaque, an open-source Python package focusing on flexibility and modularity rather than a bulky graphic user interface. Unlike previous methods, an abstracted architecture using object-oriented programming allows accommodation of various experimental containers and specimen carriers as data structures while focusing on phenotype-specific information. Aligned with the logical flow of experimental design and desired quantifications, it delivers insights at multiple granularity levels, facilitating detailed analysis. Furthermore, similar design is generalisable to diverse datasets in various biological contexts that fit our structural paradigm.

For further details please look at our paper: [https://www.biorxiv.org/content/10.1101/2024.08.07.603274v1]
___________
## Version
New release v0.2.0

___________
## Installation

See project's PyPi page [https://pypi.org/project/PyPlaque/](https://pypi.org/project/PyPlaque/)

```
pip install PyPlaque
```
___________
## Local devloper installation

- Clone repo
- run `pip install -e .`

___________
## Documentation
To be added in a separate webpage. Please refer to scripts in the repository now.

___________
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

___________
## Class Types

### Experiment
1. CrystalViolet - This class is designed to contain metadata of multiple instances of a multititre plate of 
  Crystal Violet plaques.
2. FluorescenceMicroscopy -  This class is designed to contain metadata of multiple instances of a multititre plate of Fluorescence 
  plaques.

### Specimen
1. PlaquesImageGray - This class is designed to hold grayscale image data containing multiple plaque phenotypes with a 
  respective binary mask. The class inherits from PlaquesMask.
2. PlaquesImageRGB - The class is designed to hold RGB image data containing multiple plaque phenotypes with a 
  respective binary mask. The class inherits from PlaquesMask.
3. PlaquesMask - This class is designed to hold a binary mask of multiple plaque instances in a well.
4. PlaquesWell - This class is designed to contain a full well of a multititre plate
   
### Phenotypes
1. CrystalVioletPlaque - This class contains a plaque obtained from crystal violet image. Class inherits from Plaque class 
  and is also designed to hold a single virological plaque phenotype.
2. FluorescencePlaque - This class contains a plaque obtained from fluorescence image. Class inherits from Plaque class 
  and is also designed to hold a single virological plaque phenotype.
3. Plaque - This class is designed to hold a single virological plaque phenotype as an object. It 
  encapsulates the properties and behaviors related to a specific plaque, including its mask, 
  centroid coordinates, bounding box, and usage preference for pick measurements.

### View
1. WellImageReadout - This class encapsulates metadata related to multiple instances of plaques 
    within a single well of a fluorescence plate.
2. PlaqueObjectReadout - This class encapsulate data related to a single instance of a 
    plaque from a fluorescence plaque well.
3. PlateReadout -  This class contains readouts of multiple wells of a single plate 
    of a Fluorescence Plaque.
4. PlateImage - This class encapsulates a full multi-title plate image and 
  its corresponding binary mask. It provides methods to extract individual well images 
  from the plate based on specified criteria, visualize these wells annotated with their positions, 
  and more.

For more information about class attributes and functions please refer to scripts in the repository.
___________

## For further clarifications or queries, please contact:
1. Trina De (https://orcid.org/0000-0003-1111-9851)
2. Dr. Artur Yakimovich (https://orcid.org/0000-0003-2458-4904)
3. Dr. Vardan Andriasyan (https://orcid.org/0000-0002-9619-6655)
