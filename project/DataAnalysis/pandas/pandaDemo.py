# -*- coding: utf-8 -*-
# Author: Zach.Wang
# @Time  : 2020-02-24 16:29
import pandas as pd
import numpy as np
import forgery_py

def getDataInfo(dataTable):
  print(dataTable)
  print(dataTable.size,dataTable.shape,dataTable.index)
  print(dataTable.dtypes)
  print(dataTable.columns)
  print(dataTable.values)
  print(dataTable.describe())
  print(dataTable.T)
  print(dataTable.sort_index(axis=1,ascending=False))
  print(dataTable.sort_values(by='id',ascending=False))

def generateData():
  # print(pd.Series([1,2,3,4,np.nan]))
  dates = pd.date_range(start='2020-01-05',
                      end='2020-02-01',
                      # periods=20,
                      # tz="Europe/London",
                      freq='D')
  # print(dates.values)
  y=1
  step=0.01
  data=[]
  for x in range(20):
    y=y*(1+step)
    data.append(y)
  # print(pd.DataFrame(data=data,index=dates,columns=['values',]))
  # print(pd.DataFrame(data=np.arange(9).reshape((3,3))))
  dataTable=pd.DataFrame({'id':np.arange(1,10),
                      'name': [ forgery_py.name.full_name() for _ in range(9)],
                     'address':[forgery_py.address.street_address() for _ in range(9)],
                      'city':'vanillas'},dates[1:10])
  return dataTable

def selectData(dataTable):
  # select name from dataTable
  print(dataTable.name,'\n', dataTable['name'])
  # select * from dataTable where index between 0 and 2
  print(dataTable[0:2])
  # select * from dataTable where index.label = '2020-01-06'
  print(dataTable.loc['2020-01-06'])
  # select id,name from dataTable
  print(dataTable.loc[:,['id','name']])
  # select name from dataTable where index.label = '2020-01-06'
  print(dataTable.loc['2020-01-06',['name']])
  # select name,address from dataTable where index = 1
  # iloc[[index,],start_col:end_col(not reach)]
  print(dataTable.iloc[[1],1:3])
  # select name,address from dataTable where id > 5
  # Boolean indexing
  print(dataTable[dataTable.id>5])
  # select name,city from dataTable where index = 1
  # FIXME deprecated
  # print(dataTable.ix[:3,['name','city']])

def insertData(dataTable):
  valuelist=[10,'zach',"fask asia","seafoo"]
  # dataTable.loc[10]=valuelist
  # set new values
  dataTable.loc[pd.to_datetime('2020-01-16 00:00:00')]=valuelist
  dataTable.loc[pd.to_datetime('2020-01-15 00:00:00')] = dataTable.columns.tolist()
  dataTable.loc[pd.to_datetime('2020-01-19 00:00:00')] = [np.nan,np.nan,np.nan,np.nan]
  print(dataTable.sort_index(axis=0,ascending=False))

def updateData(dataTable):
  # set row 1 col 2 data value to zach [col: name]
  dataTable.iloc[1,2]="zach"
  # alter table add column 'comments'
  # update dataTable set comments='null'
  dataTable['comments']="null"
  dataTable.insert(1,'age',np.nan)
  # update dataTable set id=101 where index='2020-01-06'
  dataTable.loc['2020-01-19','comments']=np.nan
  # update dataTable set city='sealand' where city='vanillas'
  dataTable.city[dataTable.city=='vanillas']='sealand'

def deleteInvalidData(dataTable):
  # how={'any', 'all'}  any=> drop has NaN rows, all=> drop all values are NaN rows
  return dataTable.dropna(axis=0,how='all')

def fixInvalidData(dataTable):
  # replace NaN with the value defined
  return dataTable.fillna(value='NULL')

if __name__ == '__main__':
  # dataTable=generateData()
  # getDataInfo(dataTable)
  # insertData(dataTable)
  # updateData(dataTable)
  # selectData(dataTable)
  # judge whether is null value in table
  # print("null value matrix:\n",pd.isnull(dataTable))
  # dataTable = deleteInvalidData(dataTable)
  # dataTable = fixInvalidData(dataTable)
  # print(dataTable)
  # save to csv
  # dataTable.to_csv('pandaDemo.csv')
  # dataTable.to_pickle('pandaDemo.pickle')
  # dataTable.to_html('pandaDemo.html')

