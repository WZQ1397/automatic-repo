#TODO xml.dom.minidom是DOM API的极简化实现
import xml.dom.minidom

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("movies.xml")
collection = DOMTree.documentElement
if collection.hasAttribute("shelf"):
   print("Root element : %s" % collection.getAttribute("shelf"))

# 在集合中获取所有电影,大标题title
movies = collection.getElementsByTagName("movie")

# 打印每部电影的详细信息
for movie in movies:
   print ("*****Movie*****")
   if movie.hasAttribute("title"):
      #根据选取的属性
      print ("Title: %s" % movie.getAttribute("title"))

   for childnode in ['type','format','rating','description']:
        print(str(childnode).capitalize()+": %s"
              % movie.getElementsByTagName(childnode)[0].childNodes[0].data)