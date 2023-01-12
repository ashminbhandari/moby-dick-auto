from string import ascii_letters
import textwrap
import nltk.data
import random
from PIL import Image, ImageDraw, ImageFont
from instagrapi import Client

FONT_URL = 'Bitter-ExtraBold.ttf'

API_KEY = "b1313aaf-4bb1-4c55-98dc-e0c326cf2b63"

IMG_NAME = "img.jpg"

def getRandomSentence(txt_file):

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    fp = open(txt_file)

    data = fp.read()

    tok = tokenizer.tokenize(data); #breaks into sentences 

    newTok = random.choice([x for x in tok if len(x)<280])

    return newTok
    
def generageImage(txt, font_url):
    img = Image.open(fp='background.jpg', mode='r')
    
    font = ImageFont.truetype(font=font_url, size=55)
    
    draw = ImageDraw.Draw(im=img)

    avg_char_width = sum(font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)

    max_char_count = int(img.size[0] * .900 / avg_char_width)
    
    text = textwrap.fill(text=txt, width=max_char_count)

    bbox = draw.textbbox((img.size[0]/5, img.size[1]/3.5), text, font=font)
    draw.rectangle(bbox, fill="#F0E0C0")
    draw.text((img.size[0]/5, img.size[1]/3.5), text, font=font, fill="#3B3A28")
    img.show()
    img.save(IMG_NAME)

def uploadImage(imgpth, caption):
    cl = Client()
    cl.login(USERNAME, PASSWORD)
    cl.photo_upload(
    imgpth,
    caption,
    extra_data={
        "custom_accessibility_caption": caption,
    }
)


txt = getRandomSentence('moby-dick.txt')
generageImage(txt, FONT_URL)
uploadImage(IMG_NAME, txt)



