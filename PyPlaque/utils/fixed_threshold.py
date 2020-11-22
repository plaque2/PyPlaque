from skimage.filters import gaussian

def fixed_threshold(img, thr, s):
        img = gaussian(img, sigma = s)
        img[img > thr] = 1
        img[img <= thr] = 0
        return img