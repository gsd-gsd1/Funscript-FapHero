import math
import random
from tkinter import *
from skimage.metrics import structural_similarity as compare_ssim
import cv2 as cv
import os
import threading
import tkinter
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Notebook, Combobox
import numpy as np
from ffpyplayer.player import MediaPlayer
import sys
import tkinter as tk
from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

import Mouse_Event


def ShowImage(img, canvas, layout):
    print()


class UI:
    def __init__(self, master):
        # 定义相关文件路径变量

        self.selected_folder_out = None  # 输出文件夹目录
        self.selected_file_path = None

        self.select_file_path = tk.StringVar()  # 选中的文件名称
        self.select_file_path_out = tk.StringVar()

        self.select_dir_path = tk.StringVar()
        self.select_dir_path_out = tk.StringVar()

        self.file_output_stream = None  # 文件输出流

        # 定义图片展示框
        self.UI_Image_Canvas = None
        self.UI_Image_Weigh = None
        self.UI_Image_High = None
        self.UI_Image_Mode = None  # 图片显示模式

        # 定义相关位置变量
        self.row_position_base = tk.IntVar()
        self.col_position_base = tk.IntVar()
        self.set_step = tk.IntVar()
        self.radio_box_verb = tk.IntVar()

        # 定义相关视频的参数
        self.Video_Total_Frame = None  # 视频时长总帧数
        self.Video_Frame_Width = None  # 视频宽度
        self.Video_Frame_High = None  # 视频高度
        self.Video_FPS = None  # 视频帧率
        self.Video_Wait = None  # 视频播放帧间隔毫秒数
        self.Video_Frame_Count = None  # 帧数计数器

        self.Video_Time_Hour = None  # 播放时间（小时）
        self.Video_Time_Minute = None  # 播放时间（分钟）
        self.Video_Time_Second = None  # 播放时间（秒）
        self.Video_Time_F = None

        self.Video_Is_Pause = None  # 视频暂停标志
        self.Video_ROI_Area = None  # 感兴趣区域

        # 定义相关分析时变量
        self.Analyze_Max_Strength = tk.StringVar()  # 最大强度输入
        self.Analyze_Min_Strength = tk.StringVar()  # 最低强度输入
        self.Strength_Mode_Verb = tk.IntVar()  # 输出模式选择
        self.Similarity_Degree_Verb = tk.IntVar()  # 相似度调节
        self.Similarity_Degree_Light_Verb = tk.IntVar()  # 灰度亮度阈值调节
        self.Similarity_Degree_Color_Verb = tk.IntVar()  # 颜色阈值调节
        self.Similarity_Degree_NCC_Verb = tk.IntVar()  # NCC阈值调节
        self.Similarity_Degree_SSIM_Verb = tk.IntVar()  # SSIM阈值调节
        self.Sample_ROI = None  # 样本采集

        self.time_and_strength = None  # 时间与强度列表

        # 其他
        self.checkbox_check = tk.IntVar()
        self.Thread_Finish_Select = False
        self.Add_New_Point = False
        self.Change_Show_Color_Verb = tk.IntVar()
        self.Add_New_Point_Verb = tk.IntVar()
        self.Strength_Random_verb = tk.IntVar()
        self.Strength_Random_Min_Time_Verb = tk.IntVar()

        '''首页界面创建'''
        master_frame = Frame(master, name='master_frame', width=1024, height=800)
        master_frame.grid_propagate(False)
        master.title('FapHero转换程序')
        master.resizable(0, 0)
        # 分页
        note = Notebook(master_frame, name='note')
        # 菜单
        menubar = tk.Menu(master)

        # 定义空的菜单单元
        fileMenu = tk.Menu(menubar, tearoff=0)  # tearoff意为下拉
        editMenu = tk.Menu(menubar, tearoff=0)
        toolMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='文件', menu=fileMenu)
        master.config(menu=menubar)
        master_frame.grid()
        # 放置分页
        note.grid(row=0, column=0, ipadx=300, ipady=260)

        '''创建分页1---------主界面'''
        frame_main = Frame(note)
        note.add(frame_main, text="主界面")

        # 初始化相关参数
        self.selected_folder = os.getcwd()
        self.selected_folder_out = os.getcwd()

        self.row_position_base = 3
        self.col_position_base = 1

        self.Analyze_Max_Strength.set("100")
        self.Analyze_Min_Strength.set("20")

        self.Similarity_Degree_Verb.set(3)
        self.Similarity_Degree_Light_Verb.set(5)
        self.Similarity_Degree_Color_Verb.set(70)
        self.Similarity_Degree_NCC_Verb.set(90)
        self.Similarity_Degree_SSIM_Verb.set(70)
        self.time_and_strength = []

        self.radio_box_verb.set(0)
        self.checkbox_check.set(1)

        self.Change_Show_Color_Verb.set(1)
        self.Add_New_Point_Verb.set(0)  # 默认不勾选
        self.Strength_Random_verb.set(2)
        self.Strength_Random_Min_Time_Verb.set(2)  # 0.2s不处理时间

        '''创建标签'''
        # 选择文件标签
        self.SelectFileDir_label = Label(frame_main, text="选择文件")
        self.SelectFileDir_label.grid(row=self.row_position_base * 0, column=self.col_position_base * 0, rowspan=3)
        # 单文件路径输入框
        self.input_entry_file = Entry(frame_main, textvariable=self.select_file_path)
        self.input_entry_file.grid(row=self.row_position_base * 1, column=self.col_position_base * 1, rowspan=3,
                                   sticky=tk.EW)

        # 文件路径选择按钮
        self.btn_Dir = Button(frame_main, text='选择文件', command=self.select_file)
        self.btn_Dir.grid(row=self.row_position_base * 1, column=self.col_position_base * 2, rowspan=3, sticky=tk.W)

        # 文件路径输入框（输出）
        self.out_entry_file = Entry(frame_main, textvariable=self.select_dir_path_out)
        self.out_entry_file.grid(row=self.row_position_base * 2, column=self.col_position_base * 1, rowspan=3,
                                 sticky=tk.EW)

        # 目录路径选择按钮（输出）
        self.btn_Dir = Button(frame_main, text='保存路径', command=self.file_save)
        self.btn_Dir.grid(row=self.row_position_base * 2, column=self.col_position_base * 2, rowspan=3, sticky=tk.W)

        # 强度选择
        self.Select_Strength_Label = Label(frame_main, text="强度选择")
        self.Select_Strength_Label.grid(row=self.row_position_base * 3, column=self.col_position_base * 0, rowspan=3)

        # 最大强度
        self.Select_Max_Strength_Label = Label(frame_main, text="最大强度")
        self.Select_Max_Strength_Label.grid(row=self.row_position_base * 4, column=self.col_position_base * 0,
                                            rowspan=3)
        # 最大强度输入框
        self.Select_Max_Strength_Entry = Entry(frame_main, textvariable=self.Analyze_Max_Strength)
        self.Select_Max_Strength_Entry.grid(row=self.row_position_base * 4, column=self.col_position_base * 1,
                                            rowspan=3)

        # 最低强度
        self.Select_Min_Strength_Label = Label(frame_main, text="最低强度")
        self.Select_Min_Strength_Label.grid(row=self.row_position_base * 5, column=self.col_position_base * 0,
                                            rowspan=3)
        # 最低强度输入框
        self.Select_Min_Strength_Entry = Entry(frame_main, textvariable=self.Analyze_Min_Strength)
        self.Select_Min_Strength_Entry.grid(row=self.row_position_base * 5, column=self.col_position_base * 1,
                                            rowspan=3)

        # 随机强度振幅
        self.Strength_Random_Label = Label(frame_main, text="随机强度振幅(不要\n超过原振幅的一半)")
        self.Strength_Random_Label.grid(row=self.row_position_base * 4, column=self.col_position_base * 2,
                                        rowspan=3)
        self.Strength_Random_Scale = Scale(frame_main, from_=0, to=5, orient="horizontal",
                                           variable=self.Strength_Random_verb)
        self.Strength_Random_Scale.grid(row=self.row_position_base * 4, column=self.col_position_base * 3,
                                        rowspan=3)

        # 随机最小不处理时间
        self.Strength_Random_Min_Time_Label = Label(frame_main, text="随机最小不处理\n时间(1代表0.1s)")
        self.Strength_Random_Min_Time_Label.grid(row=self.row_position_base * 5, column=self.col_position_base * 2,
                                                 rowspan=3)
        self.Strength_Random_Min_Time_Scale = Scale(frame_main, from_=0, to=10, orient="horizontal",
                                                    variable=self.Strength_Random_Min_Time_Verb)
        self.Strength_Random_Min_Time_Scale.grid(row=self.row_position_base * 5, column=self.col_position_base * 3,
                                                 rowspan=3)

        # 相似度标签
        self.Similarity_Degree_Label1 = Label(frame_main, text="使用PHash方法")
        self.Similarity_Degree_Label1.grid(row=self.row_position_base * 6, column=self.col_position_base * 0, rowspan=3)
        self.Similarity_Degree_Label = Label(frame_main, text="相似程度")
        self.Similarity_Degree_Label.grid(row=self.row_position_base * 7, column=self.col_position_base * 0, rowspan=3)
        # 相似度参数调节
        self.Similarity_Degree = Entry(frame_main, textvariable=self.Similarity_Degree_Verb)
        self.Similarity_Degree.grid(row=self.row_position_base * 7, column=self.col_position_base * 1, rowspan=3)
        self.Similarity_Degree_Scale = Scale(frame_main, from_=0, to=100, orient="horizontal",
                                             variable=self.Similarity_Degree_Verb)
        self.Similarity_Degree_Scale.grid(row=self.row_position_base * 7, column=self.col_position_base * 2, rowspan=3)

        # 使用灰度值比较算法
        self.Similarity_Degree_light_Label = Label(frame_main, text="使用亮度比较方法")
        self.Similarity_Degree_light_Label.grid(row=self.row_position_base * 8, column=self.col_position_base * 0,
                                                rowspan=3)
        self.Similarity_Degree_light_Label1 = Label(frame_main, text="阈值")
        self.Similarity_Degree_light_Label1.grid(row=self.row_position_base * 9, column=self.col_position_base * 0,
                                                 rowspan=3)

        self.Similarity_Degree_light = Entry(frame_main, textvariable=self.Similarity_Degree_Light_Verb)
        self.Similarity_Degree_light.grid(row=self.row_position_base * 9, column=self.col_position_base * 1, rowspan=3)
        self.Similarity_Degree_light_Scale = Scale(frame_main, from_=0, to=100, orient="horizontal",
                                                   variable=self.Similarity_Degree_Light_Verb)
        self.Similarity_Degree_light_Scale.grid(row=self.row_position_base * 9, column=self.col_position_base * 2,
                                                rowspan=3)

        # 使用颜色比较算法
        self.Similarity_Degree_Color_Label = Label(frame_main, text="使用颜色比较方法")
        self.Similarity_Degree_Color_Label.grid(row=self.row_position_base * 10, column=self.col_position_base * 0,
                                                rowspan=3)
        self.Similarity_Degree_Color_Label1 = Label(frame_main, text="阈值")
        self.Similarity_Degree_Color_Label1.grid(row=self.row_position_base * 11, column=self.col_position_base * 0,
                                                 rowspan=3)
        self.Similarity_Degree_Color = Entry(frame_main, textvariable=self.Similarity_Degree_Color_Verb)
        self.Similarity_Degree_Color.grid(row=self.row_position_base * 11, column=self.col_position_base * 1, rowspan=3)
        self.Similarity_Degree_Color_Scale = Scale(frame_main, from_=0, to=100, orient="horizontal",
                                                   variable=self.Similarity_Degree_Color_Verb)
        self.Similarity_Degree_Color_Scale.grid(row=self.row_position_base * 11, column=self.col_position_base * 2,
                                                rowspan=3)

        # 使用NCC算法
        self.Similarity_Degree_NCC_Label = Label(frame_main, text="使用NCC比较方法")
        self.Similarity_Degree_NCC_Label.grid(row=self.row_position_base * 12, column=self.col_position_base * 0,
                                              rowspan=3)
        self.Similarity_Degree_NCC_Label1 = Label(frame_main, text="阈值")
        self.Similarity_Degree_NCC_Label1.grid(row=self.row_position_base * 13, column=self.col_position_base * 0,
                                               rowspan=3)
        self.Similarity_Degree_NCC = Entry(frame_main, textvariable=self.Similarity_Degree_NCC_Verb)
        self.Similarity_Degree_NCC.grid(row=self.row_position_base * 13, column=self.col_position_base * 1, rowspan=3)
        self.Similarity_Degree_NCC_Scale = Scale(frame_main, from_=0, to=100, orient="horizontal",
                                                 variable=self.Similarity_Degree_NCC_Verb)
        self.Similarity_Degree_NCC_Scale.grid(row=self.row_position_base * 13, column=self.col_position_base * 2,
                                              rowspan=3)

        # 使用SSIM算法
        self.Similarity_Degree_SSIM_Label = Label(frame_main, text="使用SSIM算法")
        self.Similarity_Degree_SSIM_Label.grid(row=self.row_position_base * 14, column=self.col_position_base * 0,
                                               rowspan=3)
        self.Similarity_Degree_SSIM_Label1 = Label(frame_main, text="阈值")
        self.Similarity_Degree_SSIM_Label1.grid(row=self.row_position_base * 15, column=self.col_position_base * 0,
                                                rowspan=3)
        self.Similarity_Degree_SSIM = Entry(frame_main, textvariable=self.Similarity_Degree_SSIM_Verb)
        self.Similarity_Degree_SSIM.grid(row=self.row_position_base * 15, column=self.col_position_base * 1, rowspan=3)
        self.Similarity_Degree_SSIM_Scale = Scale(frame_main, from_=0, to=100, orient="horizontal",
                                                  variable=self.Similarity_Degree_SSIM_Verb)
        self.Similarity_Degree_SSIM_Scale.grid(row=self.row_position_base * 15, column=self.col_position_base * 2,
                                               rowspan=3)

        check_box_base = 16
        # 选择复选框
        self.Check_Box_Method_Phash = Radiobutton(frame_main, text="使用PHash方法", variable=self.radio_box_verb,
                                                  value=0, command=self.change_input_mode)
        self.Check_Box_Method_Light = Radiobutton(frame_main, text="使用亮度方法", variable=self.radio_box_verb,
                                                  value=1, command=self.change_input_mode)
        self.Check_Box_Method_Color = Radiobutton(frame_main, text="使用颜色方法", variable=self.radio_box_verb,
                                                  value=2, command=self.change_input_mode)
        self.Check_Box_Method_NCC = Radiobutton(frame_main, text="使用NCC方法", variable=self.radio_box_verb,
                                                value=3, command=self.change_input_mode)
        self.Check_Box_Method_SSIM = Radiobutton(frame_main, text="使用SSIM方法", variable=self.radio_box_verb,
                                                 value=4, command=self.change_input_mode)
        self.Check_Box_Method_Phash.grid(row=self.row_position_base * check_box_base, column=self.col_position_base * 0,
                                         rowspan=3,
                                         sticky=W)
        self.Check_Box_Method_Light.grid(row=self.row_position_base * check_box_base, column=self.col_position_base * 1,
                                         rowspan=3,
                                         sticky=W)
        self.Check_Box_Method_Color.grid(row=self.row_position_base * (check_box_base + 0),
                                         column=self.col_position_base * 2, rowspan=3,
                                         sticky=W)
        self.Check_Box_Method_NCC.grid(row=self.row_position_base * (check_box_base + 1),
                                       column=self.col_position_base * 0, rowspan=3,
                                       sticky=W)
        self.Check_Box_Method_SSIM.grid(row=self.row_position_base * (check_box_base + 1),
                                        column=self.col_position_base * 1, rowspan=3,
                                        sticky=W)
        # 显示颜色变化
        self.Change_Show_Color_Label = Label(frame_main, text="显示颜色变化")
        self.Change_Show_Color_Label.grid(row=self.row_position_base * (check_box_base + 2),
                                          column=self.col_position_base * 0, rowspan=3,
                                          sticky=W)
        self.Change_Show_Color_Scale = Scale(frame_main, from_=1, to=3, orient="horizontal",
                                             variable=self.Change_Show_Color_Verb)
        self.Change_Show_Color_Scale.grid(row=self.row_position_base * (check_box_base + 2),
                                          column=self.col_position_base * 1, rowspan=3,
                                          sticky=W)
        # 随机强度变化
        self.Strength_Mode_CheckBox = Checkbutton(frame_main, text="随机强度变化", variable=self.checkbox_check,
                                                  command=self.strength_mode_fun)
        self.Strength_Mode_CheckBox.grid(row=self.row_position_base * (check_box_base + 3),
                                         column=self.col_position_base * 0, rowspan=3,
                                         sticky=W)
        # 开启整个周期
        self.Open_All_T_CheckBox = Checkbutton(frame_main, text="增加节点数量", variable=self.Add_New_Point_Verb,
                                               command=self.Add_New_Point_Fun)
        self.Open_All_T_CheckBox.grid(row=self.row_position_base * (check_box_base + 3),
                                      column=self.col_position_base * 1, rowspan=3,
                                      sticky=W)
        self.strength_mode_fun()
        self.change_input_mode()
        # 开始运算
        self.btn_Dir = Button(frame_main, text='开始', command=self.start_analyze)
        self.btn_Dir.grid(row=self.row_position_base * (check_box_base + 4), column=self.col_position_base * 1,
                          rowspan=3, sticky=NSEW)

    # 文件夹选择
    def select_folder(self):
        self.selected_folder = filedialog.askdirectory(initialdir=self.selected_folder)  # 使用askdirectory函数选择文件夹
        self.select_dir_path.set(self.selected_folder)

    def select_folder_out(self):
        self.selected_folder_out = filedialog.askdirectory(initialdir=self.selected_folder_out)  # 使用askdirectory函数选择文件夹
        self.select_dir_path_out.set(self.selected_folder_out)

    # 单个文件选择
    def select_file(self):
        files = [('All Files', '*.*'),
                 ('mp4 Files', '*.mp4'),
                 ('avi Document', '*.avi')]
        self.selected_file_path = filedialog.askopenfilename(initialdir=self.selected_folder,
                                                             filetypes=files)  # 使用askopenfilename函数选择单个文件
        self.select_file_path.set(self.selected_file_path)

    '''保存文件'''

    def file_save(self):
        files = [('Function Files', '*.funscript'),
                 ('Text Document', '*.txt'),
                 ('All Files', '*.*')]
        self.file_output_stream = filedialog.asksaveasfile(mode='w', filetypes=files)
        if self.file_output_stream:
            self.write_to_file()
        else:
            print('文件保存失败！')

    # 设置其他复选框状态
    def change_input_mode(self):
        num = self.radio_box_verb.get()
        if num == 0:
            # 灰度与颜色均不可用
            self.Similarity_Degree_light["state"] = DISABLED
            self.Similarity_Degree_Color['state'] = DISABLED
            self.Similarity_Degree_NCC['state'] = DISABLED
            self.Similarity_Degree_SSIM["state"] = DISABLED

            self.Similarity_Degree_light_Scale['state'] = DISABLED
            self.Similarity_Degree_Color_Scale['state'] = DISABLED
            self.Similarity_Degree_NCC_Scale['state'] = DISABLED
            self.Similarity_Degree_SSIM_Scale["state"] = DISABLED

            self.Similarity_Degree['state'] = NORMAL
            self.Similarity_Degree_Scale['state'] = NORMAL
        elif num == 1:
            # PHash与颜色不能用
            self.Similarity_Degree["state"] = DISABLED
            self.Similarity_Degree_Color['state'] = DISABLED
            self.Similarity_Degree_NCC['state'] = DISABLED
            self.Similarity_Degree_SSIM["state"] = DISABLED

            self.Similarity_Degree_Scale['state'] = DISABLED
            self.Similarity_Degree_Color_Scale['state'] = DISABLED
            self.Similarity_Degree_NCC_Scale['state'] = DISABLED
            self.Similarity_Degree_SSIM_Scale["state"] = DISABLED

            self.Similarity_Degree_light['state'] = NORMAL
            self.Similarity_Degree_light_Scale['state'] = NORMAL
        elif num == 2:
            # PHash与灰度不能用
            self.Similarity_Degree["state"] = DISABLED
            self.Similarity_Degree_light['state'] = DISABLED
            self.Similarity_Degree_NCC['state'] = DISABLED
            self.Similarity_Degree_SSIM["state"] = DISABLED

            self.Similarity_Degree_Scale['state'] = DISABLED
            self.Similarity_Degree_light_Scale['state'] = DISABLED
            self.Similarity_Degree_NCC_Scale['state'] = DISABLED
            self.Similarity_Degree_SSIM_Scale["state"] = DISABLED

            self.Similarity_Degree_Color['state'] = NORMAL
            self.Similarity_Degree_Color_Scale['state'] = NORMAL
        elif num == 3:
            # 仅使用NCC
            self.Similarity_Degree["state"] = DISABLED
            self.Similarity_Degree_light["state"] = DISABLED
            self.Similarity_Degree_Color['state'] = DISABLED
            self.Similarity_Degree_SSIM["state"] = DISABLED

            self.Similarity_Degree_Scale['state'] = DISABLED
            self.Similarity_Degree_light_Scale['state'] = DISABLED
            self.Similarity_Degree_Color_Scale['state'] = DISABLED
            self.Similarity_Degree_SSIM_Scale["state"] = DISABLED

            self.Similarity_Degree_NCC['state'] = NORMAL
            self.Similarity_Degree_NCC_Scale['state'] = NORMAL
        elif num == 4:
            # 仅使用SSIM
            self.Similarity_Degree["state"] = DISABLED
            self.Similarity_Degree_light["state"] = DISABLED
            self.Similarity_Degree_Color['state'] = DISABLED
            self.Similarity_Degree_NCC['state'] = DISABLED

            self.Similarity_Degree_Scale['state'] = DISABLED
            self.Similarity_Degree_light_Scale['state'] = DISABLED
            self.Similarity_Degree_Color_Scale['state'] = DISABLED
            self.Similarity_Degree_NCC_Scale['state'] = DISABLED

            self.Similarity_Degree_SSIM["state"] = NORMAL
            self.Similarity_Degree_SSIM_Scale["state"] = NORMAL

    '''开始运行分析程序'''

    def start_analyze(self):
        print(self.selected_file_path)
        # 首先播放视频
        # self.start_video(False)  # 不播放声音
        th_select = threading.Thread(target=self.start_video, args=(False,))
        th_select.setDaemon(True)  # 守护线程
        th_select.start()
        # 创建一个监听线程
        # th_select_listen = threading.Thread(target=Video_Listen, args=(th_select,))
        # th_select_listen.setDaemon(True)
        # th_select_listen.start()

    '''将数据保存到文件中'''

    def write_to_file(self):
        print(self.selected_folder)
        # 读取视频，根据灰度变化情况进行数据分析
        self.analyze_by_area()

    '''有声播放视频'''

    def start_video(self, UsePlayer):
        file_path = self.selected_file_path
        cap = cv.VideoCapture(file_path)
        player = None
        if UsePlayer:
            player = MediaPlayer(file_path)
        # 检查文件打开状态
        if not cap.isOpened():
            print('错误！ 无法打开具体文件')
            return
        self.Video_Total_Frame = cap.get(cv.CAP_PROP_FRAME_COUNT)
        self.Video_Frame_Width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        self.Video_Frame_High = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        self.Video_FPS = cap.get(cv.CAP_PROP_FPS)
        self.Video_Wait = int(1000 / self.Video_FPS)
        self.Video_Frame_Count = 0
        self.Video_Is_Pause = False
        rect = None
        # 循环读取视频
        image_High = 0
        image_Width = 0
        show_video = False
        while True:
            # 读取帧图像
            ret, frame = cap.read()
            if not ret:
                if self.Video_Frame_Count < self.Video_Total_Frame:
                    # 读取错误
                    print("视频读取错误！ ")
                else:
                    # 正常结束
                    print("视频结束！ ")
                break
            self.Video_Frame_Count = self.Video_Frame_Count + 1
            cv.putText(frame, "[{}/{}]".format(str(self.Video_Frame_Count), str(int(self.Video_Total_Frame))), (20, 50),
                       cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 9), 2)
            # 重新调整图片大小
            # 获取图片长宽比
            rate_w_h = self.Video_Frame_Width / self.Video_Frame_High
            # 根据分辨率进行调整
            if rate_w_h > 1:
                image_High = 800 / rate_w_h
                image_High = int(image_High)  # 取整
                image_Width = image_High * rate_w_h
                image_Width = int(image_Width)  # 取整
            elif rate_w_h < 1:
                image_Width = 800 * rate_w_h
                image_Width = int(image_Width)
                image_High = image_Width / rate_w_h
                image_High = int(image_High)

            dst = cv.resize(frame, (image_Width, image_High), interpolation=cv.INTER_CUBIC)
            # 计算当前播放时间
            self.Video_Time_Hour = int(self.Video_Frame_Count / self.Video_FPS / 60 / 60)
            self.Video_Time_Minute = int(self.Video_Frame_Count / self.Video_FPS / 60)
            self.Video_Time_Second = self.Video_Frame_Count / self.Video_FPS % 60
            s = math.modf(self.Video_Time_Second)
            self.Video_Time_Second = int(self.Video_Time_Second)
            self.Video_Time_F = int(s[0] * self.Video_FPS)
            # print("{:0>2d}:{:0>2d}:{:0>2d}.{:0>2d}".format(self.Video_Time_Hour, self.Video_Time_Minute, self.Video_Time_Second, self.Video_Time_F))

            # 显示帧图像
            cv.imshow('movie', dst)
            # 播放间隔
            if not show_video:
                wk = cv.waitKey(int(self.Video_Wait))
            else:
                wk = cv.waitKey(1)
            # 按键值  & 0xFF是一个二进制AND操作 返回一个不是单字节的代码
            keycode = wk & 0xff
            # 空格键暂停
            if keycode == ord(" "):
                if not self.Video_Is_Pause:
                    if UsePlayer:
                        player.set_pause(1)  # 暂停声音播放
                    self.Video_Is_Pause = True

                    while self.Video_Is_Pause:  # 如果没按下空格，继续阻塞
                        st = cv.waitKey(0)
                        keycode1 = st & 0xff
                        if keycode1 == ord(" "):
                            self.Video_Is_Pause = False
                        if keycode1 == 27:  # 避免卡死ESC退出
                            keycode = 27
                            break
                        if cv.getWindowProperty('movie', cv.WND_PROP_VISIBLE) < 1:  # 当窗口关闭时为-1，显示时为0
                            print("窗口全部关闭(暂停)")
                            break
                        # 按a开始截图并进入选择框模式
                        if keycode1 == ord('A'):
                            rect = Mouse_Event.draw_image_rectangle_on_mouse(dst)
                            self.Sample_ROI = dst[int(rect[1]):int(rect[3]), int(rect[0]):int(rect[2])]
                            print("结束截图")
                    if UsePlayer:
                        player.set_pause(0)  # 继续声音播放
                    self.Video_Is_Pause = False
            # 按a开始截图并进入选择框模式
            if keycode == ord('A'):
                rect = Mouse_Event.draw_image_rectangle_on_mouse(dst)
                print(rect)
                self.Sample_ROI = dst[int(rect[1]):int(rect[3]), int(rect[0]):int(rect[2])]
                print("结束截图")

            # Q键加速 S键恢复
            if keycode == ord('Q'):
                print("加速播放")
                show_video = True
            if keycode == ord('S'):
                print("恢复原来速率")
                show_video = False

            # esc键退出
            if keycode == 27:
                print("退出播放! ")
                break
            if cv.getWindowProperty('movie', cv.WND_PROP_VISIBLE) < 1:  # 当窗口关闭时为-1，显示时为0
                print("窗口全部关闭(运行)")
                break
        # 释放实例
        cap.release()
        # 销毁窗口
        # 如果选中矩形框
        cv.destroyAllWindows()
        if rect is not None:
            self.Video_ROI_Area = rect
        # 进行后续运算
        # 开始分析视频并写入文件
        self.file_save()

    '''根据选中区域进行变化分析  使用不透明方式准确率高 '''

    def analyze_by_area(self):
        rect = self.Video_ROI_Area
        file_path = self.selected_file_path
        cap = cv.VideoCapture(file_path)
        if not cap.isOpened():
            print("视频打开失败! ")
            return
        # 预先读入一帧
        ret, frame_past = cap.read()
        if not ret:
            print("视频读取出错！")
            return
        # 重新调整图片大小
        # 获取图片长宽比
        rate_w_h = self.Video_Frame_Width / self.Video_Frame_High
        image_Width = 0
        image_High = 0
        # 根据分辨率进行调整
        if rate_w_h > 1:
            image_High = 800 / rate_w_h
            image_High = int(image_High)  # 取整
            image_Width = image_High * rate_w_h
            image_Width = int(image_Width)  # 取整
        elif rate_w_h < 1:
            image_Width = 800 * rate_w_h
            image_Width = int(image_Width)
            image_High = image_Width / rate_w_h
            image_High = int(image_High)
        frame_past = cv.resize(frame_past, (image_Width, image_High), interpolation=cv.INTER_CUBIC)
        frame_past = cv.cvtColor(frame_past, cv.COLOR_BGR2GRAY)  # 灰度化图片
        roi_past: np.ndarray = frame_past[rect[1]:rect[3], rect[0]:rect[2]]

        first_inverse = 0

        # PHash
        hash_past = pHash(roi_past)
        hash_inverse_first = None

        # Light
        light_past = light_cac_fun(roi_past)
        light_inverse_first = None

        # color
        roi_color = None
        sample_hsv = handle_img(self.Sample_ROI)
        hist_sample = create_rgb_hist(sample_hsv)
        compare_hist = 0

        max_position = 0
        show_result = False
        max_n = 0
        count = 1
        show_video = False  # 播放速率
        wk = None
        show_color = (0, 0, 255)
        while True:
            # 正式读入一帧
            ret, frame_pre = cap.read()
            if not ret:
                if count < self.Video_Total_Frame:
                    # 读取错误
                    print("读取视频某帧出错！")
                else:
                    print("视频正常结束！")
                break
            count = count + 1
            frame_pre = cv.resize(frame_pre, (image_Width, image_High), interpolation=cv.INTER_CUBIC)
            roi_color = frame_pre[rect[1]:rect[3], rect[0]:rect[2]]  # 注意相对位置
            image_show = frame_pre
            frame_pre = cv.cvtColor(frame_pre, cv.COLOR_BGR2GRAY)
            # 进行显示颜色的确认
            if self.Change_Show_Color_Verb.get() == 1:
                show_color = (0, 0, 255)
            elif self.Change_Show_Color_Verb.get() == 2:
                show_color = (0, 255, 0)
            elif self.Change_Show_Color_Verb.get() == 3:
                show_color = (255, 0, 0)
            else:  # 异常处理
                show_color = (255, 255, 255)
            # 最小不处理时间
            Min_No_Deal_Time = 0.1 * float(self.Strength_Random_Min_Time_Verb.get())
            # 提取选定区域
            roi_pre: np.ndarray = frame_pre[rect[1]:rect[3], rect[0]:rect[2]]
            # 进行相似度匹配（使用pHash算法）
            if self.radio_box_verb.get() == 0:
                # 计算哈希
                hash_pre = pHash(roi_pre)
                # 计算汉明距离
                n = cmpHash(hash_past, hash_pre)
                if self.Similarity_Degree_Verb.get() is None:
                    compare_get_Phash = 0
                else:
                    compare_get_Phash = self.Similarity_Degree_Verb.get()
                if n <= compare_get_Phash or first_inverse != 0:
                    if first_inverse != 0:  # 说明出现了一次翻转
                        n_check = cmpHash(hash_inverse_first, hash_pre)
                        if n_check > max_n:  # 说明本次与上次相比差距较大(还在增大)
                            max_n = n_check
                        else:  # 最大可能就是相似度变高
                            # 将该点作为转折点（最大）
                            max_position = count  # 记录节点
                            max_n = 0  # 清除数据
                            first_inverse = 0
                            self.time_and_strength.append(max_position)  # 将数据存入列表
                            show_result = True
                elif n > self.Similarity_Degree_Verb.get() and first_inverse == 0:
                    # print("图片不相似！", count)
                    # 记录第一次翻转
                    if first_inverse == 0 and count - max_position > self.Video_FPS * Min_No_Deal_Time:  # 一次检测完成后，后续0.2s不进行检测
                        hash_inverse_first = hash_past
                        first_inverse = 1
                # 为下次循环做准备
                hash_past = hash_pre
                frame_past = frame_pre
                roi_past = roi_pre
                if show_result:
                    # print("展示(PHash) ", count, n)
                    cv.rectangle(image_show, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])),
                                 color=show_color,
                                 thickness=-1)
                    show_result = False

            elif self.radio_box_verb.get() == 1:  # 使用灰度算法
                # 计算灰度值
                light_pre = light_cac_fun(roi_pre)
                compare_light = light_check_fun(light_past, light_pre)
                # 如果超出设定阈值
                if self.Similarity_Degree_Light_Verb.get() is None:
                    compare_get_light = 0
                else:
                    compare_get_light = self.Similarity_Degree_Light_Verb.get() / 100
                if compare_light <= compare_get_light or first_inverse != 0:
                    if first_inverse != 0:  # 说明出现了一次翻转
                        n_check = light_check_fun(light_inverse_first, light_pre)
                        if n_check > max_n:
                            max_n = n_check
                        else:
                            max_position = count
                            max_n = 0  # 清除数据
                            first_inverse = 0
                            self.time_and_strength.append(max_position)  # 将数据存入列表
                            show_result = True

                elif compare_light > self.Similarity_Degree_Light_Verb.get() / 100:
                    if first_inverse == 0 and count - max_position > self.Video_FPS * Min_No_Deal_Time:  # 一次检测完成后，后续0.2s不进行检测
                        light_inverse_first = light_past
                        first_inverse = 1
                # 为下次循环做准备
                light_past = light_pre
                frame_past = frame_pre
                roi_past = roi_pre
                if show_result:
                    print("展示(灰度) ", count, compare_light)
                    cv.rectangle(image_show, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])),
                                 color=show_color,
                                 thickness=-1)
                    show_result = False

            elif self.radio_box_verb.get() == 2:  # 使用颜色算法 (使用样本的方式)
                # 将图片进行处理
                roi_color_hsv = handle_img(roi_color)
                roi_color_hist = create_rgb_hist(roi_color_hsv)
                # 进行比较
                compare_hist = hist_compare(hist_sample, roi_color_hist)
                if self.Similarity_Degree_Color_Verb.get() is None:
                    compare_get_color = 1 / 100
                else:
                    compare_get_color = self.Similarity_Degree_Color_Verb.get() / 100
                if compare_hist > compare_get_color and count - max_position > self.Video_FPS * Min_No_Deal_Time:
                    if compare_hist > max_n:
                        max_n = compare_hist
                    else:
                        max_position = count
                        max_n = 0
                        self.time_and_strength.append(max_position)  # 将数据存入列表
                        show_result = True
                if show_result:
                    print("展示(颜色) ", count, compare_hist)
                    # 如果关闭视频显示
                    cv.rectangle(image_show, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])),
                                 color=show_color,
                                 thickness=-1)
                    show_result = False

            elif self.radio_box_verb.get() == 3:  # 使用NCC算法
                compare_ncc = calculate_correlation_coefficient_2(cv.cvtColor(self.Sample_ROI, cv.COLOR_BGR2GRAY),
                                                                  roi_pre)
                if self.Similarity_Degree_NCC_Verb.get() is None:
                    compare_get_NCC = 1 / 100
                else:
                    compare_get_NCC = self.Similarity_Degree_NCC_Verb.get() / 100
                if compare_ncc > compare_get_NCC and count - max_position > self.Video_FPS * Min_No_Deal_Time:
                    if compare_ncc > max_n:
                        max_n = compare_ncc
                    else:
                        max_position = count
                        max_n = 0
                        self.time_and_strength.append(max_position)  # 将数据存入列表
                        show_result = True
                if show_result:
                    print("展示(NCC) ", count, compare_ncc)
                    # 如果关闭视频显示
                    cv.rectangle(image_show, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])),
                                 color=show_color,
                                 thickness=-1)
                    show_result = False
            elif self.radio_box_verb.get() == 4:    # 使用SSIM算法
                compare_SSIM = compare_picture_by_SSIM(roi_color, self.Sample_ROI)
                if self.Similarity_Degree_SSIM_Verb.get() is None:
                    compare_get_SSIM = 1/100
                else:
                    compare_get_SSIM = self.Similarity_Degree_SSIM_Verb.get() / 100

                if compare_SSIM > compare_get_SSIM and count - max_position > self.Video_FPS * Min_No_Deal_Time:
                    if compare_SSIM > max_n:
                        max_n = compare_SSIM
                    else:
                        max_position = count
                        max_n = 0
                        self.time_and_strength.append(max_position)  # 将数据存入列表
                        show_result = True
                if show_result:
                    print("展示(SSIM) ", count, compare_SSIM)
                    # 如果关闭视频显示
                    cv.rectangle(image_show, (int(rect[0]), int(rect[1])), (int(rect[2]), int(rect[3])),
                                 color=show_color,
                                 thickness=-1)
                    show_result = False

            if show_video:
                cv.imshow("test", image_show)
                wk = cv.waitKey(1)
            else:
                cv.imshow("test", image_show)
                wk = cv.waitKey(10)

            # 相关播放控制
            # 按键值  & 0xFF是一个二进制AND操作 返回一个不是单字节的代码
            keycode = wk & 0xff
            # 空格键暂停
            if keycode == ord(" "):
                if not self.Video_Is_Pause:
                    self.Video_Is_Pause = True
                    while self.Video_Is_Pause:  # 如果没按下空格，继续阻塞
                        st = cv.waitKey(0)
                        keycode1 = st & 0xff
                        if keycode1 == ord(" "):
                            self.Video_Is_Pause = False
                        if keycode1 == 27:  # 避免卡死ESC退出
                            keycode = 27
                            break
                        # 按a开始截图并进入选择框模式
                        if keycode1 == ord('A'):
                            rect = Mouse_Event.draw_image_rectangle_on_mouse(image_show)
                            print(rect)
                            self.Sample_ROI = image_show[int(rect[1]):int(rect[3]), int(rect[0]):int(rect[2])]
                            print("修改截图")

                        if cv.getWindowProperty('test', cv.WND_PROP_VISIBLE) < 1:  # 当窗口关闭时为-1，显示时为0
                            print("窗口全部关闭(暂停)")
                            break
                    self.Video_Is_Pause = False
            # esc键退出
            if keycode == 27:
                print("退出播放! ")
                break
            # Q键加速 S键恢复
            if keycode == ord('Q'):
                print("加速播放")
                show_video = True
            if keycode == ord('S'):
                print("恢复原来速率")
                show_video = False

            # 按a开始截图并进入选择框模式
            if keycode == ord('A'):
                rect = Mouse_Event.draw_image_rectangle_on_mouse(image_show)
                print(rect)
                self.Sample_ROI = image_show[int(rect[1]):int(rect[3]), int(rect[0]):int(rect[2])]
                print("修改截图")

            if cv.getWindowProperty('test', cv.WND_PROP_VISIBLE) < 1:  # 当窗口关闭时为-1，显示时为0
                print("窗口全部关闭(运行)")
                break
        # 释放实例
        cap.release()
        # 销毁窗口
        # 如果选中矩形框
        cv.destroyAllWindows()

        # 将数据保存
        # fp = open('data.txt', 'w')
        # for i in range(len(self.time_and_strength)):
        #     fp.write(str(self.time_and_strength))
        #     fp.write('\n')
        # 提供插值法，将原有节点扩充
        if self.Add_New_Point:
            new_array = []
            Point_Len = len(self.time_and_strength)
            for i in range(Point_Len):

                if i + 1 >= Point_Len:
                    new_array.append(self.time_and_strength[i])
                    break
                new_array.append(self.time_and_strength[i])
                new_array.append(int((self.time_and_strength[i] + self.time_and_strength[i + 1]) / 2))
            self.time_and_strength = new_array

        # 开始进行格式转换
        # 打开文件 写入开头
        print("开始进行格式转换")
        self.file_output_stream.write("{\"actions\":[")
        duration = int(self.Video_Total_Frame / self.Video_FPS)
        # 开始根据点位生成强度
        Point_Len = len(self.time_and_strength)
        Time_Left = 0
        Time_Right = 0
        Strength_Left = 0
        Strength_Right = 0
        strength_array = []
        # 初始化 强度数组
        if self.Strength_Mode_Verb == 1:  # 使用随机生成强度
            strength_max = int(int(self.Analyze_Max_Strength.get()) / 10)
            strength_min = int(int(self.Analyze_Min_Strength.get()) / 10)
            strength = random.randint(strength_min, strength_max)
            strength_array.append(strength)
        else:
            strength_array.append(0)

        for i in range(Point_Len):  # 开始写入随机强度
            if i + 1 >= Point_Len:
                break
            Time_Left = self.time_and_strength[i]
            Time_Right = self.time_and_strength[i + 1]
            Strength_Left = strength_array[i]  # 已经完成自己迭代的功能
            if self.Strength_Mode_Verb == 1:  # 使用随机生成强度        使用时要注意不要超过振幅不要超过最大强度与最小强度差值的一半
                if Time_Right - Time_Left < self.Video_FPS / 4:  # 如果间隔小于帧率的一半，那强度应该在前一个点的附件（正负2）
                    strength_max = int(Strength_Left + self.Strength_Random_verb.get())
                    strength_min = int(Strength_Left - self.Strength_Random_verb.get())
                    strength = random.randint(strength_min, strength_max)  # 随机生成一个附近强度
                    if strength > int(int(self.Analyze_Max_Strength.get()) / 10):
                        strength = int(int(self.Analyze_Max_Strength.get()) / 10) - self.Strength_Random_verb.get()
                    if strength < 0:
                        strength = self.Strength_Random_verb.get()
                else:
                    strength_max = int(int(self.Analyze_Max_Strength.get()) / 10)
                    strength_min = int(int(self.Analyze_Min_Strength.get()) / 10)
                    strength = random.randint(strength_min, strength_max)
                strength_array.append(strength)
            else:
                if Strength_Left == int(self.Analyze_Min_Strength.get()) / 10:
                    strength = int(self.Analyze_Max_Strength.get()) / 10
                else:
                    strength = int(self.Analyze_Min_Strength.get()) / 10
                strength_array.append(strength)
        # 开始将数据写入文件
        print("正在将数据写入文件！")
        for i in range(Point_Len):
            if i + 1 >= Point_Len:
                self.file_output_stream.write(
                    "{\"at\":" + str(int((self.time_and_strength[i] / self.Video_FPS) * 1000)) + ",\"pos\":" + str(
                        int(strength_array[i] * 10)) + "}],"
                )
                break
            self.file_output_stream.write(
                "{\"at\":" + str(int((self.time_and_strength[i] / self.Video_FPS) * 1000)) + ",\"pos\":" + str(
                    int(strength_array[i] * 10)) + "},"
            )

        self.file_output_stream.write(
            "\"inverted\":false,\"metadata\":{\"bookmarks\":[],\"chapters\":[],"
            "\"creator\":\"machine\",\"description\":\"made by machine\",\"duration\":" + str(
                duration) + ",\"license\":"
                            "\"Free\",\"notes\":\"test\",\"performers\":[],\"script_url\":\" \",\"tags\":[],"
                            "\"title\":\"test\",\"type\":\"basic\",\"video_url\":\"\"},\"range\":100,"
                            "\"version\":\"1.0\"}")
        print("数据写入完成")
        self.file_output_stream.close()

    '''随机强度勾选框变量控制'''

    def strength_mode_fun(self):
        if self.checkbox_check.get() == 0:
            self.Strength_Mode_Verb = 0
        else:
            self.Strength_Mode_Verb = 1

    def Add_New_Point_Fun(self):
        if self.Add_New_Point_Verb.get() == 0:
            self.Add_New_Point = False
        else:
            self.Add_New_Point = True


