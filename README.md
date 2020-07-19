# PyPlaque
Python package for virus plaque analysis based on Plaque2.0


## Classes structure concept

![Classes structure concept](https://user-images.githubusercontent.com/1135672/85918194-705d0a80-b858-11ea-8e56-8cff78ee5b05.png)


## Specific classes

### Sepcimen

#### PlaquesMask class

**PlaquesMask class** designed to hold binary mask of multiple
plaque phenotypes.

_Arguments_:

name - (str, required) string, image sample name for identification

plaques_mask - (np.array, required) numpy array containing
binary mask of all virological plaque objects.

**iterate_palques method** returns a list of individual plaques
stored as binary numpy arrays.

_Arguments_:

min_are - (int, optional, default = 100) a cut-off value for plaque area
in px.

#### PlaqueImageGray class

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

#### PlaquesImageRGB class

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

#### Class PlaquesWell

**Class PlaquesWell** is aimed to contain a full well of a multititre plate.

_Arguments_:

row - (int or str, required) row id of the well.

column - (int or str, required) column id of the well.

well_image - (np.array, required) numpy array containing image of
the well.

well_mask  - (np.array, required) numpy array containing binary mask of
the well.


#### PlateImage Class

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

**Iterate_wells method** returns a list of individual wells of the plate
stored as binary numpy arrays.
___________

### Phenotypes

#### Plaque

**Plaque** class is designed to hold a single virological plaque
phenotype as an object.

_Arguments_:

mask - (required, 2D numpy array) containing binary mask of a single
virological plaque object.

centroid - (float tuple, optional) contains x and y of the centroid of the
plaque object

bbox - (float tuple, optional) contains minr, minc, maxr, maxc of the
plaque object

#### FluorescencePlaque

**FluorescencePlaque** conains plaque obtained from fluorescence image.
Class inherits from Plaque class and is also designed to hold a single
virological plaque phenotype.

_Additonal arguments_:

image - (required) numpy array containing grayscale image of a single
virological plaque object.

#### CrystalVioletPlaque

**CrystalVioletPlaque** plaque obtained from crystal violet image. Class
inherits from Plaque class and is also designed to hold a single virological
plaque phenotype.

_Additonal arguments_:

image - (required) numpy array containing RGB or a graysacle image of a
single virological plaque object.
