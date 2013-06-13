Eulerian Video Magnification v0.1
=================================

A tool to discover hidden variation in video.  This is based on the amazing research done at MIT:
http://people.csail.mit.edu/mrub/vidmag/

Requirements
------------

  - Python 2.7
  - OpenCV, numpy, scipy, pylab

On a windows machine make sure you install the 32-bit version of everything. You can download the needed libraries
here http://www.lfd.uci.edu/~gohlke/pythonlibs/ Make sure you install the MKL version of numpy as the scipy binary
depends on it.

How to Use
-----------

This technique works best with videos that have very little motion. Pre-processing a video through a stabilization
algorithm may help.  Some excellent videos sources can be found here: http://people.csail.mit.edu/mrub/vidmag/

Once you've downloaded the video simply run::

    eulerian_magnification('media/face.mp4', image_processing='gaussian', pyramid_levels=3, freq_min=50.0 / 60.0, freq_max=1.0, amplification=50)

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

 - Butterworth and IIR filters
 - Optimized memory usage to allow processing of larger files

Troubleshooting
---------------

**When I process the video it looks all weird - alternating from bright to dark - what am I doing wrong?**

Most likely the video you're trying to process just has too much movement. Try running it through a video stabilizer.
Even with stabilization, it can be hard to find the correct frequency and amplification parameters that isolate the
hidden motion you're trying to display.

Additionally, some videos are better suited to motion amplification using a laplacian pyramid.

**Windows: IndexError: tuple index out of range**

On windows it may be neccesary to add *C:\\OpenCV2.3\\build\\x86\\vc10\\bin* to the system path for videos to load
properly.  Make sure you adjust the path to the actual location of your opencv library.

Author
------

Bryce Drennan <eulerian-magnify@brycedrennan.com>
