# _*_ coding: utf-8 _*_
# HOW TO --> “python pyTOexe.py py2exe”
# OR OTHER TOOL -- pyinstaller
# python pyinstaller.py -w --onefile --icon="my.ico" test.py
import py2exe
from distutils.core import setup
includes = ['encoding', 'encodings.*']
options = {'py2exe':
{'compressed': 1,
'optimize': 2,
'ascii': 1,
'includes': includes,
'bundle_files': 1,
'dll_excludes': ['MSVCP90.dll'],
}
}
setup(version='1.0.0',
description='search file',
name='search file',
options=options,
zipfile=None,
windows=[{'script': 'core\\tool.py', # 需要打包的程序的主文件路径
'icon_resources': [(1, 'resource\\icon.ico')], # 程序的图标的图片路径
}],
)
