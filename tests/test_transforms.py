from eulerian_magnification.base import show_frequencies
from eulerian_magnification.io import _load_video, play_vid_data, load_image, load_video_float
from eulerian_magnification.transforms import uint8_to_float, float_to_uint8
from .base import TEST_IMAGE_PATH, TEST_VIDEO_PATH


def test_uint8_to_float_and_back():
    img = load_image(TEST_IMAGE_PATH)
    img_float = uint8_to_float(img)
    img_uint8 = float_to_uint8(img_float)
    img_diff = img - img_uint8

    assert img_diff.max() <= 1


def test_uint8_to_float_and_back_for_video():
    vid_data, fps = _load_video(TEST_VIDEO_PATH)
    vid_float = uint8_to_float(vid_data)
    vid_unit8 = float_to_uint8(vid_float)
    vid_diff = vid_data - vid_unit8

    play_vid_data(vid_float)

    assert vid_diff.max() <= 1


def test_fourier_transform_video():
    vid_data, fps = load_video_float(TEST_VIDEO_PATH)
    show_frequencies(vid_data, fps)
