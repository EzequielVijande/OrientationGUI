import numpy as np
import nibabel as nib
import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.ndimage import map_coordinates
from pickle import load

class Model:
    """Encapsulates the logic and operations necessary for loading,
    reorientating and generating slices of a cardiac nifty study in
    different planes.
    """
    def __init__(self):
        return

    def load_study(self, img_path, landmarks_path):
        nifti_obj = nib.load(img_path)
        self.img = np.array(nifti_obj.dataobj)
        self.header = nifti_obj.header
        with open(landmarks_path, 'rb') as f:
            loaded_dict = load(f)
        self.m_valve = loaded_dict['base']
        self.apex = loaded_dict['apex']
        self.rv = loaded_dict['rv']

    def perform_reorientation(self):
        self.compute_rotation_matrix()
        self.reoriented = self.apply_3d_rotation(self.m_valve)

    def compute_rotation_matrix(self):
        """
        Compute the rotation matrix to align the cardiac image to the cardiac axis.
        
        Parameters:
        - mitral_valve: Tuple (x, y, z) coordinates of the mitral valve.
        - apex: Tuple (x, y, z) coordinates of the apex.
        - rv_center: Tuple (x, y, z) coordinates of the center of the right ventricle.
        
        Returns:
        - rotation_matrix: A 3x3 numpy array representing the rotation matrix.
        """
        mitral_valve = self.m_valve
        apex = self.apex
        rv_center = self.rv
        # Compute the vector from mitral valve to apex
        apex_vector = np.array(apex) - np.array(mitral_valve)
        apex_vector = apex_vector / np.linalg.norm(apex_vector)  # Normalize the vector
        
        # Compute the vector from mitral valve to RV center
        rv_vector = np.array(rv_center) - np.array(mitral_valve)
        rv_vector = rv_vector / np.linalg.norm(rv_vector)  # Normalize the vector
        
        # Compute the orthogonal vectors to form the cardiac axis
        normal_vector = np.cross(apex_vector, rv_vector)
        normal_vector = normal_vector / np.linalg.norm(normal_vector)
        
        rv_vector_corrected = np.cross(normal_vector, apex_vector)
        
        # Create the rotation matrix from the orthogonal vectors
        rotation_matrix = np.vstack([rv_vector_corrected, normal_vector, apex_vector])

        xyz_axis = np.vstack([[1,0,0], [0,1,0], [0,0,1]])
        rot_mat_2, _ = R.align_vectors(xyz_axis, rotation_matrix)
        self.rot_mat = rot_mat_2.as_matrix() 
      
    def apply_3d_rotation(self, rotation_center, order=3):
        """
        Apply a 3D rotation to a PyTorch tensor around a specified rotation center.
        
        Parameters:
        - tensor: 3D PyTorch tensor of shape (D, H, W).
        - rotation_matrix: 3x3 numpy array representing the rotation matrix.
        - rotation_center: Tuple (x, y, z) representing the center of rotation.
        
        Returns:
        - rotated_tensor: The rotated 3D tensor.
        """
        rotation_matrix = self.rot_mat
        # Create a grid of coordinates
        W, H, D = self.img.shape
        x, y, z = np.meshgrid(np.arange(W), np.arange(H), np.arange(D), indexing='ij')
        
        # Stack the coordinates and subtract the rotation center
        coordinates = np.stack([x, y, z], axis=-1, dtype=np.float32)
        coordinates -= rotation_center
        
        # Apply the rotation matrix
        rotated_coords = np.matmul(coordinates, rotation_matrix)
        # Add the rotation center back to the coordinates
        rotated_coords += rotation_center

        transposed_grid = rotated_coords.transpose(3,0,1,2) # (3, W, H, D)
        # Separate the transposed grid into a list of 3 arrays, one for each dimension
        coordinates = [transposed_grid[i] for i in range(3)]
        #Perform resampling
        rotated_tensor = map_coordinates(self.img, coordinates, order=order)
        return rotated_tensor

    def get_transaxial_img(self):
        return self.img.transpose((2,1,0))
    def get_saggital_img(self):
        return np.flip(self.img.transpose((0,2,1)), 1)
    def get_coronal_img(self):
        return np.flip(self.img.transpose((1,2,0)), 1)
    def get_short_axs_img(self):
        return np.flip(self.reoriented.transpose((2,1,0)), 2)
    def get_hla_img(self):
        return np.flip(self.reoriented.transpose((1,2,0)), (1,2))
    def get_vla_img(self):
        return self.reoriented.transpose((0,1,2))


# dir_name = ".//dataset//"
# file_name = "10.nii"
# m = Model()
# m.load_study(dir_name+file_name)
