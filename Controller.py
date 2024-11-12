from model import Model
from Viewer import Viewer
import numpy as np
from scipy.ndimage import rotate
import os

MAX_ANGLE = 180
class Controller():

    def __init__(self, user_name, model=None, viewer=None, dir_name = None):
        self.model = model
        self.viewer = viewer
        self.user_name = user_name
        score_fname = user_name+"_scores.txt"
        self.shx_angle = 0
        self.hla_angle = 0
        self.vla_angle = 0
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
        if dir_name is not None:
            files = files = os.listdir(dir_name)
            pkl_counter = 0
            for file in files:
                if file.endswith('.pkl'):
                    pkl_counter = pkl_counter+1
            self.total_studies = pkl_counter


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
        #Update progress
        with open(self.score_fname, "r") as f:
            lines = f.readlines()
        file_id_list = []
        for line in lines:
            file_id_list.append(line.split(',')[0])
        self.viewer.progress_bar.config(text=f'Progress: {1+len(set(file_id_list))}/{self.total_studies}')

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
            file_name = files[i].split('.')[0]
            #Save result
            with open(self.score_fname, "a") as f:
                f.write(f"{file_name}, shx={self.shx_angle}, vla={self.vla_angle}, hla={self.hla_angle}\n")
            #Reset manual calibration angles
            self.shx_angle = 0
            self.vla_angle = 0
            self.hla_angle = 0
            self.viewer.shx_angle_lbl.config(text=f'{self.shx_angle}°')
            self.viewer.hla_angle_lbl.config(text=f'{self.hla_angle}°')
            self.viewer.vla_angle_lbl.config(text=f'{self.vla_angle}°')
            #Load next study
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
        i = self.cur_file
        pkl_counter = 0
        if i == 0:
            searching_nifty=True
            while searching_nifty:
                if files[i].endswith('.nii.gz'):
                    searching_nifty = False
                else:
                    i += 1
        for file in files:
            if file.endswith('.pkl'):
                pkl_counter = pkl_counter+1
        self.total_studies = pkl_counter
        self.load_study(i)
        self.viewer.disable_prev_button()

    def set_model(self, model):
        self.model = model

    def set_viewer(self, viewer):
        self.viewer = viewer

    def update_imgs(self, new_val=None, eps=1e-3):
        new_sat_p = 1-((float(self.viewer.sat_percentage.get())/100.0)-1)**2 #1-(x-1)**2
        #Get slice number
        slice_idx_shx = self.viewer.slice_n_shx.get()
        slice_idx_hla = self.viewer.slice_n_hla.get()
        slice_idx_vla = self.viewer.slice_n_vla.get()
        #Get all images
        shx_img = self.model.get_short_axs_img()
        hla_img = self.model.get_hla_img()
        vla_img = self.model.get_vla_img()
        #Saturate and normalize images
        sat_shx_img = shx_img.clip(max=shx_img.max()*(1.0-new_sat_p))
        sat_hla_img = hla_img.clip(max=hla_img.max()*(1.0-new_sat_p))
        sat_vla_img = vla_img.clip(max=vla_img.max()*(1.0-new_sat_p))
        #update viewer images
        self.viewer.update_shx_img(rotate((sat_shx_img/(sat_shx_img.max()+eps))[slice_idx_shx], self.shx_angle, reshape=False))
        self.viewer.update_hla_img(rotate((sat_hla_img/(sat_hla_img.max()+eps))[slice_idx_hla], self.hla_angle, reshape=False))
        self.viewer.update_vla_img(rotate((sat_vla_img/(sat_vla_img.max()+eps))[slice_idx_vla], self.vla_angle, reshape=False))
    
    def increment_shx_angle(self):
        self.shx_angle = np.clip(self.shx_angle+1, a_min=-MAX_ANGLE, a_max=MAX_ANGLE)
        self.viewer.shx_angle_lbl.config(text=f'{self.shx_angle}°')
        self.update_imgs()

    def increment_hla_angle(self):
        self.hla_angle = np.clip(self.hla_angle+1, a_min=-MAX_ANGLE, a_max=MAX_ANGLE)
        self.viewer.hla_angle_lbl.config(text=f'{self.hla_angle}°')
        self.update_imgs()

    def increment_vla_angle(self):
        self.vla_angle = np.clip(self.vla_angle+1, a_min=-MAX_ANGLE, a_max=MAX_ANGLE)
        self.viewer.vla_angle_lbl.config(text=f'{self.vla_angle}°')
        self.update_imgs()

    def decrement_shx_angle(self):
        self.shx_angle = np.clip(self.shx_angle-1, a_min=-MAX_ANGLE, a_max=MAX_ANGLE)
        self.viewer.shx_angle_lbl.config(text=f'{self.shx_angle}°')
        self.update_imgs()

    def decrement_hla_angle(self):
        self.hla_angle = np.clip(self.hla_angle-1, a_min=-MAX_ANGLE, a_max=MAX_ANGLE)
        self.viewer.hla_angle_lbl.config(text=f'{self.hla_angle}°')
        self.update_imgs()

    def decrement_vla_angle(self):
        self.vla_angle = np.clip(self.vla_angle-1, a_min=-MAX_ANGLE, a_max=MAX_ANGLE)
        self.viewer.vla_angle_lbl.config(text=f'{self.vla_angle}°')
        self.update_imgs()