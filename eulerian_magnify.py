import cv2
import os

import cv
import numpy
import pylab
import scipy.signal
import scipy.fftpack


def eulerian_magnification(video_filename, freq_min=0.833, freq_max=1, amplification=50, gauss_level=4):
    """Amplify subtle variation in a video and save it to disk"""
    orig_vid, fps = load_video(video_filename)
    vid_data = gaussian_video(orig_vid, gauss_level)
    vid_data = temporal_bandpass_filter(vid_data, fps, freq_min=freq_min, freq_max=freq_max)
    print "Amplifying signal by factor of " + str(amplification)
    vid_data *= amplification
    file_name = os.path.splitext(video_filename)[0]
    combine_gaussian_and_save(vid_data, orig_vid, gauss_level, fps,
                              save_filename=file_name + '_magnified.avi')


def show_frequencies(video_filename, bounds=None):
    """Graph the average value of the video as well as the frequency strength"""
    original_video, fps = load_video(video_filename)
    print fps
    averages = []

    if bounds:
        for x in range(1, original_video.shape[0] - 1):
            averages.append(original_video[x, bounds[2]:bounds[3], bounds[0]:bounds[1], :].sum())
    else:
        for x in range(1, original_video.shape[0] - 1):
            averages.append(original_video[x, :, :, :].sum())

    charts_x = 1
    charts_y = 2
    pylab.figure(figsize=(charts_y, charts_x))
    pylab.subplots_adjust(hspace=.7)

    pylab.subplot(charts_y, charts_x, 1)
    pylab.title("Pixel Average")
    pylab.plot(averages)

    frequencies = scipy.fftpack.fftfreq(len(averages), d=1.0 / fps)

    pylab.subplot(charts_y, charts_x, 2)
    pylab.title("FFT")
    pylab.axis([0, 15, -2000000, 5000000])
    pylab.plot(frequencies, scipy.fftpack.fft(averages))

    pylab.show()


def temporal_bandpass_filter(data, fps, freq_min=0.833, freq_max=1, axis=0):
    print "Applying bandpass between " + str(freq_min) + " and " + str(freq_max) + " Hz"
    fft = scipy.fftpack.fft(data, axis=axis)
    frequencies = scipy.fftpack.fftfreq(data.shape[0], d=1.0 / fps)
    bound_low = (numpy.abs(frequencies - freq_min)).argmin()
    bound_high = (numpy.abs(frequencies - freq_max)).argmin()
    fft[:bound_low] = 0
    fft[bound_high:-bound_high] = 0
    fft[-bound_low:] = 0

    return scipy.fftpack.ifft(fft, axis=0)


def load_video(video_filename):
    """Load a video into a numpy array"""
    print "Loading " + video_filename
    # noinspection PyArgumentList
    capture = cv2.VideoCapture(video_filename)
    frame_count = int(capture.get(cv.CV_CAP_PROP_FRAME_COUNT))
    width, height = get_capture_dimensions(capture)
    fps = int(capture.get(cv.CV_CAP_PROP_FPS))
    x = 0
    orig_vid = numpy.zeros((frame_count, height, width, 3), dtype='uint8')
    while True:
        _, frame = capture.read()

        if frame == None or x >= frame_count:
            break
        orig_vid[x] = frame
        x += 1
    capture.release()

    return orig_vid, fps


def save_video(video, fps, save_filename='media/output.avi'):
    """Save a video to disk"""
    fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
    writer = cv2.VideoWriter(save_filename, fourcc, fps, (video.shape[2], video.shape[1]), 1)
    for x in range(0, video.shape[0]):
        res = cv2.convertScaleAbs(video[x])
        writer.write(res)


def gaussian_video(video, shrink_multiple):
    """Create a gaussian representation of a video"""
    vid_data = None
    for x in range(0, video.shape[0]):
        frame = video[x]
        gauss_copy = numpy.ndarray(shape=frame.shape, dtype="float")
        gauss_copy[:] = frame
        for i in range(shrink_multiple):
            gauss_copy = cv2.pyrDown(gauss_copy)

        if x == 0:
            vid_data = numpy.zeros((video.shape[0], gauss_copy.shape[0], gauss_copy.shape[1], 3))
        vid_data[x] = gauss_copy
    return vid_data


def combine_gaussian_and_save(g_video, orig_video, enlarge_multiple, fps, save_filename='media/output.avi'):
    """Combine a gaussian video representation with the original and save to file"""
    width, height = get_frame_dimensions(orig_video[0])
    fourcc = cv.CV_FOURCC('M', 'J', 'P', 'G')
    writer = cv2.VideoWriter(save_filename, fourcc, fps, (width, height), 1)
    for x in range(0, g_video.shape[0]):
        img = numpy.ndarray(shape=g_video[x].shape, dtype='float')
        img[:] = g_video[x]
        for i in range(enlarge_multiple):
            img = cv2.pyrUp(img)

        img[:height, :width] = img[:height, :width] + orig_video[x]
        res = cv2.convertScaleAbs(img[:height, :width])
        writer.write(res)


def get_capture_dimensions(capture):
    """Get the dimensions of a capture"""
    width = int(capture.get(cv.CV_CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
    return width, height


def get_frame_dimensions(frame):
    """Get the dimensions of a single frame"""
    height, width = frame.shape[:2]
    return width, height


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = scipy.signal.butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = scipy.signal.lfilter(b, a, data, axis=0)
    return y