from model import Model
from Viewer import Viewer
import numpy as np

class Controller():
    def __init__(self, model=None, viewer=None):
        self.model = model
        self.viewer = viewer
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
        self.viewer.update_tax_img((255*(tax_img/tax_img.max())).astype(np.uint8))
        self.viewer.update_sg_img((255*(sg_img/sg_img.max())).astype(np.uint8))
        self.viewer.update_co_img((255*(co_img/co_img.max())).astype(np.uint8))
        self.viewer.update_shx_img((255*(shx_img/shx_img.max())).astype(np.uint8))
        self.viewer.update_hla_img((255*(hla_img/hla_img.max())).astype(np.uint8))
        self.viewer.update_vla_img((255*(vla_img/vla_img.max())).astype(np.uint8))
