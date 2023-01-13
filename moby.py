import io
from string import ascii_letters
from urllib.request import urlopen
import nltk.data
import random
from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client
import cv2
import numpy as np
from image_utils import ImageText
import os
import time
import constants
from animations import Animations
import cv2
from moviepy.editor import *
import requests
from colorthief import ColorThief

#constants
FONT_PATH = 'Bitter-ExtraBold.ttf'
OUTPUT_IMG_NAME = "img.png"
OUTPUT_REEL_NAME = "reel.mp4"
BACKGROUND_IMG = "background.jpg"
FILE_PATH = "moby-dick.txt"

def hilo(a, b, c):
    if c < b: b, c = c, b
    if b < a: a, b = b, a
    if c < b: b, c = c, b
    return a + c

def complement(r, g, b):
    k = hilo(r, g, b)
    return tuple(k - u for u in (r, g, b))

def getRandomSentence(txt_file):
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    fp = open(txt_file)
    data = fp.read()
    tok = tokenizer.tokenize(data); #breaks into sentences 
    newTok = random.choice([x for x in tok if len(x)<280])
    return newTok
   
def generateImage(txt, font_url, svImg):
    img = ImageText((600, 800), background=(colorPalettes[0][0], colorPalettes[0][1], colorPalettes[0][2], 200)) # 200 = alpha

    img.write_text_box((20, 10), txt, box_width=500, font_filename=font_url,
                   font_size=60, color=colorPalettes[int(len(colorPalettes) / 2)], place='center')
    
    img.save(svImg)

def uploadImage(imgpth, caption, username, password):
    cl = Client()
    cl.login(username, password)
    cl.photo_upload(
    imgpth,
    caption,
    extra_data={
        "custom_accessibility_caption": caption,
    })

def convert_avi_to_mp4(avi_file_path, output_name):
    os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
    return True

def createZoomedInVideo():
    start = time.time()
    size = constants.SIZE
    frame_rate = constants.FRAME_RATE
    anim = Animations()
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    images = ['background.jpg']
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter('zoomed.mp4', fourcc, 5, constants.SIZE)

    for iimgs, img_path in enumerate(images):
        img = cv2.imread(img_path)
        print(img_path)
        (h,w) = img.shape[:2]

        img = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=constants.WHITE)
        blur = anim.get_blur_img(img,size)

        for i in anim.img_animation_zoom_in(img, blur):
            out.write(i)

    out.release()

def overlayTextOnVideo():
    video = VideoFileClip("zoomed.mp4")
    title = ImageClip("img.png").set_start(0).set_duration(video.duration).set_pos(("center","center"))  
    audiofile = AudioFileClip("sounds/" + random.choice(os.listdir('sounds/'))) #change dir name to whatever
    print("Chose ", audiofile.filename)
    final = CompositeVideoClip([video, title])
    final.audio = audiofile
    final.write_videofile("reel.mp4")

def uploadReels(reelpth, caption, username, password):
    cl = Client()
    cl.login(username, password)
    cl.clip_upload(
    reelpth,
    "Image and post created by AI.\n" + caption +  " \n - excerpt from The Moby Dick by Herman Melville",
    extra_data={
        "custom_accessibility_caption": caption,
    })

def requestPicture(txt):
    r = requests.post(
    "https://api.deepai.org/api/text2img",
    data={
        'text': txt,
        'grid_size': 1,
    },
    headers={'api-key': ''})
    img_data = requests.get(r.json()['output_url']).content
    fd = urlopen(r.json()['output_url'])
    f = io.BytesIO(fd.read())
    color_thief = ColorThief(f)
    global colorPalettes 
    colorPalettes = color_thief.get_palette(quality=1)
    with open('background.jpg', 'wb') as handler:
        handler.write(img_data)


txt = getRandomSentence(FILE_PATH) 
requestPicture(txt)
generateImage(txt, FONT_PATH, OUTPUT_IMG_NAME)
createZoomedInVideo()
overlayTextOnVideo()
uploadReels("reel.mp4", txt, "", "")









