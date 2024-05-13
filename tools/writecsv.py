import os

import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity
from skimage.metrics import peak_signal_noise_ratio

import warnings
warnings.filterwarnings('ignore')

'''
五种方法 blur, 
数据集, 暂时5个

'''
base_input_dir = '/home/huliwen/nerf-pytorch/data/nerf_synthetic/'
base_output_dir = '/home/huliwen/nerf-pytorch/all_pngs_test200000/'
def test_dataset(dataset, method):
    '''
    method: blur', 'rgb', 'mask_spike_rgb',  ''  , 'mask_spike
    base_dir: like logs, spike_logs_mask...
    dataset: like chair, drums, 
    type_1: like rgb, blur,  ''
    '''
    base_dir = ''
    type_1 = ''
    if method == 'blur' :
        base_dir = 'logs'
        type_1 = 'blur'
    elif method == 'rgb':
        base_dir = 'logs'
        type_1 = 'rgb'
    elif method == 'mask_spike_rgb':
        base_dir = 'spike_logs_mask_spike_rgb'
        type_1 = 'rgb'
    elif method == '':
        base_dir = 'logs'
        type_1 = ''
    elif method == 'mask_spike':
        base_dir = 'spike_logs_mask_spike'
        type_1 = ''
    elif method == 'mask':
        base_dir = 'spike_logs_mask'
        type_1 = ''
    elif method == 'mask_rgb':
        base_dir = 'spike_logs_mask_rgb'
        type_1 = 'rgb'
    elif method == 'spike':
        base_dir = 'spike_logs_spike'
        type_1 = ''
    elif method == 'spike_rgb':
        base_dir = 'spike_logs_spike_rgb'
        type_1 = 'rgb'
    # base_dir = 
    # type = 
    input_name = ''
    output_name = ''
    if type_1 == 'rgb':
        input_name = 'spike_' + dataset + '_rgb'
        
    elif type_1 == 'blur':
        input_name = 'blur_' + dataset
    elif type_1 == '':
        input_name = 'spike_' + dataset
    input_dir = os.path.join(base_input_dir, os.path.join(input_name, 'val'))
    if type_1 == '':
        output_name = 'blender_paper_' + dataset
    else :
        output_name = 'blender_paper_' + dataset + '_' + type_1
    
    output_dir = os.path.join(base_output_dir, os.path.join(base_dir, os.path.join(output_name, 'testset_200000')))
    print(dataset, "--", method)
    print(input_dir)
    print(output_dir)

    # input_dir = '/home/huliwen/nerf-pytorch/data/nerf_synthetic/spike_hotdog_rgb/test/'
    # output_dir = '/home/huliwen/nerf-pytorch/all_logs_test200000/logs/blender_paper_hotdog_blur/testset_200000'
    SSIM_list = []
    PSNR_LIST = []
    clear_img_path = input_dir  # 清晰图像文件夹路径
    hazy_img_path = output_dir  # 待去雾图像文件夹路径
    clear_img_names = os.listdir(clear_img_path) # 获取所有的清晰图像文件名
    hazy_img_names=os.listdir(hazy_img_path)
    # 遍历清晰图像文件名列表，找到对应的待去雾图像文件名
    if type_1 == 'rgb' or type_1 == 'blur':
        needgamma=False
    else:
        needgamma=True
    count=0
    for i in range(len(hazy_img_names)):
        clear_img = cv2.imread(os.path.join(clear_img_path, "r_"+str(count)+".png"))#,cv2.IMREAD_GRAYSCALE)
        count=count+8
        print(hazy_img_names[i])
        hazy_img = cv2.imread(os.path.join(hazy_img_path, str(i).zfill(3)+".png"))#,cv2.IMREAD_GRAYSCALE)
        if needgamma:
            clear_img = cv2.cvtColor(clear_img, cv2.COLOR_BGR2GRAY)
            hazy_img = cv2.cvtColor(hazy_img, cv2.COLOR_BGR2GRAY)
            hazy_img=(hazy_img/ 255.0)**(2.2)*255.0
        hazy_mean=cv2.mean(hazy_img)[0]
        clear_mean=cv2.mean(clear_img)[0]
        hazy_img=hazy_img*clear_mean/hazy_mean
        if clear_img.shape[0] != hazy_img.shape[0] or clear_img.shape[1] != hazy_img.shape[1]:  
	        pil_img = Image.fromarray(hazy_img) 
	        pil_img = pil_img.resize((clear_img.shape[1], clear_img.shape[0])) # 和clear_img的宽和高保持一致    
	        hazy_img = np.array(pil_img)    
        # cv2.imwrite('./test_logfile/lego_pngs/00' + str(i) + '.png', hazy_img)
        # png_dir = './test_logfile/lego_pngs_004/'
        # # if method == '':
        # #     png_2_dir = os.path.join(png_dir, 'nerf')
        # # else:
        # #     png_2_dir = os.path.join(png_dir, method)
        # if not os.path.exists(png_dir):
        #     os.makedirs(png_dir)
        # test_dir = png_dir + 'test_'
        # if i == 4:
        #     cv2.imwrite(png_dir + method + '_' + ('00' + str(i) + '.png'), hazy_img)
        #     cv2.imwrite(test_dir + method + '_' + ('00' + str(i) + '.png'), clear_img)
        # 计算PSNR
        # PSNR越大，代表着图像质量越好。
        PSNR = peak_signal_noise_ratio(clear_img, hazy_img)
        print(i+1, 'PSNR: ', PSNR)
        PSNR_LIST.append(PSNR)  

        print(clear_img.shape)
        print(hazy_img.shape)
        # 计算SSIM
        SSIM = structural_similarity(clear_img, hazy_img, multichannel=True)
        print(i+1, 'SSIM: ', SSIM)
        SSIM_list.append(SSIM)

    print("average SSIM", sum(SSIM_list)/ len(SSIM_list))
    print("average PSNR", sum(PSNR_LIST)/ len(PSNR_LIST))

    res_ssim = sum(SSIM_list)/ len(SSIM_list)
    res_psnr = sum(PSNR_LIST)/ len(PSNR_LIST)
    # print("average SSIM", sum(SSIM_list)/ len(SSIM_list))
    # print("average PSNR", sum(PSNR_LIST)/ len(PSNR_LIST))
    return res_ssim, res_psnr


