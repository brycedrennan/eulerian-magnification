from eulerian_magnify import eulerian_magnification, show_frequencies


#eulerian_magnification('media/bryce.avi', gauss_level=3, freq_min=1.1, freq_max=1.3, amplification=50)
#eulerian_magnification('media/bryce3.MOV', gauss_level=3, freq_min=1.1, freq_max=1.3, amplification=75)
#eulerian_magnification('media/babysleeping_source.wmv', gauss_level=4, freq_min=0.4, freq_max=0.55, amplification=75)
eulerian_magnification('media/face.mp4', gauss_level=3, freq_min=50.0/60.0, freq_max=1.0, amplification=50)

#show_frequencies('media/skin.avi',bounds=[340,340+134,300,600])
#show_frequencies('media/babysleeping_source.wmv')
#eulerian_magnification('media/skin.avi', gauss_level=3, freq_min=1.0, freq_max=1.2, amplification=85)
#eulerian_magnification('media/oldspice_fabio.avi', gauss_level=3, freq_min=1.0, freq_max=1.2, amplification=85)