#!/usr/bin/env python
# coding: utf-8

# In[4]:

import numpy as np
import random 

def gauss_3d(mu_x, mu_y, mu_z, sigma_x, sigma_y, sigma_z, amount, phantom_array):
    x = np.random.normal(mu_x, sigma_x, amount)
    y = np.random.normal(mu_y, sigma_y, amount)
    z = np.random.normal(mu_z, sigma_z, amount)
    
    scatter_phantom = phantom_array
    
    for i in range(amount):
        if scatter_phantom[int(z[i]),int(x[i]),int(y[i])] != 0:
            scatter_phantom[int(z[i]),int(x[i]),int(y[i])] = 200
        
    return scatter_phantom

def gauss_3ds(mu_x, mu_y, mu_z, sigma_x, sigma_y, sigma_z, x_p, y_p, z_p, amount, phantom_array):
    x = np.random.normal(mu_x, sigma_x, amount)
    y = np.random.normal(mu_y, sigma_y, amount)
    z = np.random.normal(mu_z, sigma_z, amount)
    
    scatter_phantom = np.copy(phantom_array)
    
    for i in range(amount):
        
        #excluding air, pectoral muscle, paddle, vein and artery
        if x[i] < int(x_p) and y[i] < int(y_p) and z[i] < int(z_p)\
        and x[i] > 0 and y[i] > 0 and z[i] > 0\
        and scatter_phantom[int(x[i]),int(y[i]),int(z[i])] != 0\
        and scatter_phantom[int(x[i]),int(y[i]),int(z[i])] != 40\
        and scatter_phantom[int(x[i]),int(y[i]),int(z[i])] != 50\
        and scatter_phantom[int(x[i]),int(y[i]),int(z[i])] != 150\
        and scatter_phantom[int(x[i]),int(y[i]),int(z[i])] != 225:
            scatter_phantom[int(x[i]),int(y[i]),int(z[i])] = 200
        
    return scatter_phantom


# In[ ]:

def random_point_for_double_model(x,y,z,phantom):
    
    '''
    Función que escoge un valor aleatorio en la parte frontal de la mama
    '''
    
    #se inicializa con un valor random
    x_t = np.random.randint(0,int(x))
    y_t = np.random.randint(0,int(y))
    z_t = np.random.randint(int(int(z)/3),int(z))
    
    while phantom[x_t,y_t,z_t] == 0 or phantom[x_t,y_t,z_t] == 40\
    or phantom[x_t,y_t,z_t] == 2 or phantom[x_t,y_t,z_t] == 50:
        
        x_t = np.random.randint(0,int(x))
        y_t = np.random.randint(0,int(int(y)/2))
        z_t = np.random.randint(int(int(z)/3),int(z))

        if phantom[x_t,y_t,z_t] != 0 and phantom[x_t,y_t,z_t] != 40\
        and phantom[x_t,y_t,z_t] != 2 and phantom[x_t,y_t,z_t] != 50:
            break
            
    #si el valor está dentro de la mama, se designa este punto como el mean
    return x_t, y_t, z_t
