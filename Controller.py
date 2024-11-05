from model import Model
from Viewer import Viewer
import numpy as np
import os

class Controller():

    def __init__(self, user_name, model=None, viewer=None, dir_name = None):
        self.model = model
        self.viewer = viewer
        self.user_name = user_name
        score_fname = user_name+"_scores.txt"
        if os.path.isfile(score_fname) and (os.path.getsize(score_fname)>0):
            with open(score_fname, "r") as f:
                f_name = f.readlines()[-1].split(',')[0]
            files = os.listdir(dir_name)
            files.sort()
            self.cur_file = files.index(f_name+'.nii.gz')
        else:
            # Creates a new file
            with open(score_fname, 'w') as fp:
                pass
            self.cur_file = 0
        self.score_fname = score_fname


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
            self.viewer.disable_next_button()
            score = self.viewer.score_val.get()
            self.viewer.reset_score()
            file_name = files[i].split('.')[0]
            with open(self.score_fname, "a") as f:
                f.write(f"{file_name}, {score}\n")
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
        i = self.cur_file
        if i == 0:
            searching_nifty=True
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
        slice_idx_tx = self.viewer.slice_n_tx.get()
        slice_idx_sg = self.viewer.slice_n_sg.get()
        slice_idx_co = self.viewer.slice_n_co.get()
        #Get all images
        tax_img = self.model.get_transaxial_img()[slice_idx_tx]
        sg_img = self.model.get_saggital_img()[slice_idx_sg]
        co_img = self.model.get_coronal_img()[slice_idx_co]
        shx_img = self.model.get_short_axs_img()[slice_idx_tx]
        hla_img = self.model.get_hla_img()[slice_idx_co]
        vla_img = self.model.get_vla_img()[slice_idx_sg]
        #update viewer images
        self.viewer.update_tax_img(tax_img)
        self.viewer.update_sg_img(sg_img)
        self.viewer.update_co_img(co_img)
        self.viewer.update_shx_img(shx_img)
        self.viewer.update_hla_img(hla_img)
        self.viewer.update_vla_img(vla_img)
