from eulerian_magnification.base import show_frequencies
from eulerian_magnification.io import _load_video, play_vid_data, load_image, load_video_float
from eulerian_magnification.transforms import uint8_to_float, float_to_uint8
from tests.base import DISPLAY_RESULTS

from .base import get_test_media_filepath, TEST_VIDEO_NAME, TEST_IMAGE_NAME


def test_uint8_to_float_and_back():
    img = load_image(get_test_media_filepath(TEST_IMAGE_NAME))
    img_float = uint8_to_float(img)
    img_uint8 = float_to_uint8(img_float)
    img_diff = img - img_uint8

    assert img_diff.max() <= 1


def test_uint8_to_float_and_back_for_video():
    vid_data, fps = _load_video(get_test_media_filepath(TEST_VIDEO_NAME))
    vid_float = uint8_to_float(vid_data)
    vid_unit8 = float_to_uint8(vid_float)
    vid_diff = vid_data - vid_unit8

    if DISPLAY_RESULTS:
        play_vid_data(vid_float)

    assert vid_diff.max() <= 1
    del vid_float


def test_fourier_transform_video():
    vid_data, fps = load_video_float(get_test_media_filepath(TEST_VIDEO_NAME))
    if DISPLAY_RESULTS:
        show_frequencies(vid_data, fps)