# 灰度相似度比较算法
def light_check_fun(mean1, mean2):
    if mean1 == 0:
        return -1
    return abs(mean2 - mean1) / mean1  # 返回相对于第一个均值来说的变化部分


# 监听线程
def Video_Listen(th):
    while True:
        if not th.is_alive():
            break


# 灰度计算算法
def light_cac_fun(img):
    return np.mean(img)


# 颜色比较算法（相似度）
def create_rgb_hist(image):
    """"创建 RGB 三通道直方图（直方图矩阵）"""
    h, w, c = image.shape
    # 创建一个（16*16*16,1）的初始矩阵，作为直方图矩阵
    # 16*16*16的意思为三通道每通道有16个bins
    rgbhist = np.zeros([16 * 16 * 16, 1], np.float32)
    bsize = 256 / 16
    for row in range(h):
        for col in range(w):
            b = image[row, col, 0]
            g = image[row, col, 1]
            r = image[row, col, 2]
            # 人为构建直方图矩阵的索引，该索引是通过每一个像素点的三通道值进行构建
            index = int(b / bsize) * 16 * 16 + int(g / bsize) * 16 + int(r / bsize)
            # 该处形成的矩阵即为直方图矩阵
            rgbhist[int(index), 0] += 1
    return rgbhist


def hist_compare(hist1, hist2):
    """直方图比较函数"""
    '''# 创建第一幅图的rgb三通道直方图（直方图矩阵）
    hist1 = create_rgb_hist(image1)
    # 创建第二幅图的rgb三通道直方图（直方图矩阵）
    hist2 = create_rgb_hist(image2)'''
    # 进行三种方式的直方图比较
    match2 = cv.compareHist(hist1, hist2, cv.HISTCMP_CORREL)
    return match2


