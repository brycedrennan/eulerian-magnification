from eulerian_magnify import eulerian_magnification, show_frequencies


show_frequencies('media/face.mp4')
eulerian_magnification('media/face.mp4', gauss_level=3, freq_min=50.0/60.0, freq_max=1.0, amplification=50)

#show_frequencies('media/baby.mp4')
#eulerian_magnification('media/baby.mp4', gauss_level=4, freq_min=0.45, freq_max=0.55, amplification=50)