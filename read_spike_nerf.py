import numpy as np
import argparse
import math
import struct
import cv2  # 利用opencv读取图像
from PIL import Image
import copy
import torch
def readspike(pre = "", c = 400, r = 250, tot = 1000, is_noise = 1, suff_id = "1"):
    if is_noise == 0:
        binfile=open(pre + "400x250_360" + ".dat",'rb')
    else:
        binfile=open(pre + "no_noise" + ".dat",'rb')
    #binfile=open("D:\\work\\vidar-project\\Cycle(python)\\out\\noise_pattern.dat",'rb')
    frame = 0
    frame_tot = tot
    img = np.zeros((r, c, frame_tot + 10), dtype='uint8')
    pos = 0
    dt = np.zeros((r, c), dtype = int)
    #accu = np.zeros((r, c, frame_tot + 10))
    #tfi = np.zeros((r, c, frame_tot + 10))
    interval = np.ones((r, c, frame_tot + 10), dtype = int) * tot
    #rep = np.zeros((r, c, frame_tot + 10), dtype = int)
    #rep_cnt = np.zeros((r, c), dtype = int)
    #rep_pos = np.zeros((r, c, frame_tot + 10), dtype = int)
    while(1):
        #print("read")
        if frame >= frame_tot:
            break
        a = binfile.read(1)
        if not a:
            break
        real_a = struct.unpack('b', a)[0]
        for i in range(8):
            pan = (real_a & (1 << (i)))
            x = int(pos / c)
            y = pos % c
            dt[x][y] += 1
            if pan != 0:#bug聚集地，因为可能是大于1的orz
                img[x][y][frame] = 1
                #predict = np.linspace(0.0, 1.0, num=int(dt[int(pos / c)][pos % c]) + 1)
                #print(predict.shape)
                #tfi[int(pos / c), (pos % c), (frame - int(dt[int(pos / c)][pos % c]) + 1) : frame + 1] = 1.0 / dt[int(pos / c)][pos % c]
                interval[x, y, (frame - int(dt[x][y]) + 1) : frame + 1] = dt[x][y]
                #rep[x][y][rep_cnt[x][y]] = dt[x][y]
                #rep_pos[x, y, (frame - int(dt[x][y]) + 1) : frame + 1] = rep_cnt[x][y]
                #rep_cnt[x][y] += 1
                #accu[int(pos / c), (pos % c), (frame - int(dt[int(pos / c)][pos % c]) + 1) : frame + 1] = predict[1:]
                #accu[int(pos / c)][(pos % c)][frame] = 0.0
                dt[x][y] = 0
            else:
                img[x][y][frame] = 0
                """
                if frame == 0:
                    rep_pos[x][y][frame] = 0
                else:
                    rep_pos[x][y][frame] = rep_pos[x][y][frame - 1]
                """
            pos += 1
            if pos >= r * c: #进入此条件意味这处理完一个dog的全部积分图，因此必须更新到下一个dog，初始化pos
                pos = 0
                frame += 1
                #print(frame)
                break #这里少加了一个break orz 每一帧采集完后 不够1个字节 会自动补0 所以 这个字节后面的信息是错误的 要从下个字节开始读取
    return img[:,:,0:frame], frame, interval[:,:,0:frame] #返回有效帧数对应的脉冲数据和有效帧数