def handle_img(img):
    img = cv.resize(img, (32, 32))
    img = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    img[:, :, 2] = cv.equalizeHist(img[:, :, 2])
    img = cv.cvtColor(img, cv.COLOR_HSV2BGR)
    return img


def pHash(img):
    # 加载并调整图片为32x32灰度图片
    img = cv.resize(img, (32, 32), interpolation=cv.INTER_CUBIC)
    img = img.astype(np.float32)

    # 离散余弦变换
    img = cv.dct(img)
    img = img[0:8, 0:8]
    avg = 0
    hash_str = ''

    # 计算均值
    for i in range(8):
        for j in range(8):
            avg += img[i, j]
    avg = avg / 64

    # 获得hash
    for i in range(8):
        for j in range(8):
            if img[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str


def cmpHash(hash1, hash2):
    n = 0
    if len(hash1) != len(hash2):
        return -1
    for i in range(len(hash1)):
        if hash1[i] != hash2[i]:
            n = n + 1
    return n


# NCC系数计算
def calculate_correlation_coefficient_2(mask_a, mask_b):
    mask_a = cv.resize(mask_a, (32, 32))
    mask_b = cv.resize(mask_b, (32, 32))
    # 对掩膜进行图像增强
    # mask_a = cv.equalizeHist(mask_a)
    # mask_b = cv.equalizeHist(mask_b)
    # 将输入图像转换为浮点型
    image1 = np.float32(mask_a)
    image2 = np.float32(mask_b)
    # 计算输入图像的均值
    mean1 = np.mean(image1)
    mean2 = np.mean(image2)
    # 计算输入图像的标准差
    std1 = np.std(image1)
    std2 = np.std(image2)
    # 减去均值，使输入图像的平均值为0
    image1 -= mean1
    image2 -= mean2
    # 使用FFT计算互相关
    f1 = np.fft.fft2(image1)
    f2 = np.fft.fft2(image2)
    corr = np.fft.ifft2(f1 * np.conj(f2)).real
    # 计算归一化互相关系数
    ncc = corr / (std1 * std2 * image1.size)
    # 仅返回NCC系数
    return np.max(ncc)


# SSIM计算图片相似度（值越大，图片失真越小）
def compare_picture_by_SSIM(mask_a, mask_b):
    mask_a = cv.resize(mask_a, (32, 32))
    mask_b = cv.resize(mask_b, (32, 32))
    ssim = compare_ssim(mask_a, mask_b, channel_axis=2)
    return ssim


if __name__ == "__main__":
    root = Tk()
    # canvas = Canvas(root, width=800, height=600, bg="gray")
    # canvas.pack()
    # img = cv.imread("test.jpg")
    # ShowImage(img, canvas, "fill")
    UI(root)
    root.mainloop()
