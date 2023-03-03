import random 
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

def model2_a(phantom, sig):
    
    #se buscan las posiciones de los ductos, porque para ponerse buscar voxeles random hasta que caiga en
    #uno de ducto...
    coords = np.where(phantom == 125)
    
    #se selecciona un o de manera aleatoria
    indice =  np.random.randint(0, high= 2 * len(coords[0]) / 3, size=1)
    
    print(indice)
    
    i1 = coords[0][indice]
    i2 = coords[1][indice]
    i3 = coords[2][indice]
    
    indices = np.transpose([coords[0],coords[1],coords[2]])
    
    #mean de la distribución
    me = np.array([np.int(i1), np.int(i2), np.int(i3)])
    
    #matriz de covarianza 
    sigma = sig / np.sqrt(2)

    covar = np.array([[sigma**2, 0.0, 0.0],
                [0.0, sigma**2, 0.0],
                [0.0, 0.0, sigma**2]])
    
    #se seleccionan qué voxeles, de los correspondientes a ductos, se cambiarán, de acuerdo a 
    #una dist de prob normal.
    
    #se define la distribución
    mul = multivariate_normal(mean=me, cov=covar)
    
    #la probabilidad de las posiciones
    y = mul.pdf(indices)
    
    #los valores de y son muy pequeños porque es una función muy muy expandida en el espacio
    
    #un arreglo de probabilidades aleaotrias para comparar
    prob = np.random.uniform(0, max(y),len(y))

    #comparando las probabilidades de las posiciones, con las aleatorias, para decidir qué cambiar
    comparison = prob < y

    #reemplacing where comparison is tru for 200
    phantom[coords[0][comparison],coords[1][comparison],coords[2][comparison]] = 200 

    #devuelve el phantom modificado
    return phantom, i1, i2, i3