import numpy as np
np.set_printoptions(threshold=np.inf)
import argparse
import math
import scipy
import struct
from scipy import integrate
import cv2  # 利用opencv读取图像
import matplotlib.pyplot as plt 
from PIL import Image
import torch
import copy
#w，h is resolution of image，frame_tot is total number of images，file_name is the directory of image
def get_spike(img, ret, w = 400, h = 250, threshold = 256):
    accumulator = ret
    byte = 0
    pos = 0
    #f = open(out_filepath + "test.dat", 'wb')
    #print(i)
    #num = str(i).zfill(4) #自动补0 总共补成到5位
    #img_str = in_filepath + num + ".png"
    #print(img_str)
    #img = np.array(img.convert('L').resize((w, h),Image.ANTIALIAS))
    #img.show()
    out_img=torch.zeros((1024,1))
    #print(img.shape)
    rgb2grey = torch.tensor([0.299, 0.587, 0.114])
    img=torch.mv(img, rgb2grey) * 255
    #img1=img.cpu().detach().numpy()
    #print(img1)
    #print(img.size())
    for a in range(1024):
        for b in range(1):
            #print(b)
            #print(img[a][b])
            accumulator[a] += img[a]
            if accumulator[a] >= threshold:
                accumulator[a] -= threshold
                out_img[a]=1
    return torch.tensor(out_img),torch.tensor(accumulator)
#get_spike("D:\\lwhu\\gt\FlowDataset\\cook\\", "D:\\lwhu\\gt\FlowDataset\\cook\\", 800, 500, 400, 0, 4000)
"""
for i in range(100):
    file = "D:\\lwhu\\gt\FlowDataset\\pretrain_quick\\" + str(i) + "\\"
    print(i)
    get_spike(file, file, 800, 500, 400, 0, 500)
    """
"""if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", "--width")
    parser.add_argument("-H", "--height")
    parser.add_argument("-phi", "--threshold")
    parser.add_argument("--frame_tot")
    parser.add_argument("--file_name")
    args = parser.parse_args()
    get_spike(args.W, args.H, args.phi, args.frame_tot, args.file_name)
"""