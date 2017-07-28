import numpy as np

from eulerian_magnification.base import eulerian_magnification
from eulerian_magnification.io import play_video, play_vid_data, play_pyramid, load_video_float, load_image
from eulerian_magnification.pyramid import create_gaussian_image_pyramid, create_laplacian_image_pyramid, \
    create_gaussian_video_pyramid, create_laplacian_video_pyramid, collapse_laplacian_pyramid, \
    collapse_laplacian_video_pyramid
from .base import TEST_IMAGE_PATH, TEST_VIDEO_PATH, display_image, display_image_pyramid


def test_create_gaussian_image_pyramid():
    pyramid_depth = 3

    img = load_image(TEST_IMAGE_PATH)
    pyramid = create_gaussian_image_pyramid(img, pyramid_depth)
    display_image_pyramid(pyramid)

    means = [np.average(f) for f in pyramid]
    deviations = [np.std(f) for f in pyramid]

    assert len(pyramid) == pyramid_depth
    assert np.std(means) < 1
    assert np.std(deviations) < 1
    assert pyramid[0].shape == img.shape
    assert pyramid[1].shape[0] < pyramid[0].shape[0]
    assert pyramid[2].shape[0] < pyramid[1].shape[0]


def test_create_laplacian_image_pyramid():
    pyramid_depth = 3

    img = load_image(TEST_IMAGE_PATH)
    pyramid = create_laplacian_image_pyramid(img, pyramid_depth)
    display_image_pyramid(pyramid)

    # means = [np.average(f) for f in pyramid]
    deviations = [np.std(f) for f in pyramid]

    assert len(pyramid) == pyramid_depth
    assert np.std(deviations) > 0.01  # one of the images is just the original sized down photo. there should be significantly more variance in that photo
    assert pyramid[0].shape == img.shape
    assert pyramid[1].shape[0] < pyramid[0].shape[0]
    assert pyramid[2].shape[0] < pyramid[1].shape[0]


def test_play_video():
    play_video(TEST_VIDEO_PATH)


def test_create_gaussian_video():
    orig_vid, fps = load_video_float(TEST_VIDEO_PATH)
    pyramid = create_gaussian_video_pyramid(orig_vid, 3)
    play_pyramid(pyramid)


def test_laplacian_video():
    orig_vid, fps = load_video_float(TEST_VIDEO_PATH)
    pyramid = create_laplacian_video_pyramid(orig_vid, 3)
    play_pyramid(pyramid)
    recomposed_video = collapse_laplacian_video_pyramid(pyramid)
    assert (recomposed_video == orig_vid).all()


def test_collapse_laplacian_pyramid():
    img = load_image(TEST_IMAGE_PATH)
    pyramid = create_laplacian_image_pyramid(img, 5)
    display_image_pyramid(pyramid)
    img_collapsed = collapse_laplacian_pyramid(pyramid)
    display_image(img, "Original")
    display_image(img_collapsed, "Recomposed", wait=True)
    assert (img == img_collapsed).all()


def test_eulerian_magnification():
    # ('baby', 10, 16, 0.4, 3, 30),
    orig_vid, fps = load_video_float(TEST_VIDEO_PATH)
    enhanced_vid = eulerian_magnification(orig_vid, fps=30, freq_max=0.77, freq_min=0.4, amplification=30)
    play_vid_data(enhanced_vid)
