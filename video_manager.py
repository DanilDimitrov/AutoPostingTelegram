import os


def create_video_from_photo():
    os.system("ffmpeg -r 1 -i out.png -vcodec mpeg4 -y output.mp4")