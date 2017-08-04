# -*- coding: utf-8 -*-
from PIL import Image,ImageDraw,ImageFont
import random

class RandomChar():
    s="fsdgfdgdbhfdhfhdhdfsdfhd"
    def createchar(self):
        return random.sample(self.s,1)[0]


class ImageChar:
  def __init__(self, fontColor = (0, 0, 0),
                     size = (100, 40),
                     fontPath = 'C:\\Windows\winsxs\\amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_6.1.7601.17514_none_d0a9759ec3fa9e2d\\arial.ttf',
                     bgColor = (255, 255, 255),
                     fontSize = 20):
    self.size = size
    self.fontPath = fontPath
    self.bgColor = bgColor
    self.fontSize = fontSize
    self.fontColor = fontColor
    self.font = ImageFont.truetype(self.fontPath, self.fontSize)
    self.image = Image.new('RGB', size, bgColor)

  def rotate(self):
    self.image.rotate(random.randint(0, 30), expand=0)

  def drawText(self, pos, txt, fill):
    draw = ImageDraw.Draw(self.image)
    draw.text(pos, txt, font=self.font, fill=fill)

  def randRGB(self):
    return (random.randint(0, 255),
           random.randint(0, 255),
           random.randint(0, 255))

  def randPoint(self):
    (width, height) = self.size
    return (random.randint(0, width), random.randint(0, height))

  def randLine(self, num):
    draw = ImageDraw.Draw(self.image)
    for i in range(0, num):
      draw.line([self.randPoint(), self.randPoint()], self.randRGB())

  def randChinese(self, num):
    gap = 5
    start = 0
    for i in range(0, num):
      char = RandomChar().createchar()
      x = start + self.fontSize * i + random.randint(0, gap) + gap * i
      self.drawText((x, random.randint(-5, 5)), char, self.randRGB())
      self.rotate()
    self.randLine(18)

  def save(self, path):
    self.image.rotate(45)
    self.image.save(path)

ic = ImageChar(fontColor=(100,211,90))
#FIXME CHINESE UNSPPORT!
ic.randChinese(4)
ic.save("1.jpeg")
