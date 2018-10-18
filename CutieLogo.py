from PIL import Image, ImageDraw, ImageFont, ImageTk
import random
from random import randint
import numpy as np
import os.path
import sys
import importlib

def get_img_dir() -> str:
    pkg_dir = os.path.dirname(__file__)
    return pkg_dir

class CutieLogo:
  def __init__(self, shape, rC, gC, bC, nameColor):
    self.shape = shape
    self.rC = rC
    self.gC = gC
    self.bC = bC
    self.nameColor = nameColor

  def logo(self, shape, rC, gC, bC, nameColor, text, Tfont, k):
    #convert shape color
    im = Image.open(shape)
    pixels = list(im.getdata())

    pixels = [(int((255-pixel[0]) * rC), int((255-pixel[1]) * gC), int((255-pixel[2]) * bC)) for pixel in pixels]
    im.putdata(pixels)
    im2 = im
    
    #create logo
    l = Image.new('RGB', (500,400), color = (255,255,255))
    w, h = l.size
    file_name = str(k).zfill(4)
    path = os.path.join(get_img_dir(),'static','img', 'Cutie Logos',file_name + ".png")
    l.save(path)

    
    #add shape
    lg = Image.open(path)
    cl = ImageDraw.Draw(lg)
    lg.paste(im2,(0,0,500,400))
    
    #add brand
    clogo = Image.open('cutie.png')
    lg.paste(clogo,(0,0))

    #add text
    f = ImageFont.truetype(Tfont,size=90)
    text_w, text_h = cl.textsize(text,f)
    cl.text(((w-text_w)/2,(h-text_h)/2), text, fill=nameColor, font=f, align="center")

    #save file
    lg.save(path)

      

shapeList = ['Shapes/1.png', 'Shapes/2.png','Shapes/3.png','Shapes/4.png','Shapes/5.png']
textList = ["Soft", "Compact", "Budget"]

def cutie_logo_maker(n):
  k = 1
  while k<=n:#number of copies + 1
    R= random.uniform(0,1)
    G = random.uniform(0,1)
    B = random.uniform(0,1)
    rValueF = randint(100,255)
    gValueF = randint(100,255)
    bValueF = randint(100,255)
    random.shuffle(shapeList)
    random.shuffle(textList)
    
    LOGO = CutieLogo(shapeList[0],R,G,B,(rValueF,gValueF,bValueF))
    LOGO.logo(shapeList[0],R,G,B,(rValueF,gValueF,bValueF),textList[0],'Font/Lucida.ttf',k)
    k = k + 1
            


