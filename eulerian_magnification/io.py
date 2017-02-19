import os

import cv2
import numpy

from eulerian_magnification.transforms import uint8_to_float, float_to_uint8


def load_image(img_path):
    img = cv2.imread(img_path)
    return uint8_to_float(img)


def _load_video(video_filename):
    """Load a video into a numpy array"""
    print("Loading " + video_filename)
    if not os.path.isfile(video_filename):
        raise Exception("File Not Found: %s" % video_filename)
    # noinspection PyArgumentList
    capture = cv2.VideoCapture(video_filename)
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    width, height = get_capture_dimensions(capture)
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    x = 0
    vid_frames = numpy.zeros((frame_count, height, width, 3), dtype='uint8')
    while capture.isOpened():
        ret, frame = capture.read()
        if not ret:
            break

        vid_frames[x] = frame
        x += 1
    capture.release()

    return vid_frames, fps


def load_video_float(video_filename):
    vid_data, fps = _load_video(video_filename)
    return uint8_to_float(vid_data), fps


def get_capture_dimensions(capture):
    """Get the dimensions of a capture"""
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return width, height


def play_video(video_filename):
    orig_vid, fps = load_video_float(video_filename)
    play_vid_data(orig_vid)


def play_pyramid(pyramid):
    i = 0
    while True:
        try:
            for level, vid in enumerate(pyramid):
                cv2.imshow('Level %i' % level, vid[i])
            i += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except IndexError:
            break


def play_vid_data(frames):
    play_pyramid([frames])


def save_video(video, fps, save_filename='media/output.avi'):
    """Save a video to disk"""
    # fourcc = cv2.CAP_PROP_FOURCC('M', 'J', 'P', 'G')
    print(save_filename)
    video = float_to_uint8(video)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    writer = cv2.VideoWriter(save_filename, fourcc, fps, (video.shape[2], video.shape[1]), 1)
    for x in range(0, video.shape[0]):
        res = cv2.convertScaleAbs(video[x])
        writer.write(res)
