# -*- conding:utf-8 -*-
xls_file = "name.xls"
book = xlrd.open_workbook(xls_file)
sheet1 = book.sheet_by_index(0)
# # 获得指定索引的sheet名
# sheet1_name = book.sheet_names()[0]
# print(sheet1_name)
# # 通过sheet名字获得sheet对象
# sheet1 = book.sheet_by_name(sheet1_name)

# 获得行数和列数
# 总行数
nrows = sheet1.nrows
#总列数

ncols = sheet1.ncols
# 遍历打印表中的内容


for i in range(nrows):
    for j in range(ncols):
        cell_value = sheet1.cell_value(i, j)
        print(cell_value, end = "\t")
    print("")