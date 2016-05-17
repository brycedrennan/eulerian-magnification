import cv2

TEST_VIDEO_PATH = r"U:\Users\Bryce\Projects\python\eulerian-magnification\eulerian_source_videos\baby.mp4"
TEST_IMAGE_PATH = r"U:\Users\Bryce\Projects\python\eulerian-magnification\eulerian_source_videos\lenna.tiff"
DISPLAY_RESULTS = True


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
