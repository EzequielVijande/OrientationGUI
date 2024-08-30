import numpy as np
import nibabel as nib
import os

class Model:
    """Encapsulates the logic and operations necessary for loading,
    reorientating and generating slices of a cardiac nifty study in
    different planes.
    """
    def __init__(self):
        return

    def load_study(self, file_name):
        nifti_obj = nib.load(file_name)
        self.img = np.array(nifti_obj.dataobj)
        self.img = (255*(self.img / self.img.max())).astype(np.uint8)
        self.header = nifti_obj.header

    def generate_short_ax_img(self):
        return

    def get_transaxial_img(self):
        return self.img

def anonymize_niftii(nifti_file):
    # Access the header
    header = nifti_file.header

    # Anonymize the header
    header['descrip'] = b''  # Empty string in bytes
    header['aux_file'] = b''
    header['intent_name'] = b''

    # Optionally, anonymize more fields if needed
    header['db_name'] = b''  # Clears database name
    header['session_error'] = 0  # Reset session error
    return header

dir_name = ".//dataset//"
file_name = "10.nii"
m = Model()
m.load_study(dir_name+file_name)
