# Eulerian Video Magnification

Amplify tiny movements in video.

Based on the amazing research done at MIT:
http://people.csail.mit.edu/mrub/vidmag/

## Installation
  - Install OpenCV
  - `pip install eulerian-magnification`
  
  or
  
    docker build -t eulerian -t
    docker run -it eulerian /bin/bash

## Requirements
  - Python 3.5, untested on Python 2.7.
  - OpenCV 3+.
  - numpy, scipy, matplotlib

On windows you can download the needed python dependencies [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/). Make sure you install the MKL
version of numpy as the scipy binary depends on it.

## Usage

This technique works best with videos that have very little motion. Pre-processing a video through a stabilization
algorithm may help.  Some excellent videos sources can be found here: http://people.csail.mit.edu/mrub/vidmag/

Once you've downloaded the video simply run::

    import eulerian_magnification as em

    vid, fps = em.load_video_float(source_path)
    em.eulerian_magnification(vid, fps, 
            freq_min=50.0 / 60.0,
            freq_max=1.0,
            amplification=50,
            pyramid_levels=3
    )


`freq_min` and `freq_max` specify the frequency in hertz that will be amplified. `amplification` specifies how much that signal will be amplified.

It can take a while to find the best parameters for a specific video. To help with that there is the show_frequencies
function::


    import eulerian_magnification as em
    
    vid, fps = em.load_video_float(source_path)
    em.show_frequencies(vid, fps)


This will show a graph of the average value of the video as well as a graph of the signal strength at various
frequencies.

## Todo
 - Butterworth and IIR filters
 - Optimized memory usage to allow processing of larger files

## Troubleshooting


**When I process the video it looks all weird - alternating from bright to dark - what am I doing wrong?**

Most likely the video you're trying to process just has too much movement. Try running it through a video stabilizer.
Even with stabilization, it can be hard to find the correct frequency and amplification parameters that isolate the
hidden motion you're trying to display.

Additionally, some videos are better suited to motion amplification using a laplacian pyramid.

**Windows: IndexError: tuple index out of range**

On windows with OpenCv2 it may be necessary to add *C:\\OpenCV2.3\\build\\x86\\vc10\\bin* to the system path for videos to load
properly.  Make sure you adjust the path to the actual location of your opencv library.

## Push to Pypi

    git tag 0.22
    git push --tags
    python setup.py sdist
    twine upload dist/*
    rm dist -r


## Author

Bryce Drennan <eulerian-magnify@brycedrennan.com>
