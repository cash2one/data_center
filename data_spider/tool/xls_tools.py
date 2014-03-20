#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Xie Guanfu
@contact: xieguanfu@maimiaotech.com
@date: 2014-03-05 10:23
@version: 0.0.0
@license: Copyright Maimiaotech.com
@copyright: Copyright Maimiaotech.com

"""
import  xdrlib ,sys
import xlrd
def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e)

def excel_table_from_file_byindex(file,colnameindex=-1,by_index=0,colnames=[]):
    data = file
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    if not colnames and colnameindex > -1:
        colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
            list.append(app)
    return list

def excel_table_byindex(file,colnameindex=-1,by_index=0,colnames=[]):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows #行数
    ncols = table.ncols #列数
    if not colnames and colnameindex > -1:
        colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i] 
            list.append(app)
    return list

def excel_table_byname(file,colnameindex=0,by_name=u'Sheet1'):
    data = open_excel(file)
    table = data.sheet_by_name(by_name)
    nrows = table.nrows #行数 
    colnames =  table.row_values(colnameindex) #某一行数据 
    list =[]
    for rownum in range(1,nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                app[colnames[i]] = row[i]
            list.append(app)
    return list

def test():
    file = "/home/xiegf/app/Spider/ztc/rpt/2014-03-03_2014-03-03adgroup.csv"

    colnames = ["page","campaign","pv","click","cost","cpc","ctr"]
    tables = excel_table_byindex(file,colnames=colnames)
    for row in tables:
        print row 

#    tables = excel_table_byname(file)
#    for row in tables:
#        print row

if __name__=="__main__":
    test()


