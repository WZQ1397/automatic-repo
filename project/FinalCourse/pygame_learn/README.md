# Pygame 模块使用

### pygame 的模块
|模块名|功能|
|:---:|:---:|
|pygame.cdrom|访问光驱|
|pygame.cursors|加载光标|
|pygame.display|访问显示设备|
|pygame.draw|绘制形状，线，点|
|pygame.event|管理事件|
|pygame.font|使用字体|
|pygame.image|加载和存储图片|
|pygame.joystick|使用游戏手柄或者类似的东西|
|pygame.key|读取键盘按钮|
|pygame.mixer|声音|
|pygame.mouse|鼠标|
|pygame.movie|播放视频|
|pygame.music|播放音频|
|pygame.overlay|访问高级视频叠加|
|pygame.rect|管理矩形区域|
|pygame.sndarray|操作声音数据|
|pygame.sprite|操作移动图像|
|pygame.surface|管理点阵图像数据|
|pygame.time|管理时间和帧信息|
|pygame.transform|缩放和移动图像|

有些模块在某些平台不存在，我们可以使用None来测试一下
```python
import pygame
if pygame.font is None:
    print('the font not available')
    exit(0)
```

### 事件
pygame.event.get()来处理所有的事件，这好像打开大门让所有的人进入。如果我们使用pygame.event.wait()，Pygame就会等到发生一个事件才继续下去，就好像你在门的猫眼上盯着外面一样，来一个放一个……一般游戏中不太实用，因为游戏往往是需要动态运作的；而另外一个方法pygame.event.poll()就好一些，一旦调用，它会根据现在的情形返回一个真实的事件，或者一个“什么都没有”。下表是一个常用事件集：

|事件|产生途径|参数|
|:---:|:---|:---:|
|QUIT|用户点击关闭按钮|None|
|ATIVEEVENT|Pygame被激活或被隐藏|gain,state|
|KEYDOWN|键盘被按下|unicode,key,mod|
|KEYUP|键盘被放开|key,mod|
|MOUSEMOTION|鼠标移动|pos,rel,buttons|
|MOUSEBUTTONDOWN|鼠标按下|pos,button|
|MOUSEBUTTONUP|鼠标放开|pos,button|
|JOYAXISMOTION|游戏手柄移动|joy,axis,value|
|JOYBALLMOTION|游戏球移动？|joy,axis,value|
|JOYHATMOTION|游戏手柄移动？|joy,axis,value|
|JOYBUTTONDOWN|游戏手柄按下|joy,button|
|JOYBUTTONUP|游戏手柄放开|joy,button|
|VIDEORESIZE|Pygame窗口缩放|size,w,h|
|VIDEOEXPOSE|Pygame窗口部分公开|none|
|USEREVENT|触发了一个用户事件|code|


