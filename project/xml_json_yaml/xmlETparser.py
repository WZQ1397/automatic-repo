#coding:utf-8
#TODO 推荐使用此方法
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys

try:
    tree = ET.parse("movies.xml")     #打开xml文档
    #root = ET.fromstring(movie_string) #从字符串传递xml
    root = tree.getroot()         #获得root节点
except Exception as e:
    print("Error:cannot parse file:movies.xml.")
    sys.exit(1)
print (root.tag, "---", root.attrib)
for child in root:
    print(child.tag, "---", child.attrib['title'])

print ("*"*10)
print (root[0][1].text)   #通过下标访问
print (root[0].tag, root[0].text)
print ("*"*10)

for movie in root.findall('movie'): #找到root节点下的所有movie节点
    rank = movie.find('type').text   #子节点下节点rank的值
    '''
    for name, value in sorted(rank.attrib.items()):
        print('  %-4s = "%s"' % (name, value))
    '''
    name = movie.get('title')      #子节点下属性name的值
    print(name,":",rank)

#TODO 修改xml文件https://docs.python.org/2/library/xml.etree.elementtree.html
'''
for movie in root.findall('movie'):
    rank = int(movie.find('rank').text)
    if rank > 10:
        #删除
        root.remove(movie)
        #修改内容
        new_star  = int(star.text) - 1
        star.text = str(new_star)
        star.set('Total', '10')

tree.write('output.xml')'''