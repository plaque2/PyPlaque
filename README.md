# PyPlaque
Python package for virus plaque analysis based on Plaque2.0

# Installation

See project's PyPi page [https://pypi.org/project/PyPlaque/](https://pypi.org/project/PyPlaque/)

```
pip install PyPlaque
```

# Usage

```
from specimen import PlaquesImageGray
from phenotypes import Plaque
```

Here's a test example of how to analyze plaques in an image using PyPlaque. First let's load an example image:

```
from skimage.io import imsave, imread, imshow

img_url = 'https://raw.github.com/plaque2/matlab/master/Sample_B01_s1_w2.tif'
img = imread(img_url)
imshow(img)
```

![image](https://user-images.githubusercontent.com/1135672/88387118-b8b10f00-cda9-11ea-8d5e-98edff82a80f.png)

Now let's detect plaques in this flourescence microscopy image and print out all their coordinmates:

```
plq_img = PlaquesImageGray('Sample_B01_s1_w2',img, threshold=0.25)
for plq in plq_img.get_plaques():
    print(plq.centroid)
```

This will output following measurements:

```
(435.85833333333335, 1785.8416666666667)
(653.1464788732394, 1209.9647887323943)
(708.058912386707, 1251.6835347432025)
(728.976492712741, 1599.9073812881993)
(712.3316195372751, 1312.491002570694)
(747.0576576576576, 1174.0234234234233)
(752.5772277227722, 1119.0891089108911)
(782.8965517241379, 1151.510344827586)

...
```

Each Plaque object containes a crop of individual virological plaque, as well as, measurements:

```
imshow(plq.mask)
print(plq.area)
```

![image](https://user-images.githubusercontent.com/1135672/88387173-db432800-cda9-11ea-9064-79e075c143ec.png)

___________

## Classes structure concept

![Classes structure concept](https://user-images.githubusercontent.com/1135672/85918194-705d0a80-b858-11ea-8e56-8cff78ee5b05.png)


## Specific classes

### Sepcimen

___________

**PlaquesMask class** designed to hold binary mask of multiple
plaque phenotypes.

_Arguments_:

name - (str, required) string, image sample name for identification

plaques_mask - (np.array, required) numpy array containing
binary mask of all virological plaque objects.

**get_palques method** returns a list of individual plaques
stored as binary numpy arrays.

_Arguments_:

min_are - (int, optional, default = 100) a cut-off value for plaque area
in px.

___________

**PlaqueImageGray class** designed to hold grayscale image data containing
multiple plaque phenotypes with a respective binary mask. The class inherits
from PlaquesMask.

_Additonal arguments_:

name - (str, required) string, image sample name for identification

image - (np.array, required) numpy array containing 2D grayscale image of
a virological plaque object, respective to the mask. Used, in case of
measuring properties of fluorescent plaque image.

plaques_mask - (np.array, optional, default None) numpy array containing
binary mask of all virological plaque objects.

threshold - (float between 0 and 1, optional, default None) fixed threshold
value for creating the binary mask.

sigma - (int, optional, default = 5) guassian blur sigma in pixels used by
the fixed thresholding approach.

Either mask or fixed threshold must be provided
___________

**PlaquesImageRGB class** designed to hold RGB image data containing
multiple plaque phenotypes with a respective binary mask.The class inherits
from PlaquesMask.

_Additonal arguments_:

name - (str, required) image sample name for identification

image - (np.array, required) 3D (red, green, blue) numpy array
containing image of a virological plaque object, respective to the mask.
Used, e.g. in case of measuring properties of crystal violet plaque image.

plaques_mask - (np.array, required) numpy array containing binary mask of all
virological plaque objects.

___________

**Class PlaquesWell** is aimed to contain a full well of a multititre plate.

_Arguments_:

row - (int or str, required) row id of the well.

column - (int or str, required) column id of the well.

well_image - (np.array, required) numpy array containing image of
the well.

well_mask  - (np.array, required) numpy array containing binary mask of
the well.


___________

**PlateImage Class** is aimed to contain a full multititre plate image and
it's respective binary mask.

_Arguments_:

n_rows - (int, required) number of rows in the plate (usually lower than
the number of rows).

n_columns - (int, required) number of columns in the plate (usually higher than
the number of rows).

plate_image - (np.array, required) an image of individual wells of the
plate.

plate_mask - (np.array, required) a binary mask outlining individual wells of the
plate.

**get_wells method** returns a list of individual wells of the plate
stored as binary numpy arrays.
___________

### Phenotypes

___________

**Plaque** class is designed to hold a single virological plaque
phenotype as an object.

_Arguments_:

mask - (required, 2D numpy array) containing binary mask of a single
virological plaque object.

centroid - (float tuple, optional) contains x and y of the centroid of the
plaque object

bbox - (float tuple, optional) contains minr, minc, maxr, maxc of the
plaque object

___________

**FluorescencePlaque** conains plaque obtained from fluorescence image.
Class inherits from Plaque class and is also designed to hold a single
virological plaque phenotype.

_Additonal arguments_:

image - (required) numpy array containing grayscale image of a single
virological plaque object.

___________

**CrystalVioletPlaque** plaque obtained from crystal violet image. Class
inherits from Plaque class and is also designed to hold a single virological
plaque phenotype.

_Additonal arguments_:

image - (required) numpy array containing RGB or a graysacle image of a
single virological plaque object.
