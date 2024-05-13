import os
import torch
import numpy as np
import imageio 
import json
import torch.nn.functional as F
import cv2


trans_t = lambda t : torch.Tensor([
    [1,0,0,0],
    [0,1,0,0],
    [0,0,1,t],
    [0,0,0,1]]).float()

rot_phi = lambda phi : torch.Tensor([
    [1,0,0,0],
    [0,np.cos(phi),-np.sin(phi),0],
    [0,np.sin(phi), np.cos(phi),0],
    [0,0,0,1]]).float()

rot_theta = lambda th : torch.Tensor([
    [np.cos(th),0,-np.sin(th),0],
    [0,1,0,0],
    [np.sin(th),0, np.cos(th),0],
    [0,0,0,1]]).float()


def pose_spherical(theta, phi, radius):
    c2w = trans_t(radius)
    c2w = rot_phi(phi/180.*np.pi) @ c2w
    c2w = rot_theta(theta/180.*np.pi) @ c2w
    c2w = torch.Tensor(np.array([[-1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])) @ c2w
    return c2w


def load_blender_data(basedir, half_res=False, testskip=1):
    splits = ['train', 'test']
    metas = {}
    for s in splits:
        with open(os.path.join(basedir, 'transforms_{}.json'.format(s)), 'r') as fp:
            metas[s] = json.load(fp)

    all_imgs = []
    all_poses = []
    counts = [0]
    poses = []
    test_poses = []
    for s in splits:
        meta = metas[s]
        imgs = []
        if s=='train' or testskip==0:
            skip = 1
        else:
            skip = testskip
        countsss=3    
        for frame in meta['frames'][3:len(meta['frames'])-3:skip]:
            fname = os.path.join(basedir, frame['file_path'] + '.png')
            #change
            w=250
            h=400
            alpha_channel = np.ones((w, h)) * 255
            image=imageio.imread(fname)
            img = np.zeros((w, h, 4))
            img[:,:,0] = image[:, :, 0]
            img[:,:,1] = image[:, :, 1]
            img[:,:,2] = image[:, :, 2]
            img[:,:,3] = alpha_channel
            imgs.append(img)
            #end
            if s=='train':
               
                #frames[j]=meta['frames'][countsss+j-3]
                poses.append(np.array([meta['frames'][countsss-2]['transform_matrix'],
                                     meta['frames'][countsss-1]['transform_matrix'],
                                    meta['frames'][countsss]['transform_matrix'],
                                     meta['frames'][countsss+1]['transform_matrix'],
                                      meta['frames'][countsss+2]['transform_matrix']]))
                countsss+=1
            else:
                test_poses.append(np.array(frame['transform_matrix']))
        imgs = (np.array(imgs) / 255.).astype(np.float32) # keep all 4 channels (RGBA)
        
        counts.append(counts[-1] + imgs.shape[0])
        all_imgs.append(imgs)
        #all_poses.append(poses)
    test_poses = np.array(test_poses).astype(np.float32)

    poses = np.array(poses).astype(np.float32)
    i_split = [np.arange(counts[i], counts[i+1]) for i in range(2)]
    
    imgs = np.concatenate(all_imgs, 0)
   # poses = np.concatenate(all_poses, 0)
    
    H, W = imgs[0].shape[:2]
    camera_angle_x = float(meta['camera_angle_x'])
    focal = .5 * W / np.tan(.5 * camera_angle_x)
    
    render_poses = torch.stack([pose_spherical(angle, -30.0, 4.0) for angle in np.linspace(-180,180,40+1)[:-1]], 0)
    
    if half_res:
        H = H//2
        W = W//2
        focal = focal/2.

        imgs_half_res = np.zeros((imgs.shape[0], H, W, 4))
        for i, img in enumerate(imgs):
            imgs_half_res[i] = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
        imgs = imgs_half_res
        # imgs = tf.image.resize_area(imgs, [400, 400]).numpy()
    print('Poseshape:')
    print(poses.shape)    
    return imgs, poses,test_poses, render_poses, [H, W, focal], i_split


