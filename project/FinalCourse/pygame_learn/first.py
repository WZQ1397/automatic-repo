import pygame
import sys

background_image = './images/background.jpg'
fish_image = './images/fish.png'

# 初始化pygame， 为使用硬件做准备
pygame.init()

size = width, height = 640, 480
# 创建一个窗口
screen = pygame.display.set_mode(size, 0, 32)

# 设置一个标题
pygame.display.set_caption('hello world')

# 加载并转换图像
background = pygame.image.load(background_image).convert()
fish = pygame.image.load(fish_image).convert_alpha()

font = pygame.font.SysFont('方正舒体', 64)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        screen.blit(background, (0,0))

        # 获取鼠标位置
        x, y = pygame.mouse.get_pos()

        x -= fish.get_width() / 2
        y -= fish.get_height() / 2

        # 把鱼画上去
        screen.blit(fish, (x,y))
        name_surface = font.render(u'徐金', True, (0,0,0), (255,255,255))
        name_surface1 = font.render('xujin', False, (0,0,0), (255,255,255))
        screen.blit(name_surface, (0,0))
        screen.blit(name_surface1, (200,0))

        pygame.display.update()