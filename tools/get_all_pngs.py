import os
import shutil

def copy_folder(source_folder, destination_folder):
    try:
        shutil.copytree(source_folder, destination_folder)
        # print("文件夹复制成功！")
    except Exception as e:
        print("文件夹复制失败：", str(e))

root_path = './'
for dir in os.listdir(root_path):
    if not os.path.isdir(os.path.join(root_path, dir)):
        continue
    if dir.find('logs') == -1:
        continue
    if dir == 'all_logs_mask_test200000' or dir == 'all_logs_test200000':
        continue
    else:
        # ./logs/
        one_level_path = os.path.join(root_path, dir)
        for sub_dir in os.listdir(one_level_path):
            two_level_path = os.path.join(one_level_path, sub_dir)
            for  sub_sub_dir in os.listdir(two_level_path):
                three_level_path =  os.path.join(two_level_path, sub_sub_dir)
                if os.path.isdir(three_level_path) and sub_sub_dir =='testset_200000':
                    # print(three_level_path.split('./')[-1])
                    destination_folder = os.path.join('./all_pngs_test200000',  three_level_path.split('./')[-1])
                    # print(destination_folder)
                    copy_folder(three_level_path,  destination_folder)
                    # print(three_level_path)
        