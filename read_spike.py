import numpy as np
import argparse
import math
import struct
import cv2  # 利用opencv读取图像
from PIL import Image
import copy
import torch
def read(pre = "", c = 400, r = 250, tot = 1000, is_lego = 1, suff_id = "1"):
    if is_lego == 1:
        binfile=open(pre + "lego_400_250" + ".dat",'rb')
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
    #return img[:,:,0:frame], frame, interval[:,:,0:frame] #返回有效帧数对应的脉冲数据和有效帧数
    #f = open(out_filepath + "lego_400x250_360.dat", 'wb')
    print(img.shape)
    out_filepath="/home/huliwen/nerfdata/nerf/lego/train/spike/0/"
    for i in range(0, frame + 1,20):
        if i+20>frame:
            break
        pos = 0
        h=r
        w=c
        accumulator = np.zeros((h, w))
        f = open(out_filepath +str(i%20).zfill(3) + ".dat", 'wb')
        for j in range(i,i+19):
            for a in range(h):
                for b in range(w):
                    #print(b)
                    #print(img[a][b])
                    threshold=1
                    accumulator[a][b] += img[a][b][j]
                    if accumulator[a][b] >= threshold:
                        accumulator[a][b] -= threshold
                        byte = byte | (1 << (pos))
                    pos += 1
                    #print(i)
                    if pos == 8:
                        pos = 0
                        temp = struct.pack('B', byte)
                        #print(byte)
                        #print(struct.unpack('B', temp))
                        byte = 0
                        f.write(temp)
        if pos != 0:
            pos = 0
            temp = struct.pack('B', byte)
            byte = 0
            f.write(temp)
    f.close()
    return
if __name__ == '__main__':
    read("/home/huliwen/nerfdata/nerf/lego/train/spike/",400,250,100,1,'1')
    
