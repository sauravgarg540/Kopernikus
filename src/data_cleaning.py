import os

from config import *
from utils.general_utils import get_images_per_camera
from utils.image_utils import *

# global values for speed up
# This saves image loading time
img_path_cache = []
image_cache = []


def get_scores_window(window):
    """
    Compute image difference score of the images in a window.
    First image in a window is a base frame and a comparison is made with rest of the frames.

    returns a list of image paths to be removed
    """

    remove = []

    if len(img_path_cache) != 0:
        image_cache.pop(0)
        img_path_cache.pop(0)

    for img_path in window:
        if img_path in img_path_cache:
            continue
        img = cv2.imread(img_path)
        if img is None:
            remove.append(img_path)
            continue
        img = preprocess_image(img, size=(width, height))
        image_cache.append(img)
        img_path_cache.append(img_path)

    base_frame = image_cache[0]
    for i, next_frame in enumerate(image_cache[1:]):
        score, _, _ = compare_frames_change_detection(
            base_frame, next_frame, min_contour_area
        )
        if score < min_score:
            remove.append(img_path_cache[i + 1])
    return remove


def _clean_per_camera(img_paths, window=10):
    """
    Create a window of frames and call a method to get duplicate/similar image paths.
    """

    remove = []

    for i in range(len(img_paths)):
        remove.extend(get_scores_window(img_paths[i : i + window]))
    print(remove)
    return remove


def clean_data(dir):
    """
    Find and remove duplicates/similar images from the dataset
    """

    camera_img_dict = get_images_per_camera(dir)
    for camera, img_paths in camera_img_dict.items():
        removed_paths = list(set(_clean_per_camera(img_paths, window=window)))
        for path in removed_paths:
            os.remove(path)

        # reset cache for next camera
        global image_cache, img_path_cache
        img_path_cache = []
        image_cache = []
