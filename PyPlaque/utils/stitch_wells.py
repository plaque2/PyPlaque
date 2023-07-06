import numpy as np
def stitch_wells(wells: list, nrows: int, ncols: int) -> np.array :
    combined_img = combine_img_blocks(wells, nrows, ncols)
    return combined_img

def combine_img_blocks(img_array: list, nrows: int, ncols: int) -> np.array:
    combined_img = np.array([])
    for k in range(nrows):
        temp = np.concatenate([np.squeeze(img_array[i]) for i in range(ncols)],axis=1).astype(np.float32)
        img_array = img_array[ncols:]
        combined_img = np.vstack([combined_img,temp]).astype(np.float32) if combined_img.size else temp
    return combined_img