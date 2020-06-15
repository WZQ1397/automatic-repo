import pathlib
from datetime import datetime
from collections import Counter

def countAllFileTypes(directory):
  gen = (i.suffix for i in directory.iterdir())
  print(Counter(gen))

def countSpecFileType(ftype):
  gen =(p.suffix for p in pathlib.Path.cwd().glob('*.'+ftype))
  print(Counter(gen))

# countSpecFileType('py')

def dirTree(directory):
  print(f'+ {directory}')
  for path in sorted(directory.rglob('*')):
    depth = len(path.relative_to(directory).parts)
    spacer = '  ' * depth
    print(f'{spacer}+ {path.name}')

now_path = pathlib.Path.cwd()
dirTree(now_path)
# parts方法可以返回路径的各部分
print(now_path.parts)

time, file_path = max((f.stat().st_mtime, f) for f in now_path.iterdir())
print(datetime.fromtimestamp(time).strftime("%b %d %Y %H:%M:%S"), file_path)