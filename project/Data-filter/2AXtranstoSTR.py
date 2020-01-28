import re
import argparse

def bintostr(text):
  text = text.replace(' ','')
  text = re.findall(r'.{8}',text)
  s = map(lambda x:chr(int(x,2)),text) #批量二进制转十进制
  flag = ''.join(s)
  return flag

def asciitostr(text):
  if ' ' in text:
    text = text.split(' ')
  elif ',' in text:
    text = text.split(',')
  s = map(lambda x:chr(int(x)),text)
  flag = ''.join(s)
  return flag

def hextostr(text):
  text = re.findall(r'.{2}',text)
  #print text
  s = map(lambda x:chr(int(x,16)),text)
  #print s
  flag = ''.join(s)
  return flag
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-b")
  parser.add_argument("-a")
  parser.add_argument("-x")
  argv = parser.parse_args()
  #print argv
  if argv.b:
    res = bintostr(argv.b)
  elif argv.a:
    res = asciitostr(argv.a)
  elif argv.x:
    res = hextostr(argv.x)
  print (res)
