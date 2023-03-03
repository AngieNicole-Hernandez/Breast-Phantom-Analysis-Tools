import re
import os
import gzip
import shutil
import numpy as np
import SimpleITK as sitk
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from oriented_model import model2_a
from voxelized_volume import load_itk
from gaussian_models import gauss_3ds

#---------cantidades necesarias------

P      = 700000000 #cantidad de voxeles a modificar con gauss

sigmax = 700    # definimos un sigma, arbitrario por ahora
sigmay = 700
sigmaz = 700

Q      = 1000   #elemento diagonal de la matriz de corelación del modelo orientado

ending = 17     #Final del nombre del phantom modificado

#------------------------------------

path = './phantoms/'
dest_dir = './modified_phantoms/'

files = os.listdir(path)

for file in files:
    if file.startswith("pc_") and file.endswith("_crop.mhd"):
        
        #se carga el phantom
        phantom_mean, origen, espaciamiento = load_itk(path + file)
        
        #a buscar el mhd correspondiente para hallar un punto aleatorio como mean
        s = file
        #se obtiene la semilla que necesitamos
        seed = re.search('pc_(.*)_crop.mhd', s)
        #se abre el mhd
        mhd_info = open(path + file)
        list_of_lines = mhd_info.readlines()
        #se lee el tamaño del phantom
        a, b, z1, y1, x1 = list_of_lines[9].split()
        mhd_info.close()
        
        #se modifica el phantom con el modelo orientado
        modified_phantom, mux, muy, muz = model2_a(phantom_mean, Q)
        
        #se modifica el phantom con el modelo gaussiano
        modified_phantom = gauss_3ds(mux, muy, muz, sigmax, sigmay, sigmaz, x1, y1, z1, P, modified_phantom)
            
        #guardo el phantom, esto consiste de primero guardarlo como .raw
        modified_phantom.tofile(dest_dir + 'pc_' + seed.group(1)[:-2] + str(ending) + '_crop.raw')
            
        #y luego comprimirlo en .gz
        with open(dest_dir + 'pc_' + seed.group(1)[:-2] + str(ending) + '_crop.raw', 'rb') as f_in:
            with gzip.open(dest_dir + 'pc_' + seed.group(1)[:-2] + str(ending) + '_crop.raw.gz', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        #se elimina el .raw (es muy pesado)
        os.remove(dest_dir + 'pc_' + seed.group(1)[:-2] + str(ending) + '_crop.raw')
 
        #ahora el mhd, que hay que modificar por dentro
        a_file = open(path + file, "r")
        list_of_lines = a_file.readlines()
        list_of_lines[13] = "ElementDataFile = pc_" + seed.group(1)[:-2] + str(ending) + "_crop.raw\n"

        other_file = open(dest_dir + "pc_" + seed.group(1)[:-2] + str(ending) + "_crop.mhd", "w")
        other_file.writelines(list_of_lines)

        a_file.close()
        other_file.close()
