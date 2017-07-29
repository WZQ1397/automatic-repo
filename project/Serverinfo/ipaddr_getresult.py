import os, re
# execute command, and return the output
def execCmd(cmd):
  r = os.popen(cmd)
  text = r.read()
  r.close()
  return text
# write "data" to file-filename
def writeFile(filename, data):
  f = open(filename, "w")
  f.write(data)
  f.close()
# 获取计算机MAC地址和IP地址
if __name__ == '__main__':
  cmd = "ipconfig /all"
  result = execCmd(cmd)
  pat1 = "Physical Address[\. ]+: ([\w-]+)"
  pat2 = "IP Address[\. ]+: ([\.\d]+)"
  MAC = re.findall(pat1, result)[0] # 找到MAC
  IP = re.findall(pat2, result)[0] # 找到IP
  print("MAC=%s, IP=%s" %(MAC, IP))
