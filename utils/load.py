import random
from pathlib import Path
from skimage.feature import peak_local_max
import numpy as np
import torch
import cv2
from scipy.ndimage.interpolation import rotate


def local_maxima(img, threshold=100, dist=2):
    assert len(img.shape) == 2
    data = np.zeros((0, 2))
    x = peak_local_max(img, threshold_abs=threshold, min_distance=dist)
    peak_img = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
    for j in range(x.shape[0]):
        peak_img[x[j, 0], x[j, 1]] = 255
    labels, _, _, center = cv2.connectedComponentsWithStats(peak_img)
    for j in range(1, labels):
        data = np.append(data, [[center[j, 0], center[j, 1]]], axis=0).astype(int)
    return data


class CellImageLoad(object):
    def __init__(self, ori_path, gt_path, crop_size=(512, 512)):
        self.ori_paths = ori_path
        self.gt_paths = gt_path
        self.crop_size = crop_size

    def __len__(self):
        return len(self.ori_paths)

    def random_crop_param(self, shape):
        h, w = shape[:2]
        top = np.random.randint(0, h - self.crop_size[0])
        left = np.random.randint(0, w - self.crop_size[1])
        bottom = top + self.crop_size[0]
        right = left + self.crop_size[1]
        return top, bottom, left, right

    def __getitem__(self, data_id):
        img_name = self.ori_paths[data_id]
        img = cv2.imread(str(img_name))
        img = img / img.max()

        gt_name = self.gt_paths[data_id]
        gt = cv2.imread(str(gt_name), 0)

        if gt.max()!=0:
            gt = gt / gt.max()

            
        
        
        # data augumentation
        top, bottom, left, right = self.random_crop_param(img.shape)

        img = img[top:bottom, left:right]
        gt = gt[top:bottom, left:right]

        rand_value = np.random.randint(0, 4)
        img = rotate(img, 90 * rand_value, mode="nearest")
        gt = rotate(gt, 90 * rand_value)

        img = torch.from_numpy(img.astype(np.float32))
        gt = torch.from_numpy(gt.astype(np.float32))

        datas = {"image": img.permute(2, 0, 1), "gt": gt.unsqueeze(0)}

        return datas
