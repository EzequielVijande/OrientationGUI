from model import Model
from Viewer import Viewer
import numpy as np
import os

class Controller():

    def __init__(self, model=None, viewer=None, dir_name = None):
        self.model = model
        self.viewer = viewer
        if dir_name is not None:
            self.set_dir(dir_name)

    def load_study(self, index):
        self.cur_file = index
        files = os.listdir(self.working_dir)
        files.sort()
        file_name = files[index].split('.')[0]
        img_path = self.working_dir+'//'+file_name+'.nii.gz'
        landmark_path = self.working_dir+'//'+file_name+'.pkl'
        self.model.load_study(img_path, landmark_path)
        self.model.perform_reorientation()
        self.update_imgs()

    def next_study(self):
        files = os.listdir(self.working_dir)
        files.sort()
        searching_nifty=True
        i=self.cur_file+1
        while searching_nifty:
            if i < len(files):
                if files[i].endswith('.nii.gz'):
                    searching_nifty = False
                else:
                    i += 1
            else:
                break
        if i < len(files):
            self.load_study(i)
            self.viewer.enable_prev_button()
        else:
            self.viewer.disable_next_button()

    def prev_study(self):
        files = os.listdir(self.working_dir)
        files.sort()
        searching_nifty=True
        i=self.cur_file-1
        while searching_nifty:
            if i >= 0:
                if files[i].endswith('.nii.gz'):
                    searching_nifty = False
                else:
                    i -= 1
            else:
                break
        if i >= 0:
            self.load_study(i)
            self.viewer.enable_next_button()
        else:
            self.viewer.disable_prev_button()

    def set_dir(self, dir_name):
        self.working_dir = dir_name
        files = os.listdir(dir_name)
        files.sort()
        searching_nifty=True
        i=0
        while searching_nifty:
            if files[i].endswith('.nii.gz'):
                searching_nifty = False
            else:
                i += 1
        self.load_study(i)
        self.viewer.disable_prev_button()

    def set_model(self, model):
        self.model = model

    def set_viewer(self, viewer):
        self.viewer = viewer

    def update_imgs(self, new_val=None):
        slice_idx = self.viewer.slice_n.get()
        #Get all images
        tax_img = self.model.get_transaxial_img()[slice_idx]
        sg_img = self.model.get_saggital_img()[slice_idx]
        co_img = self.model.get_coronal_img()[slice_idx]
        shx_img = self.model.get_short_axs_img()[slice_idx]
        hla_img = self.model.get_hla_img()[slice_idx]
        vla_img = self.model.get_vla_img()[slice_idx]
        #update viewer images
        self.viewer.update_tax_img(tax_img)
        self.viewer.update_sg_img(sg_img)
        self.viewer.update_co_img(co_img)
        self.viewer.update_shx_img(shx_img)
        self.viewer.update_hla_img(hla_img)
        self.viewer.update_vla_img(vla_img)
