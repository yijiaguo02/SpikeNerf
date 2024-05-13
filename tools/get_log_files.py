import os
import shutil
 

def copy_file(source, destination):
    shutil.copy(source, destination)


def copy_folder(source_folder, destination_folder):
    try:
        shutil.copytree(source_folder, destination_folder)
        # print("文件夹复制成功！")
    except Exception as e:
        print("文件夹复制失败：", str(e))



def copy_file(source_path, destination_path, new_name):
    # 检查目标文件夹是否存在，若不存在则创建
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
 
    # 构建新文件的完整路径
    new_file_path = os.path.join(destination_path, new_name)
 
    # 复制文件
    shutil.copy2(source_path, new_file_path)


# def solve(png_names)
png_names = {
    'lego': '011.png',
    'drums':'007.png',
    'chair':'008.png',
    'hotdog':'010.png',
    'ficus':'010.png',
    'materials':'000.png'
}

class_names_for_sort = {
    # 'mask': '1',
    # 'spike':'1',

    'blur': '1',
    '':'2',
    'mask_spike':'3',
    'rgb':'4',
    'mask_spike_rgb':'5'
}


skip_keys=('mic')

root_path = './all_pngs_test200000'

destination_root = './all_png_needed2_add'
for dir1 in os.listdir(root_path):
    one_level_file_name = dir1 # like spike_logs_mask
    if one_level_file_name in ['logs', 'spike_logs_mask', 'spike_logs_mask_rgb'] :
        continue
    one_level_path = os.path.join(root_path, dir1) # like     ./all_logs_test200000/spike_logs_mask
    for dir2  in os.listdir(one_level_path):
        two_level_file_name = dir2     # like  blender_paper_chair,  blender_paper_drums
        key = two_level_file_name.split('_')[2]
        if key in skip_keys:
            continue
        two_level_path = os.path.join(one_level_path, dir2)
        two_level_path = os.path.join(two_level_path, os.path.join('testset_200000', png_names[key]))
        
        destination_path = os.path.join(destination_root, key)  #  ./all_png_needed3_mask/chair
        new_name1 = one_level_file_name.split('logs')[-1] # '_mask'

        if len(new_name1) > 0 and new_name1[0] == '_':
            new_name1 = new_name1[1:]
        
        new_name2 = two_level_file_name.split('blender_paper')[-1]
        new_name = new_name1 + new_name2 + '_' +png_names[key]
        print(new_name)
        # if new_name[0] == '_' and new_name.find('rgb') == -1 and new_name.find('blur') == -1:
        #     new_name = '2' + new_name
        # elif new_name.find('mask_spike_rgb')  !=  -1:
        #     new_name = '5_' + new_name
        # elif new_name.find('blur')  !=  -1:
        #     new_name = '1' + new_name
        # elif new_name[0] == '_' and new_name.find('rgb') != -1 :
        #     new_name = '4_' + new_name
        # elif new_name.find('mask_spike') != -1:
        #     new_name = '3_' + new_name
        # print(new_name)

    

        # if new_name.find('mask_rgb')  !=  -1:
            # continue
        # if new_name.find('spike') != -1 and new_name.find('spike_rgb') == -1 and new_name.find('mask_spike') == -1 and new_name.find('mask_spike_rgb') == -1:
        #     continue
        # print(new_name)
    # print('---------------------------------------')
        copy_file(two_level_path, destination_path, new_name)

        # copy_file(two_level_path)
        

