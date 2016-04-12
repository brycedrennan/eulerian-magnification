from eularian_magnification.base import eulerian_magnification, show_frequencies

# show_frequencies('media/face.mp4')
eulerian_magnification('media/face.mp4', image_processing='gaussian', pyramid_levels=3, freq_min=50.0 / 60.0, freq_max=1.0, amplification=50)


#show_frequencies('media/baby.mp4')
#eulerian_magnification('media/baby.mp4', image_processing='laplacian', pyramid_levels=5, freq_min=0.45, freq_max=1, amplification=50)
