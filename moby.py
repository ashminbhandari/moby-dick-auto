import nltk.data
import random
import requests
from PIL import Image, ImageDraw, ImageFont

API_KEY = "b1313aaf-4bb1-4c55-98dc-e0c326cf2b63"

def getRandomSentence(txt_file):

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    fp = open(txt_file)

    data = fp.read()

    tok = tokenizer.tokenize(data); #breaks into sentences 

    newTok = random.choice([x for x in tok if len(x)<280])

    return newTok

def generateImage(txt, file_name):
    # Create a new image with a white background
    image = Image.new('RGB', (200, 100), (255, 255, 255))

    # Create a draw object to draw on the image
    draw = ImageDraw.Draw(image)
 
    # Load the default font, and specify the font size
    font = ImageFont.load_default()

    # Draw the text on the image
    draw.text((10, 10), txt, font=font, fill=(0, 0, 0))

    # Save the image to a file
    image.save(file_name)

prompt = getRandomSentence('moby-dick.txt')
generateImage(prompt, 'image.png')


