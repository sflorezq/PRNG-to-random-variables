from scipy.stats import poisson
import numpy as np
import math
def binomial(numeros,n,theta):
    var_binomial = []
    exitos,i,flag = 0,1,0
    for num in numeros:
        if(num<theta):
            exitos +=1
        if(i == n):
            var_binomial.append(exitos)
            flag = 1
        if(flag != 0):
            exitos,i,flag = 0,1,0
        else:
            i+=1
    return var_binomial

def exponencial(media,numeros):
    var_exponencial = []
    for num in numeros:
        var_exponencial.append(-media*math.log(num))
    return var_exponencial

def uniforme(lim_inferior,lim_superior,numeros):
    var_uniforme = []
    for num in numeros:
        var_uniforme.append(lim_inferior+(lim_superior-lim_inferior)*num)
    return var_uniforme

def poisson_distr(lam,numeros):
    # Valores discretos para los que quieres calcular la probabilidad
    x = np.arange(0, 11)

    # Probabilidades teóricas
    acumulado = poisson.cdf(x, mu=lam)
    #print(acumulado)
    '''
    for xi, pi in zip(x, acumulado):
        print(f"P(X={xi}) = {pi:.4f}")
    '''

    var_poisson = []
    for num in numeros:
        for xi,pi in zip(x, acumulado):
            if(num<pi):
                var_poisson.append(xi)
                break
    '''
    for x in var_poisson:
        print(x)
    '''
    
    return var_poisson

def normal(media,desv,numeros):
    var_normal = []
    i, suma = 0,0
    for num in numeros:
        if(i<12):
            suma += num
            i += 1
        else:
            var_normal.append(media+desv*(suma-6))
            i,suma=0,0
    return var_normal

def z1(u):
    return math.sqrt(-2*math.log(u[0]))*math.cos(2*math.pi*u[1])

def z2(u):
    return math.sqrt(-2*math.log(u[0]))*math.sin(2*math.pi*u[1])

def box_muller(media,desv,numeros):
    var_box_muller = []
    i = 0
    u = []
    for num in numeros:
        if(i<2):
            u.append(num)
            i += 1
        else:
            var_box_muller.append(media+desv*z1(u))
            var_box_muller.append(media+desv*z2(u))
            u.clear()
            i = 0
    return var_box_muller