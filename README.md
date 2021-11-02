# Distort videos

[![Distorted video example](https://i.ibb.co/cXzQMHm/github-thumbnail.jpg)](https://www.youtube.com/watch?v=jM7Vzzkz8z0)

Applies a [Seam Carving](https://en.wikipedia.org/wiki/Seam_carving) algorithm (aka liquid rescale) on every frame of a video, and a vibrato effect on the audio to distort the video

*Inspired from [@DistordBot](https://www.twitter.com/DistortBot) on Twitter by [SergioSV96](https://github.com/SergioSV96)*

## Prerequisites :
* Python 3 :
  * [opencv-python](https://pypi.org/project/opencv-python/) (video)
  * [ffmpeg-python](https://pypi.org/project/ffmpeg-python/) (audio)
  * tkinter (file dialog)
  
  (Use `pip install -r requirements.txt`)

* [ImageMagick](https://imagemagick.org/script/index.php) (distortion algorithm)

## Usage :
Run `main.py` and choose a video, at the end you will find your distorted video in `/result/result_[name].mp4`

