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

    eulerian_magnification('face.mp4', gauss_level=4, freq_min=50.0/60.0, freq_max=1.0, amplification=50)


TODO
------------

Pull requests welcome!

 - Laplacian Pyramid motion amplification
 - Butterworth and IIR filters
 - Optimized memory usage to allow processing of larger files


Author
------

Bryce Drennan <eulerian-magnify@brycedrennan.com>