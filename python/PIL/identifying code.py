from PIL import Image, ImageFilter,ImageDraw,ImageFont
import random
# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))

# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

def randPoint():
    (width, height) = image.size
    return (random.randint(0, width), random.randint(0, height))

# 180 x 60:
CHAR_NUMS = 6
SINGLE_CHAR_SIZE = 30
width = SINGLE_CHAR_SIZE * CHAR_NUMS
height = 60

image = Image.new('RGB', (width, height), (255, 255, 255))
# 创建Font对象:
fontpath = 'C:\\Windows\winsxs\\amd64_microsoft-windows-font-truetype-arial_31bf3856ad364e35_6.1.7601.17514_none_d0a9759ec3fa9e2d\\arial.ttf'
font = ImageFont.truetype(fontpath, 36)
# 创建Draw对象:
draw = ImageDraw.Draw(image)
# 填充每个像素:
for x in range(width):
    for y in range(height):
        draw.point((x, y), fill=rndColor())
# 输出文字:

for t in range(CHAR_NUMS):
    draw.text((SINGLE_CHAR_SIZE * t + 10, 10), rndChar(), font=font, fill=rndColor2())
# LINE
for x in range(5):
    draw.line([randPoint(), randPoint()],fill=random.randint(0,255))

# 模糊:
image = image.filter(ImageFilter.BLUR)

image.save('code.jpg', 'jpeg')