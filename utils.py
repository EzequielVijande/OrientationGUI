#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 29 10:37:06 2023

@author: Ezequiel Vijande
"""

import numpy as np
import shutil

def copy_and_rename(src_path, dest_path, og_name, new_name):
    # Copy the file
    shutil.copy(src_path, dest_path)

    # Rename the copied file
    new_path = f"{dest_path}/{new_name}"
    shutil.move(f"{dest_path}/{og_name}", new_path)
    
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

def partition_dataset(file_names, train_sz_fraction, r_seed=35):
    if (train_sz_fraction<0)|(train_sz_fraction>1):
        raise ValueError('train_sz_fraction must be a number in the range 0-1.')
    np.random.seed(r_seed)
    train_sz = np.ceil(train_sz_fraction*len(file_names)).astype(np.uint32)
    test_sz = len(file_names)-train_sz
    train_idxs = np.random.choice(range(0,len(file_names)), train_sz, replace=False)
    train_files = file_names[train_idxs]
    test_files = list(set(file_names) - set(train_files))
    return train_files, test_files

def non_zero_mask(x):
    return x.ne(0)
   
def get_model_size(model):
    '''
    Returns the number of parameters in model

    Parameters
    ----------
    model : torch.nn.Module
        Neural network which size is measured

    Returns
    -------
    int number of parameters in model

    '''
    return sum(p.numel() for p in model.parameters())

def unravel_index(index, shape):
    '''
    Converts index of flattened array to index of unflattened array.

    Parameters
    ----------
    index : TYPE
        DESCRIPTION.
    shape : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    out = []
    for dim in reversed(shape):
        out.append(index % dim)
        index = index // dim
    return tuple(reversed(out))
