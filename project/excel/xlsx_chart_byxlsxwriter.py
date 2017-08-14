import xlsxwriter

book=xlsxwriter.Workbook('zachfio.xlsx')
sheet=book.add_worksheet()
ffast=open('E:\\zach.csv','r')

al=ffast.readlines()
a=[]

for line in al:
    a.append(line.split(','))
    #print(a)

for i in range(len(a[0])):
    sheet.write(0,i,a[0][i])
for i in range(1,len(a)-1):
    sheet.write(i,0,a[i][0])
    for j in range(1,len(a[0])):
        sheet.write(i,j,float(a[i][j]))

#sheet.insert_image('F5', 'E:\\python\\redis.png')

chart1=book.add_chart({'type': 'column','subtype':'smooth'})

#重中之重来了！直接在Python中远程控制Excel的图表生成！利用add_chart命令，首先选定图表的种类，这里我在未来会持续讲解更新，尽量作到细致化​

chart1.add_series({
    'categories':'=Sheet1!$A$1:$A18',
    'values':'=Sheet1!$B$2:$B18',
    'line':{'color':'red'},
    'name':'=Sheet1!$B$1',
})

#导入第一个Series的数据，categories为横坐标的数，values为纵坐标的数，曲线颜色为红色，名字叫做Exp

chart1.add_series({
    'categories':'=Sheet1!$A$1:$A18',
    'values':'=Sheet1!$C$2:$C18',
    'line':{'color':'blue'},
    'name':'=Sheet1!$C$1',
})

#导入第二个Series的数据，categories为横坐标的数，values为纵坐标的数，曲线颜色为蓝色，名字叫做Sim
#    配置series的另一种方法     
#     #     [sheetname, first_row, first_col, last_row, last_col]   
#     chart1.add_series({  
#         'name':         ['Sheet1',0,1],  
#         'categories':   ['Sheet1',1,0,6,0],  
#         'values':       ['Sheet1',1,1,6,1],  
#                        })  
#         
#   
#   
#     chart1.add_series({  
#         'name':       ['Sheet1', 0, 2],  
#         'categories': ['Sheet1', 1, 0, 6, 0],  
#         'values':     ['Sheet1', 1, 2, 6, 2],  
#     })  

chart1.set_x_axis({'name':'Type'})
chart1.set_y_axis({'name':'Value'})

chart1.set_title({
    'name':'Analysis Table',
})
chart1.set_style(12)
sheet.insert_chart('F1',chart1,{'x_offset': 25, 'y_offset': 10})
print(chart1)
book.close()