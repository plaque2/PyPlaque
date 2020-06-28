# PyPlaque
Python package for virus plaque analysis based on Plaque2.0


## Classes structure concept

![Classes structure concept](https://user-images.githubusercontent.com/1135672/85918194-705d0a80-b858-11ea-8e56-8cff78ee5b05.png)


## Specific classes

### Sepcimen

#### PlaqueImage()
*PlaqueImage* class designed to hold versatile image data containing multiple plaque phenotypes.

_Arguments_:
name - (required) string, image sample name for identification

grayscale - (required) numpy array containing masked grayscale image of a virological plaque object, respective to the mask. Used, in case of measuring properties of fluorescent plaque image.

mask - (optional, default None) numpy array containing binary mask of a single virological plaque object.


### Phenotypes
*Plaque* object class is designed to hold a single virological plaque phenotype.

_Arguments_:
mask - (required) numpy array containing binary mask of a single virological plaque object.

*PlaqueFluorescence* class is designed to hold a plaque obtain from fluorescence image. Class inherits from Plaque class and is also designed to hold a single virological plaque phenotype.

_Additonal arguments_:
image - (required) numpy array containing grayscale image of a single virological plaque object.
