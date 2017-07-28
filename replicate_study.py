import os
import requests
import eulerian_magnification as em

# # show_frequencies('media/face.mp4')
# # eulerian_magnification('media/face.mp4', image_processing='gaussian', pyramid_levels=3, freq_min=50.0 / 60.0, freq_max=1.0, amplification=50)
#
#
# em.show_frequencies('media/baby.mp4')
# # em.eulerian_magnification('media/baby.mp4', image_processing='gaussian', pyramid_levels=2, freq_min=0.45, freq_max=1, amplification=190)
# em.eulerian_magnification('media/baby.mp4', image_processing='gaussian', pyramid_levels=2, freq_min=7.2, freq_max=7.6,
#                           amplification=190)
#
# # em.show_frequencies('media/wrist_magnified.avi')

# http://people.csail.mit.edu/mrub/papers/vidmag.pdf
from eulerian_magnification.io import save_video, load_video_float

PAPER_REPLICATION_VALUES = [
    # name, amplification_factor, cutoff, lower_hertz, upper_hertz, framerate
    ('baby', 10, 16, 0.4, 3, 30),
    ('baby', 10, 16, 0.4, 0.8, 30),
    ('baby2', 150, 600, 2.33, 2.67, 30),
    ('camera', 120, 20, 45, 100, 300),
    ('face', 100, 1000, 0.83, 1, 30),
    # ('face2', 20, 80, 0.83, 1, 30),  # motion
    # ('face2', 120, 960, 0.83, 1, 30),  # pulse
    ('guitar', 50, 40, 72, 92, 600),  # low E
    ('shadow', 5, 48, 0.5, 10, 30),
    ('subway', 60, 90, 3.6, 6.2, 30),
    ('wrist', 10, 80, 0.4, 3, 30),
]
SOURCE_VIDEOS_DIR = 'eulerian_source_videos'


def download_videos(dest_dir=SOURCE_VIDEOS_DIR):
    for vid_data in PAPER_REPLICATION_VALUES:
        name = vid_data[0]
        source_filename = name + '.mp4'
        os.makedirs(dest_dir, exist_ok=True)
        dest_filename = os.path.join(dest_dir, source_filename)
        download_file('http://people.csail.mit.edu/mrub/evm/video/' + source_filename, dest_filename)


def download_file(url, dest):
    if os.path.isfile(dest):
        print('Already Downloaded: %s to %s' % (url, dest))
        return
    print('Downloading: %s to %s' % (url, dest))

    response = requests.get(url, stream=True)
    if not response.ok:
        raise Exception("Couldn't download file")

    with open(dest, 'wb') as fp:
        for block in response.iter_content(1024):
            fp.write(block)


def replicate_study():
    download_videos()
    image_processing = 'laplacian'
    pyramid_levels = 4

    for name, amplification_factor, cutoff, lower_hertz, upper_hertz, framerate in PAPER_REPLICATION_VALUES:
        source_filename = name + '.mp4'

        source_path = os.path.join(SOURCE_VIDEOS_DIR, source_filename)
        vid, fps = load_video_float(source_path)
        vid = em.eulerian_magnification(
            vid, fps,
            freq_min=lower_hertz,
            freq_max=upper_hertz,
            amplification=amplification_factor,
            pyramid_levels=pyramid_levels
        )
        file_name = os.path.splitext(source_path)[0]
        file_name = file_name + "__" + image_processing + "_levels" + str(pyramid_levels) + "_min" + str(
            lower_hertz) + "_max" + str(upper_hertz) + "_amp" + str(amplification_factor)
        save_video(vid, fps, file_name + '.avi')


if __name__ == '__main__':
    replicate_study()
