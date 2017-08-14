#How to write to an Excel using xlwt module
import xlwt
#创建一个Wordbook对象，相当于创建了一个Excel文件
book = xlwt.Workbook(encoding = "utf-8", style_compression = 0)
#创建一个sheet对象，一个sheet对象对应Excel文件中的一张表格
sheet = book.add_sheet("sheet1", cell_overwrite_ok = True)
#向表sheet1中添加数据
sheet.write(0, 0, "EnglishName")  #其中，"0, 0"指定表中的单元格，"EnglishName"是向该单元格中写入的内容
sheet.write(1, 0, "MaYi")
#最后，将以上操作保存到指定的Excel文件中
book.save("name.xls")