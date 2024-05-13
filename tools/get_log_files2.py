import os
import cv2
import shutil

base_source_dir = '/home/huliwen/nerf-pytorch/all_pngs_test200000/'
base_destiny_dir = './all_png_needed_gray'
def copy_file(source_path, destination_path, new_name):
    # 检查目标文件夹是否存在，若不存在则创建
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
 
    # 构建新文件的完整路径
    new_file_path = os.path.join(destination_path, new_name)
 
    # 复制文件
    shutil.copy2(source_path, new_file_path)

png_names = {
    'lego': '004.png',
    'drums':'001.png',
    'chair':'007.png',
    'hotdog':'005.png',
    'ficus':'005.png',
    'materials':'002.png'
}


class_names_for_sort = {
    'blur': '1',
    'blur_gray': '1',
    '':'2',
    'mask_spike':'3',
    'rgb':'4',
    'mask_spike_rgb':'5'
}
def get_pngs(dataset, method):
    base_dir = ''
    type_1 = ''
    if method == 'blur' :
        base_dir = 'logs'
        type_1 = 'blur'
    elif method == 'blur_gray':
        base_dir = 'logs'
        type_1 = 'blur_gray'
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
    # input_name = ''
    output_name = ''
    # if type_1 == 'rgb':
    #     input_name = 'spike_' + dataset + '_rgb'
        
    # elif type_1 == 'blur':
    #     input_name = 'blur_' + dataset
    # elif type_1 == '':
    #     input_name = 'spike_' + dataset
    # input_dir = os.path.join(base_input_dir, os.path.join(input_name, 'val'))
    if type_1 == '':
        output_name = 'blender_paper_' + dataset
    else :
        output_name = 'blender_paper_' + dataset + '_' + type_1
    destiny_dir = os.path.join(base_destiny_dir, dataset)
    base_new_name = class_names_for_sort[method] + '_' + method + '_' + dataset + '_' + type_1 + '_'
    source_dir = os.path.join(base_source_dir, os.path.join(base_dir, os.path.join(output_name, 'testset_200000')))
    for img in os.listdir(source_dir):
        if img == png_names[dataset]:
            new_name = base_new_name + img
            copy_file(os.path.join(source_dir, img), destiny_dir, new_name)


datasets  = ['chair', 'drums', 'ficus', 'hotdog', 'lego','materials']
# datasets = ['lego']




# methods = ['blur', 'rgb', 'mask_spike_rgb', '', 'mask_spike', 'mask', 'mask_rgb','spike', 'spike_rgb']
# methods = ['blur', 'rgb', 'mask_spike_rgb', '', 'mask_spike']
# methods = ['blur', 'rgb', 'mask_spike_rgb']
methods = ['blur_gray', '', 'mask_spike']
for dataset in datasets:
    for method in methods:
        get_pngs(dataset, method)
base_gt_dir = './data/nerf_synthetic'

def add_gt(dataset):
    source_data_dir_name = 'spike_' + dataset + '_rgb'
    source_file = os.path.join(base_gt_dir, os.path.join(source_data_dir_name, 'test/' + gt_names[dataset]))
    print(source_file)
    destiny_dir = os.path.join(base_destiny_dir, dataset)
    print(destiny_dir)
    # copy_file(source_file, destiny_dir, gt_names[dataset])

    gray_img = cv2.cvtColor(cv2.imread(source_file), cv2.COLOR_BGR2GRAY)
    gray_img = (gray_img/ 255.0)**(1/2.2)*255.0
    gray_path = os.path.join(base_destiny_dir, dataset)
    gray_path = os.path.join(gray_path, 'gray_' + gt_names[dataset])
    cv2.imwrite(gray_path, gray_img)
gt_names = {
    'lego': 'r_32.png',
    'drums':'r_8.png',
    'chair':'r_56.png',
    'hotdog':'r_40.png',
    'ficus':'r_40.png',
    'materials':'r_16.png'
}
for dataset in datasets:
    add_gt(dataset)