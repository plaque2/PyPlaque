from skimage.filters import gaussian

def check_numbers(tup):
    for idx,i in enumerate(tup):
        if (not type(tup[idx]) is int) or (not type(tup[idx]) is float):
            return False
    return True

def fixed_threshold(img, thr, s):
        img = gaussian(img, sigma = s)
        img[img > thr] = 1
        img[img <= thr] = 0
        return img