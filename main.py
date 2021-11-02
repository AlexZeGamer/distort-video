import os, sys, subprocess
from tkinter import Tk, filedialog as fd
import cv2
import ffmpeg
Tk().withdraw() # makes the tkinter window not show up

# tests if ImageMagick is installed
if subprocess.getstatusoutput('magick')[0] != 0:
    raise EnvironmentError('\033[91m' + 'ImageMagick is not installed (https://imagemagick.org/script/download.php)' + '\033[0m')

DISTORT_PERCENTAGE = 60 #default: 60
SOUND_FILTER_FREQUENCY = 10 #default: 10
SOUND_FILTER_MODULATION_DEPTH = 1 #default: 1


# define paths
path = os.path.abspath(os.path.join(sys.argv[0], os.pardir))
resultDirPath = os.path.join(path, 'result')

filetypes = [('video', '*.mp4 *.avi *.mov *.wmv *.flv')]
videoPath = fd.askopenfilename(filetypes=filetypes) # choose input video
print(videoPath)
if videoPath == '': #canceled
    exit()

videoName = os.path.basename(videoPath)
framesPath = os.path.join(resultDirPath, 'frames')
distortedFramesPath = os.path.join(resultDirPath, 'distortedFrames')

# define video variables
capture = cv2.VideoCapture(videoPath)
fps = capture.get(cv2.CAP_PROP_FPS)
nbFrames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
videoSize = (
    int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
)


# create output directories
os.makedirs(resultDirPath, exist_ok=True)
os.makedirs(framesPath, exist_ok=True)
os.makedirs(distortedFramesPath, exist_ok=True)
for elem in os.listdir(framesPath):
    os.remove( os.path.join(framesPath, elem) )
for elem in os.listdir(distortedFramesPath):
    os.remove( os.path.join(distortedFramesPath, elem) )


# convert video to frames
print('Converting video into frames...')
frameNr = 0
while True:
    print(f'{frameNr}/{nbFrames}', end='\r')
    success, frame = capture.read()

    if not success:
        break

    # naming the file with an appropriate number of leading zeros
    filename = f'frame_{str(frameNr).zfill(len(str(nbFrames)))}.jpg'
    cv2.imwrite(os.path.join(framesPath, filename), frame)
    frameNr += 1
capture.release()


# distortion of frames
print('Distorting frames...')
for i, elem in enumerate(os.listdir(framesPath), start=1):
    print(f'{i}/{nbFrames}', end="\r")
    curFramePath = os.path.join(framesPath, elem)
    resFramePath = os.path.join(distortedFramesPath, elem)
    cmd = f"magick {curFramePath}\
        -liquid-rescale {100-DISTORT_PERCENTAGE}x{100-DISTORT_PERCENTAGE}%!\
        -resize {videoSize[0]}x{videoSize[1]}\! {resFramePath}"
    exitCode, cmdOutput = subprocess.getstatusoutput(cmd)

    if exitCode != 0:
        raise os.error( '\033[91m' + f'Error while distorting frame {i}/{nbFrames}:' + '\n'
                        + cmdOutput + '\033[0m')


# Assembling frames back into a video
print('Creating video...')
img_array = [cv2.imread(os.path.join(distortedFramesPath, elem)) for elem in sorted(os.listdir(distortedFramesPath))]
distortedVideoPath = os.path.join(resultDirPath, 'distorted_'+videoName)
out = cv2.VideoWriter(distortedVideoPath, cv2.VideoWriter_fourcc(*'mp4v'), fps, videoSize)

for i in range(len(img_array)):
    print(f'{i}/{nbFrames}', end="\r")
    out.write(img_array[i])
out.release()


# add distorted sound
print("Adding distorted sound...")
video = ffmpeg.input(distortedVideoPath).video
audio = ffmpeg.input(videoPath).audio.filter(
    "vibrato",
    f=SOUND_FILTER_FREQUENCY,
    d=SOUND_FILTER_MODULATION_DEPTH
    # Documentation : https://ffmpeg.org/ffmpeg-filters.html#vibrato
)
resultVideoPath = os.path.join(resultDirPath, 'result_'+videoName)
(
    ffmpeg
    .concat(video, audio, v=1, a=1) # v = video stream, a = audio stream
    .output(resultVideoPath)
    .run(overwrite_output=True)
    # Documentation : https://kkroening.github.io/ffmpeg-python/
)

# delete the distorted video with no sound
os.remove(distortedVideoPath)


print('\033[92m' + "--- DONE ! ---" + '\033[0m')