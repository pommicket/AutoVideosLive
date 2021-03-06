# AutoVideosLive
AutoVideos that play live using OpenCL.

AutoVideos, AutoImages, and AutoAudio can be found [here](https://github.com/pommicket/AutoArtGPU).

AutoVideosLive uses your GPU to create AutoVideos very quickly and play them as they are being created.

**AutoVideosLive requires the following dependencies:**  
+ Python
+ PyOpenCL
+ numpy
+ PIL

On Debian/Ubuntu, the libraries can be installed using:  
```
sudo apt-get install python python-pyopencl python-numpy python-pil
```

Or you can use [pip](https://pip.pypa.io/en/stable/) to install them.

AutoVideos is a computer program that generates images by using Markov Chains to generate random functions so that the colour of each pixel is dependent on its x and y position and time during the video.

