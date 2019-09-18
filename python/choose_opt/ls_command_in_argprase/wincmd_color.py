import ctypes
import sys
from configparser import ConfigParser
# ini config reader
config = ConfigParser()
config.read('color.ini')
STD_OUTPUT_HANDLE = int(config.get("Win_STD","STD_OUTPUT_HANDLE"))

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

# reset white
def resetColor():
    set_cmd_text_color(0x09 | 0x0a| 0x0c)
###############################################################

class PrintColor:
    def __init__(self,mess):
        self.mess=mess

    def print(self):
        sys.stdout.write(self.mess)
        resetColor()

class FOREGROUND_DARK_BLUE(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
         #SetCmdColor(FOREGROUND_DARK_BLUE).set_cmd_text_color()
         set_cmd_text_color(int(config.get("Win_FOREGROUND", self.__class__.__name__), 16))
         self.print()

class FOREGROUND_DARK_GREEN(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
        set_cmd_text_color(int(config.get("Win_FOREGROUND",self.__class__.__name__),16))
        self.print()

class FOREGROUND_DARK_SKYBLUE(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
        set_cmd_text_color(int(config.get("Win_FOREGROUND", self.__class__.__name__), 16))
        self.print()

class FOREGROUND_BOLDBLACK(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
        set_cmd_text_color(int(config.get("Win_FOREGROUND", self.__class__.__name__), 16))
        self.print()

class FOREGROUND_YELLOW(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
        set_cmd_text_color(int(config.get("Win_FOREGROUND", self.__class__.__name__), 16))
        self.print()

class FOREGROUND_RED(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
        set_cmd_text_color(int(config.get("Win_FOREGROUND", self.__class__.__name__), 16))
        self.print()

class YellowBlue(PrintColor):
    def __init__(self,mess):
        super().__init__(mess)

    def __call__(self):
        set_cmd_text_color(int(config.get("Win_FOREGROUND", 'FOREGROUND_YELLOW'), 16) | int(config.get("Win_BACKGROUND", 'BACKGROUND_DARK_BLUE'), 16))
        self.print()
##################################################

if __name__ == '__main__':
    FOREGROUND_DARK_BLUE('printDarkBlue:暗蓝色文字\n')()
    FOREGROUND_DARK_GREEN('printDarkGreen:暗绿色文字\n')()
#     printDarkSkyBlue('printDarkSkyBlue:暗天蓝色文字\n')
#     printDarkRed('printDarkRed:暗红色文字\n')
#     printDarkPink('printDarkPink:暗粉红色文字\n')
#     printDarkYellow('printDarkYellow:暗黄色文字\n')
#     printDarkWhite('printDarkWhite:暗白色文字\n')
#     printDarkGray('printDarkGray:暗灰色文字\n')
#     printBlue('printBlue:蓝色文字\n')
#     printGreen('printGreen:绿色文字\n')
#     printSkyBlue('printSkyBlue:天蓝色文字\n')
#     printRed('printRed:红色文字\n')
#     printPink('printPink:粉红色文字\n')
#     printYellow('printYellow:黄色文字\n')
#     printWhite('printWhite:白色文字\n')
#
#     printWhiteBlack('printWhiteBlack:白底黑字输出\n')
#     printWhiteBlack_2('printWhiteBlack_2:白底黑字输出（直接传入16进制参数）\n')
#     printYellowRed('printYellowRed:黄底红字输出\n')