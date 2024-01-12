# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 17:24:48 2024

@author: Administrator
"""

import subprocess
import re

import tkinter as tk
import tkinter.filedialog as tkfd
import tkinter.messagebox as tkmb

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import style
from matplotlib import pyplot as plt
import matplotlib as mtplt

import math

def GetInfo():
    command = ['nvidia-smi']
    out_put = subprocess.run(command,capture_output=True)
    result= f'{out_put.stdout}'
    
    # 解析数据
    # GPU使用率
    match_0 = re.findall(' *([0-9]{1,3})% *Default *',result)
    print(match_0)
    
    # 显存使用率
    match_1 = re.findall(' *([0-9]{1,6})MiB / *([0-9]{1,6})MiB *',result)
    print(match_1)
    
    # 温度
    match_2 = re.findall('N/A *([0-9]{1,3})C  *',result)
    print(match_2) 
    
    # 功率
    match_3 = re.findall(' *([0-9]{1,3})W */ *',result)
    print(match_3)
    
    return match_0 , match_1 , match_2 , match_3

class  MainWindow : 
    def __init__(self , MainWindow) :
        # 创建窗口
        self.top = MainWindow
        self.top.title('NVIDIA显卡状态监测')
        # top.geometry('600x200')
        self.top.resizable(width=0, height=0)
        # top2=tk.Toplevel()
        self.top2=tk.Frame(self.top)
        self.top2.pack(padx=15,pady=15)
        
        # 初始化数据
        # command = ['nvidia-smi']
        # out_put = subprocess.run(command,capture_output=True)
        # result= f'{out_put.stdout}'
        # match_0 = re.findall(' *([0-9]{1,3})% *', result)
        
        
        match_0 , match_1 , match_2 , match_3 = GetInfo()
        self.gpu_mem_size = max(  [ max(int(v[0]) , int(v[1])) for v in match_1 ] ) 
        # GPU个数
        self.gpu_count = len(match_0)        
        # print(f'{self.gpu_count = }')
        
        self.GPU_Rate=[]
        self.GPU_Mem=[]
        self.GPU_Temp=[]
        self.GPU_Power=[]
        for i in range(self.gpu_count):
            self.GPU_Rate.append([0 for v in range(300)])
            self.GPU_Mem.append([0 for v in range(300)])
            self.GPU_Temp.append([0 for v in range(300)])
            self.GPU_Power.append([0 for v in range(300)])
        
        
        
        style.use('classic') 
        
        self.figure = Figure(figsize=(8 , 6), dpi=100)
        
        self.subplot_0 = self.figure.add_subplot(4, 1, 1)
        self.subplot_0.set_title('GPU_Rate')
        self.subplot_0.set_ylim([0 , 100])
        self.subplot_0.set_yticks([v for v in range(0 , 100, 20)])
        self.subplot_0.grid()
        
        self.subplot_1 = self.figure.add_subplot(4, 1, 2)
        self.subplot_1.set_title('GPU_Mem')
        self.subplot_1.set_ylim([0 , self.gpu_mem_size  // 1024])
        self.subplot_1.set_yticks([v for v in range(0 , self.gpu_mem_size  // 1024, self.gpu_mem_size  // 1024 // 5)])
        self.subplot_1.grid()
        
        self.subplot_2 = self.figure.add_subplot(4, 1, 3)
        self.subplot_2.set_title('GPU_Temp')
        self.subplot_2.set_ylim([0 , 100])
        self.subplot_2.set_yticks([v for v in range(0 , 100, 20)])
        self.subplot_2.grid()
        
        self.subplot_3 = self.figure.add_subplot(4, 1, 4)
        self.subplot_3.set_title('GPU_Power')
        self.subplot_3.set_ylim([0 , 250])
        self.subplot_3.set_yticks([v for v in range(0 , 250, 50)])
        self.subplot_3.grid()
        
        self.figure.tight_layout()    
        
        self.canvas = FigureCanvasTkAgg(self.figure , master = self.top2)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()
        
        # 定时刷新
        self.top.after(1000 , func = self.Update)
        
    def Update(self) :        
        match_0 , match_1 , match_2 , match_3 = GetInfo()
        
        self.subplot_0.clear()
        self.subplot_1.clear()
        self.subplot_2.clear()
        self.subplot_3.clear()
        
        for i in range(self.gpu_count):
            
            self.GPU_Rate[i].append(int(match_0[i]))
            if len(self.GPU_Rate[i]) > 300 :
                self.GPU_Rate[i].pop(0)
            self.subplot_0.plot(self.GPU_Rate[i] , label = f'GPU:{i}')
            self.subplot_0.legend(loc='lower left',fontsize='small')
            self.subplot_0.set_title('GPU_Rate')
            self.subplot_0.set_ylim([0 , 100])
            self.subplot_0.set_yticks([v for v in range(0 , 100, 20)])
            self.subplot_0.grid()
            # plt.subplot(4, 1, 1)
            # plt.plot(self.GPU_Rate[i] , label = f'GPU:{i}')
            # plt.legend(loc='lower left',fontsize='small')
            # plt.ylim(bottom=0 , top=100)
            # plt.title('GPU使用率')
            
            self.GPU_Mem[i].append(int(match_1[i][0] )  // 1024)
            if len(self.GPU_Mem[i]) > 300 :
                self.GPU_Mem[i].pop(0)
            self.subplot_1.plot(self.GPU_Mem[i] , label = f'GPU:{i}')
            self.subplot_1.legend(loc='lower left',fontsize='small')
            self.subplot_1.set_title('GPU_Mem')
            self.subplot_1.set_ylim([0 , self.gpu_mem_size  // 1024])
            self.subplot_1.set_yticks([v for v in range(0 , self.gpu_mem_size  // 1024, self.gpu_mem_size  // 1024 // 5)])
            self.subplot_1.grid()
            # plt.subplot(4, 1, 2)
            # plt.plot(self.GPU_Mem[i] , label = f'GPU:{i}')
            # plt.legend(loc='lower left',fontsize='small')
            
                
            self.GPU_Temp[i].append(int(match_2[i]))
            if len(self.GPU_Temp[i]) > 300 :
                self.GPU_Temp[i].pop(0)
            self.subplot_2.plot(self.GPU_Temp[i] , label = f'GPU:{i}')
            self.subplot_2.legend(loc='lower left',fontsize='small')
            self.subplot_2.set_title('GPU_Temp')
            self.subplot_2.set_ylim([0 , 100])
            self.subplot_2.set_yticks([v for v in range(0 , 100, 20)])
            self.subplot_2.grid()
            # plt.subplot(4, 1, 3)
            # plt.plot(self.GPU_Temp[i] , label = f'GPU:{i}')
            # plt.legend(loc='lower left',fontsize='small')
            
            self.GPU_Power[i].append(int(match_3[i]))
            if len(self.GPU_Power[i]) > 300 :
                self.GPU_Power[i].pop(0)
            self.subplot_3.plot(self.GPU_Power[i] , label = f'GPU:{i}')
            self.subplot_3.legend(loc='lower left',fontsize='small')
            self.subplot_3.set_title('GPU_Power')
            self.subplot_3.set_ylim([0 , 250])
            self.subplot_3.set_yticks([v for v in range(0 , 250, 50)])
            self.subplot_3.grid()
            # plt.subplot(4, 1, 4)
            # plt.plot(self.GPU_Power[i] , label = f'GPU:{i}')
            # plt.legend(loc='lower left',fontsize='small')
         
        self.figure.tight_layout()    
        self.canvas.draw()
        
        # 定时刷新
        self.top.after(1000 , func = self.Update)
        
        

if __name__ == '__main__':
    root = tk.Tk()
    MainWindow = MainWindow(root)
    root.mainloop()
    