#import numpy as np
#import pandas as pd
import matplotlib.pyplot as plt
import mdfreader
import math
import re
import os
import copy

#打印数据文件中的基本信息
def getMdfInfo(yop):
    print ('MDF File Name: %s'%(yop.fileName))
    print ('Keys in MDF File: %s'%(yop.keys()))
    print ('MDF File Version: %d'%(yop.MDFVersionNumber))
    return

#读取当前文件夹下后缀为dat/mdf/mf4的文件名称
def getFileList():
    file_list = []
    file_dir = os.getcwd()
    list_dir = os.listdir(file_dir)
    for i in list_dir:
        if i.split('.')[-1] == 'dat' or i.split('.')[-1] == 'mdf' or i.split('.')[-1] == 'mf4' or i.split('.')[-1] == 'DAT' or i.split('.')[-1] == 'MDF' or i.split('.')[-1] == 'MF4':
            file_list.append(i)
    return file_list

#基本信息：画图函数
def plotBasicInfo(yop,channel_list,file_name):
    plt.rcParams['font.family'] = 'DejaVu Sans' #全局字体设置，例如Times New Roman, SimHei
    plt.rcParams['font.size'] = 12
    plt.rcParams['figure.figsize'] = (16,9) #图片大小设置
    fig_all = len(channel_list) #计算总的需要画图的张数
    fig_val = math.ceil(pow(fig_all,0.5)) #计算横向和纵向的列数，此处横向列数等于纵向列数
    fig_count = 0 #画图时的计数器
    for i in channel_list:    
        fig_count += 1
        plt.subplot(fig_val,fig_val,fig_count)
        xname = yop.get_channel_master(i) #取当前通道的master通道，即时间通道的名称，例如time_40
        xdata = yop.get_channel_data(xname) #取当前x通道的数据
        ydata = yop.get_channel_data(i) #取当前y通道的数据
        plt.plot(xdata, ydata, linewidth='0.8')
        yLabel = i + ' / ' + yop.get_channel_unit(i) #将坐标名称和坐标单位组合
        plt.xlabel('Time / s')
        plt.ylabel(yLabel)
        plt.grid(True)
    plt.tight_layout(rect=(0,0,1,0.9)) #使子图标题和全局标题与坐标轴不重合
    plt.suptitle(yop.fileName)
    plt.savefig(file_name[:-4] + '.png', dpi = 300) #去除后缀名
    plt.clf()
    return

#获取相应通道列表中数据的第一个值
def getFirstData(yop,channel_list):
    first_data_list = []
    for i in channel_list:
        all_data = yop.get_channel_data(i)
        first_data_list.append(round(all_data[0],2)) #保留两位小数
    return first_data_list

#保存表头文件到fname中
def saveHeadInfo(fname,channel_list):
    head = copy.deepcopy(channel_list) #必须采用深拷贝，才能将文件名添加在列表后面
    head.append('File Name')
    filename = open(fname, 'w')  
    for value in head:
        filename.write(str(value)+'\t')
    filename.write('\n')
    filename.close() 

#保存data_list中的数值到文件中
def saveLogInfo(data_list,fname):
    filename = open(fname, 'a')  
    for value in data_list:
        filename.write(str(value)+'\t')
    filename.write('\n')
    filename.close() 

def main():
    fname = 'DataLogInfo.txt' #需要保存的日志文件名
    file_list = getFileList() #调用getFileList函数，获取当前文件夹下的所有mdf/dat文件
    fig_channel_list = ['MO_Fahrpedalrohwert_01','EM1_IstMoment','ESP_v_Signal','EM1_IstDrehzahl'] #需要做图的通道
    log_channel_list = ['KBI_Aussen_Temp_gef','BMS_Ladezustand','BMS_Temperatur','EM1_Temperatur_EM','EM1_Temperatur_PWR'] #需要提取Log信息的通道
    channel_list = list(set( fig_channel_list + log_channel_list )) #合并两个list并去除重复元素，为所有要加载的列表
    saveHeadInfo(fname,log_channel_list)
    for file_name in file_list:
        yop = mdfreader.mdfreader.Mdf(file_name = file_name, channel_list = channel_list) #用mdfreader加载测试数据
        #file_new_name = file_name[:-4] + '.xlsx' #Excel文件命名
        #yop.export_to_xlsx(file_name = file_new_name) #测试数据进行重采样并导出
        #plotBasicInfo(yop,fig_channel_list,file_name) #将fig_channel_list中的通道做图
        log_info = getFirstData(yop,log_channel_list) #取log_channel_list通道的第一个值
        log_info.append(file_name) #将文件名附加到最后
        saveLogInfo(log_info,fname) #保存当前列表到文件fname中

if __name__ == '__main__':
    main()


