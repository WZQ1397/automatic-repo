# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-04-01 19:43

'''
a : append which used to add sth new into file
+ : add new things into file : r+ , w+ , a+ ???
rw × r+ √: you want both read or write file at the same time
             is not allowed in python with rw
'''


def attrOfOpenFile(f):
  print("%s\tmode: %s" % (f.name, f.mode))
  print("\t\t encoding: %s" % (f.encoding))
  print("\t\t closed: %s" % (f.closed))


def readFileMethodA():
  # step 1: open the file
  '''
  mode r ==> if you not specify the mode, default is 'r'
  '''
  f = open("abc.txt")
  # step 2: do sth for the file
  result = f.read()
  print(result)
  # print(type(f))
  # step 3: save the file and close it
  f.close()


def readFileMethodB():
  # step 1: open the file
  '''
  mode r ==> if you not specify the mode, default is 'r'
  '''
  f = open("abc.txt")
  # step 2: do sth for the file
  for result in f.read():
    print(result, end="")
  # step 3: save the file and close it
  f.close()


def readFileMethodUseContextManager():
  # use with ... as structure to simpify the file IO
  with open("abc.txt") as f:
    for result in f.read():
      print(result, end="")
    # get the attribute
    print()
    attrOfOpenFile(f)
  attrOfOpenFile(f)


def writeBinaryFile(content):
  f = open("abc2.txt", "wb")
  # TypeError: a bytes-like object is required, not 'str'
  # TypeError: string argument without an encoding
  for v in content:
    f.writelines(bytes(v + "\n", encoding="utf-8"))
  f.close()


def writeFile(content):
  # step 1: open the file
  '''
  mode w ==> if the file not exists, it will be created.
             if the file exists, the content it has will be overwrited.
  '''
  f = open("abc2.txt", "w")
  # step 2: do sth for the file
  # str="this is python3.7!"
  f.write(content)

  # step 3: save the file and close it
  f.close()


def appendToFile(content, newline=True):
  # step 1: open the file
  '''
  mode w ==> if the file not exists, it will be created.
             if the file exists, the content it has will be overwrited.
  '''
  f = open("abc.txt", "a")
  # step 2: do sth for the file
  # str="this is python3.7!"
  if newline:
    f.write("\n")
  f.write(content)
  # step 3: save the file and close it
  f.close()


# print("{:*^50}".format("before changed"))
# # read the file not changed
# readFileMethodA()
# # writeFile("teacher Zach and student Jon")
# writeBinaryFile("teacher Zach and student Jon")
# # appendToFile("this is append content!",False)
# print("{:*^50}".format("after changed"))
# # read the file updated
# readFileMethodUseContextManager()

'''
FIXME Q1: How to print the 2th line of a file?
      Q2: Print every 2rd line of a given file? (addon)
      Q3: Print a random line of a given file? (addon)
      Q4: Print the number of lines in a given file
      Q5: Print the number of words in a given file
'''

# module : a set of functions what you want.
from random import randint

filename, selectno = "abc.txt", randint(1, 5)


# method 1:
def printSpecLineContentOfFileByReadlines(filename, selectno):
  with open("abc.txt", "r") as f:
    # return a list ,each line is a item of a list
    content = f.readlines()

  '''
  get the lines of a file
  use the len() to get the items of a list, 
  for we know that one item which means one line in a file.
  
  think above that if we say 3rd line ==> 3rd item in a list
  content[selectno-1] ==> get the selectno line of a file
  '''
  print("{} lines in file {}".format(len(content), filename))
  print("{} th line :\n{}".format(selectno, content[selectno - 1]))
  return content[selectno - 1]


# method 2:
def printSpecLineContentOfFileByRead(filename, selectno, everySelectNoPrint=False):
  with open(filename, "rb") as f:
    # return a string(r)/bytes(rb/b)
    content = f.read()

  '''
  b'content' ==> make string to bytes
  when the content you get is bytes datatype，you should to use this. 
  count([substring/subbytes])  ==> count how many you want to find in main string or bytes
  
  get the content which line you want:
  1. split() --> 2. slice --> 3. convert to string --> 4. split() --> 5. slice --> 6. replace()
  1. get the list from the content of the file 
  2. get the selectno line of a file
  3. now this is bytes ,if you use the string or the file mode is not 'b' you can ignore this step.
  4/5. before we do ==> b'teacher Zach and student Jon\r'
       after we do ==> teacher Zach and student Jon\r
  6. because of this is escaping, we should use double reverse divide to do not escaping.
     delete the content "\r"
  '''
  lines = content.count(b'\n') + 1
  print("%d lines in file %s" % (lines, filename))
  if everySelectNoPrint:
    for line in range(1, lines, selectno):
      print("%dth line :\n%s" % (line,
                                 str(content.split(b'\n')[line - 1])
                                 .split("'")[1]
                                 .replace("\\r", "")
                                 ))
  else:
    result = str(content.split(b'\n')[selectno - 1]).split("'")[1].replace("\\r", "")
    print("%dth line :\n%s" % (selectno,result))
  return result

def countWordsFromSpecLine(content):
  # method 1  replace duplicate space to single ,then count it
  # method 2  realize the count function by yourself (good one)

  strlength = len(content) - 1
  i, spaceBeforeFirstWord, count = 0, False, 0
  if content[i].isspace():
    spaceBeforeFirstWord = True
  while i < strlength:
    i = i + 1
    if content[i].isspace() and spaceBeforeFirstWord:
      continue
    if not content[i].isspace():
      spaceBeforeFirstWord = False
    else:
      if not content[i - 1].isspace():
        count = count + 1
  if content[strlength - 1].isspace():
    count = count - 1

  print("words:", count + 1)

strcontent = printSpecLineContentOfFileByRead(filename, selectno)
countWordsFromSpecLine(strcontent)


