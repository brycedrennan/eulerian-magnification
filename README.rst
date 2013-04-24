Eulerian Video Magnification v0.1
=================================

A tool to discover hidden variation in video.  This is based on the amazing research done at MIT:
http://people.csail.mit.edu/mrub/vidmag/

Requirements
------------

  - Python 2.7
  - OpenCV, numpy, scipy, pylab

How to Use
-----------

This technique works best with videos that have very little motion. Pre-processing a video through a stabilization
algorithm may help.  Some excellent videos sources can be found here: http://people.csail.mit.edu/mrub/vidmag/

Once you've downloaded the video simply run::

    eulerian_magnification('face.mp4', freq_min=50.0/60.0, freq_max=1.0, amplification=50)

freq_min and freq_max specify the frequency in hertz that will be amplified. amplification specifies how much that
signal will be amplified.

It can take a while to find the best parameters for a specific video. To help with that there is the show_frequencies
function::

   show_frequencies('media/face.mp4')

This will show a graph of the average value of the video as well as a graph of the signal strength at various
frequencies.


TODO
------------

Pull requests welcome!

 - Laplacian Pyramid motion amplification
 - Butterworth and IIR filters
 - Optimized memory usage to allow processing of larger files

Troubleshooting
---------------

On my system it was neccesary to add C:\OpenCV2.3\build\x86\vc10\bin to the system path before videos would load
properly.  Until then they would load as zero-length videos.

Author
------

Bryce Drennan <eulerian-magnify@brycedrennan.com>