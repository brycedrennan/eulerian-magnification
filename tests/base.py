import hashlib
import os
import tempfile
from pathlib import Path

import cv2
import requests

TEST_DATA_PATH = Path(tempfile.gettempdir()) / Path('eulerian-magnification')
TEST_DATA_URL = "https://s3-us-west-1.amazonaws.com/eulerian-magnify/"
TEST_VIDEO_NAME = "baby.mp4"
TEST_IMAGE_NAME = "lena.tiff"
DISPLAY_RESULTS = False


def display_image(image, title='Image', wait=False):
    if DISPLAY_RESULTS:
        cv2.imshow(title, image)
        if wait:
            cv2.waitKey(0)


def display_image_pyramid(pyramid):
    if DISPLAY_RESULTS:
        for i, img in enumerate(pyramid):
            cv2.imshow(str(i), pyramid[i])
        cv2.waitKey(0)


def get_test_media_filepath(filename):
    return get_local_path_for_remote_resouce(f"{TEST_DATA_URL}{filename}")


def get_local_path_for_remote_resouce(url, data_path=TEST_DATA_PATH):
    url_hash = hashlib.md5(url.encode('utf8')).hexdigest()
    downloaded_path = data_path / Path(url_hash + '.txt')
    if not downloaded_path.exists():
        download_file(url, downloaded_path)
    return downloaded_path


def download_file(url, dest_path):
    os.makedirs(str(dest_path.parent), exist_ok=True)
    with dest_path.open('wb') as f:
        response = requests.get(url, stream=True)
        if not response.ok:
            raise Exception('Download Failed')

        for block in response.iter_content(1024):
            f.write(block)
