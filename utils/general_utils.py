import glob
import mimetypes
import os
from datetime import datetime

mimetypes.init()


def get_extension(filepath):
    """Return extension for a path"""
    return os.path.splitext(os.path.basename(filepath))[1]


def get_extensions_for_type(file_type="image"):
    """
    Get all available extensions for a file_type(image/video/audio)
    """

    file_type = file_type.lower()
    assert file_type in [
        "image",
        "video",
        "audio",
    ], "Invalid file_type, please choose one of [image, video, audio]"

    extensions = []
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == file_type:
            extensions.append(ext)
    return extensions


def get_timestamp(path):
    """ "
    Get Unix timestamp from image path
    """

    basename = os.path.basename(path)
    im_name = os.path.splitext(basename)[0]

    # image names are as follows:
    # cameraid_date or cameraid-unixtimestamp

    if '-' not in im_name:
        timestamp = "_".join(im_name.split("_")[1:])
        dt = datetime.strptime(timestamp, "%Y_%m_%d__%H_%M_%S")
        dt = str(int(datetime.timestamp(dt) * 1000))
    else:
        dt = im_name.split("-")[1]
    return dt


def get_camera_id(path):
    """ "
    Get camera id from path of an image
    """
    basename = os.path.basename(path)
    im_name = os.path.splitext(basename)[0]

    # image names are as follows:
    # cameraid_date or cameraid-unixtimestamp
    _id = None
    if '-' not in im_name:
        _id = im_name.split("_")[0]
    else:
        _id = im_name.split("-")[0]
    assert _id is not None, f"camera id is None for {basename}"
    return _id


def get_image_list(data_dir, recursive=True):
    """ "
    Get list of all images in a directory
    """

    extension_list = get_extensions_for_type()
    image_path_list = []
    if recursive:
        image_path_list += glob.glob(os.path.join(data_dir, "**", "*"), recursive=True)
    else:
        image_path_list += glob.glob(os.path.join(data_dir, "*"))
    image_path_list = [
        image_path
        for image_path in image_path_list
        if get_extension(image_path) in extension_list
    ]

    # sort images based on timestamp
    return sorted(image_path_list, key=lambda x: get_timestamp(x))


def get_images_per_camera(dir):
    """
    Get all images in a directory
    """

    image_paths = get_image_list(dir)

    camera_img_dict = {}

    for img_path in image_paths:
        _id = get_camera_id(img_path)
        if _id not in camera_img_dict:
            camera_img_dict[_id] = [img_path]
        else:
            camera_img_dict[_id].append(img_path)

    return camera_img_dict
