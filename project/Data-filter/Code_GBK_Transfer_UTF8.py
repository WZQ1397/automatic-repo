#coding:utf8 2 
import codecs
# 打开文件 如果此处用codecs.open()方法打开文件，就不用创建reader和writer 
fin = open('test.txt', 'r') 
fout = open('utf8.txt', 'w') 
# 获取 StreamReader 
reader = codecs.getreader('gbk')(fin) 
# 获取 StreamWriter 
writer = codecs.getwriter('utf8')(fout) 
din = reader.read(10) 
while din: 
    writer.write(din) 
    din = reader.read(10)
