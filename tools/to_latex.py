import pandas as pd
import os
# df = pd.read_csv('./test_logfile/all_sheet_gray.csv')

# lines = ['Method|Metrics', 'mask_spike_rgb', 'mask_rgb']
# lines = ['Method|Metrics', 'mask_spike_rgb', 'spike_rgb']
# # print(df.index)
# print(df)

# df.to_latex('label_latex.tex', index=False)
root = '/home/huliwen/nerf-pytorch/test_logfile2'
dirs = os.listdir('/home/huliwen/nerf-pytorch/test_logfile2')
print(dirs)
for file in dirs:
    # import pdb; pdb.set_trace()
    path = os.path.join(root, file)
    df = pd.read_csv(path)
    l_file = file + '.tex'

    # print(path)
    with open(os.path.join(root, l_file), 'w') as f:
        f.write(df.to_latex(index=False))