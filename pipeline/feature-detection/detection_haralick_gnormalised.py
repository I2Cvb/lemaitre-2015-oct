#title           :test_extraction_haralick_gnormalised.py
#description     :This will create a header for a python script.
#author          :Guillaume Lemaitre
#date            :2015/04/20
#version         :0.1
#notes           :
#python_version  :2.7.6  
#==============================================================================

# Import the needed libraries
# Matplotlib library
import matplotlib.pyplot as plt
# Numpy libreary
import numpy as np
# OS library
import os
from os.path import join
# SYS library
import sys

# Our module to read DCM volume from a serie of DCM
from protoclass.tool.dicom_manip import OpenVolumeNumpy
# Our module to find the extremum for across all the patients
from protoclass.tool.dicom_manip import FindExtremumDataSet
# Our module to extract Haralick feature maps
from protoclass.extraction.texture_analysis import HaralickMapExtraction

# Give the path to a patient
#path_to_data = '/work/le2i/gu5306le/experiments'
#path_to_data = '/home/lemaitre/Documents/Data/experiments'
path_patients = sys.argv[1]
path_t2w = 'gaussian_norm/volume_gnorm.npy'
path_haralick = 'haralick_gnorm'

#################################################################################
## FIND EXTREMUM FOR THE DIFFERENT PATIENTS

range_dataset_float = FindExtremumDataSet(path_patients, modality=path_t2w)

# Build the path of the current patient
path_patient = sys.argv[2]
path_dcm = join(path_patient, path_t2w)
print 'Reading data from the directory {}'.format(path_dcm)

# Read a volume
volume = OpenVolumeNumpy(path_dcm)

#################################################################################
### 2D volume

# Define the parameters for glcm
### Window size
tp_win_size = (9,9)
### Number of gray levels
tp_n_gray_levels = 64

# Create the ouput list
patient_maps = []

# Go through each slice of the volume
for sl in range(volume.shape[2]):
    ### Compute the Haralick maps
    patient_maps.append(HaralickMapExtraction(volume[:, :, sl], 
                                              win_size=tp_win_size, 
                                              n_gray_levels=tp_n_gray_levels, 
                                              gray_limits=range_dataset_float))

# Create a directory if not existing
path_haralick_saving = join(path_patient, path_haralick)
if not os.path.exists(path_haralick_saving):
    os.makedirs(path_haralick_saving)

# Convert the maps list to array
patient_maps = np.array(patient_maps)

# Roll the first axis to obtain [orientation][stats][y,x,z]
patient_maps = np.rollaxis(patient_maps, 0, 5)

# Save a volume for each orientation and stats
n_orientations = 4
n_statistics = 13
for o in range(n_orientations):
    for s in range(n_statistics):
        # Save the current volume
        filename = join(path_haralick_saving, 'volume_' + str(o) + '_' + str(s) + '.npy')
        np.save(filename, patient_maps[o][s][:, :, :])
            
