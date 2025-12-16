import math
from collections import Counter
from scipy.stats import chi2

def media_test(numeros:list):
    z_expected = 1.96 #confianza de 95%
    media_obtenida = sum(numeros)/len(numeros)
    media_esperada = 0.5
    var_obtenida = 1/12
    z_0 = (media_obtenida-media_esperada)*math.sqrt(len(numeros))/math.sqrt(var_obtenida)
    z_0 = abs(z_0)
    print("Prueba de medias: ")
    if(z_0 < z_expected):
        print("No rechaza")
    else:
        print("Rechaza")

def kolmogorov_smirnoff(numeros:list):
    n = len(numeros)
    estadistico = 1.36/math.sqrt(n)
    numeros.sort()
    acumulado = []
    for i in range(1,n):
        acumulado_esperado = i/len(numeros)
        diferencia_acumulado = acumulado_esperado - numeros[i-1]
        acumulado.append(diferencia_acumulado)
    maximo = max(acumulado)
    print("Prueba de Kolmogorov-smirnoff: ")
    if(maximo < estadistico):
        print("No rechaza")
    else:
        print("Rechaza")

def frequency_test(numeros:list):
    N = len(numeros)
    intervalos = 5
    f_esperada = N/intervalos
    chisquare_observed=0
    chisquare_expected = chi2.ppf(0.95,intervalos-1)
    for i in range(1,intervalos+1):
        l_inf = (i-1)/intervalos
        l_sup = i/intervalos
        f_observada = 0
        for num in numeros:
            if(num < l_sup and num > l_inf):
                f_observada+=1
        chisquare_observed+=(f_observada-f_esperada)**2/f_esperada
            
    print("Prueba de frecuencias: ")
    if(chisquare_observed < chisquare_expected):
        print("No rechaza")
    else:
        print("Rechaza")

def digits(num):
    # Convertir a string con al menos 5 decimales
    num_str = f"{num:.5f}"  # Esto garantiza al menos 5 decimales
    decimales = num_str.split(".")[1][:5]  # Tomar los primeros 5 decimales
    return decimales

def hand_type(cartas):
    """
    Determina la mano de poker según una lista de 5 números (0-9).
    """
    if len(cartas) != 5:
        return "Debes ingresar exactamente 5 números"

    # Contamos las repeticiones
    conteo = Counter(cartas)
    repeticiones = sorted(conteo.values(), reverse=True)

    # Evaluamos la mano
    if repeticiones == [5]:
        return "Quintilla"
    elif repeticiones == [4, 1]:
        return "Poker"
    elif repeticiones == [3, 2]:
        return "Full House"
    elif repeticiones == [3, 1, 1]:
        return "Trío"
    elif repeticiones == [2, 2, 1]:
        return "Doble Par"
    elif repeticiones == [2, 1, 1, 1]:
        return "Par"
    else:
        return "Carta Alta"

def stadistic_value_for_pokertest(manos_list:list):
    chisquare_expected = 12.5916 #Estadístico para 7 intervalos con α=0.05
    CARTA_ALTA = 0.3024
    PAR = 0.504
    DOBLE_PAR = 0.108
    TRIO = 0.072
    FULL_HOUSE = 0.009
    POKER = 0.0045
    QUINTILLA = 0.0001

    esperado = {"Carta Alta":CARTA_ALTA * len(manos_list),"Par":PAR * len(manos_list),"Doble Par":DOBLE_PAR * len(manos_list),"Trío":TRIO * len(manos_list),"Full House":FULL_HOUSE * len(manos_list),"Poker":POKER*len(manos_list),"Quintilla":QUINTILLA*len(manos_list)}
    observado = Counter(manos_list)

    chisquare_observed = 0
    for clave in esperado:
        chisquare_observed += (((esperado[clave]-observado[clave])**2)/esperado[clave])
        print(f"{clave}: esperado={esperado[clave]}, observado={observado[clave]}")
    print("Valor de chi cuadrada: ",chisquare_observed)
    if(chisquare_observed < chisquare_expected):
        print("No rechaza")
    else:
        print("Rechaza")

def poker_test(numeros:list):
    manos_list = []
    for num in numeros:
        manos_list.append(hand_type(digits(num)))
    print("Prueba de poker")
    stadistic_value_for_pokertest(manos_list)