'''
每一个数据集，都有
blur,  rgb,  mask_spike_rgb,  '',  mask_spike
'''
datasets  = ['chair', 'drums', 'ficus', 'hotdog', 'lego','materials']
# datasets = ['lego']

methods = ['blur', 'rgb', 'mask_spike_rgb', '', 'mask_spike', 'mask', 'mask_rgb','spike', 'spike_rgb']
out_sheet_file = './test_logfile/all_sheet6.csv'
# out_sheet_file = './test_logs/all_sheet2.log'

with open(out_sheet_file, 'w+') as f:
    f.write('\t')
    for dataset in datasets :
        f.write(dataset + '\t')
    f.write('avg')
    f.write('\n')
    for method in methods:
        all_ssim = 0
        all_psnr = 0
        f.write(method + ' \t')
        for dataset in datasets:
            res_ssim, res_psnr = test_dataset(dataset, method)
            all_ssim += res_ssim
            all_psnr +=res_psnr
            res_ssim = round(res_ssim, 2)
            res_psnr = round(res_psnr, 2)
            f.write(str(res_ssim)+', '+ str(res_psnr)+'|\t')
        avg_ssim = all_ssim/len(datasets)
        avg_psnr = all_psnr/len(datasets)
        avg_ssim = round(avg_ssim, 2)
        avg_psnr = round(avg_psnr, 2)
        f.write(str(avg_ssim)+', '+ str(avg_psnr))
        f.write('\n')
    
# input_dir = '/home/huliwen/nerf-pytorch/data/nerf_synthetic/spike_hotdog_rgb/test/'
# output_dir = '/home/huliwen/nerf-pytorch/all_logs_test200000/logs/blender_paper_hotdog_blur/testset_200000'
# SSIM_list = []
# PSNR_LIST = []
# clear_img_path = input_dir  # 清晰图像文件夹路径
# hazy_img_path = output_dir  # 待去雾图像文件夹路径
# clear_img_names = os.listdir(clear_img_path) # 获取所有的清晰图像文件名
# hazy_img_names=os.listdir(hazy_img_path)
# # 遍历清晰图像文件名列表，找到对应的待去雾图像文件名
# needgamma=False
# count=0
# for i in range(len(hazy_img_names)):
#     clear_img = cv2.imread(os.path.join(clear_img_path, "r_"+str(count)+".png"))#,cv2.IMREAD_GRAYSCALE)
#     count=count+8
#     print(hazy_img_names[i])
#     hazy_img = cv2.imread(os.path.join(hazy_img_path, str(i).zfill(3)+".png"))#,cv2.IMREAD_GRAYSCALE)
#     if needgamma:
#         hazy_img=(hazy_img/ 255.0)**(2.2)*255.0
#     if clear_img.shape[0] != hazy_img.shape[0] or clear_img.shape[1] != hazy_img.shape[1]:
# 	    pil_img = Image.fromarray(hazy_img)
# 	    pil_img = pil_img.resize((clear_img.shape[1], clear_img.shape[0])) # 和clear_img的宽和高保持一致
# 	    hazy_img = np.array(pil_img)

#     # 计算PSNR
#     # PSNR越大，代表着图像质量越好。
#     PSNR = peak_signal_noise_ratio(clear_img, hazy_img)
#     print(i+1, 'PSNR: ', PSNR)
#     PSNR_LIST.append(PSNR)

#     print(clear_img.shape)
#     print(hazy_img.shape)
#     # 计算SSIM
#     SSIM = structural_similarity(clear_img, hazy_img, multichannel=True)
#     print(i+1, 'SSIM: ', SSIM)
#     SSIM_list.append(SSIM)

# print("average SSIM", sum(SSIM_list)/ len(SSIM_list))
# print("average PSNR", sum(PSNR_LIST)/ len(PSNR_LIST))

