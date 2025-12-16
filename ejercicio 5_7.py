'''
Un vendedor de revistas compra mensualmente una revista el día primero de cada mes, 
el costo de cada ejemplar es de $1.50. La demanda los primeros 10 días sigue una 
distribuciónde probabilidad: 

Demanda         5 |    6 |    7 |    8 |    9 |   10 | 11 
Probabilidad 0.05 | 0.05 | 0.10 | 0.15 | 0.25 | 0.25 | 0.15 

Al final del décimo día, el vendedor puede regresar cualquier cantidad al proveedor, 
quien se las pagará a $0.90 el ejemplar, o comprar más a $1.20 el ejemplar. 
La demanda en los siguientes 20 días está dada por la siguiente distribución de probabilidad:

Demanda         4 |    5 |    6 |    7 | 8 
Probabilidad 0.15 | 0.20 | 0.30 | 0.20 | 0.15 

Al final del mes, el vendedor puede regresar al proveedor las revistas que le sobren, 
las cuáles se les pagarán a $0.60 el ejemplar. 
Finalmente se asume que después de un mes ya no existe demanda por parte del público. 
Si el precio al público es de $2 por ejemplar, determina la política óptima de compra
'''
import number_generator as ng
#Parámetros de la simulación
precio_venta = 2
costo_inicial = 1.5
precio_devolucion_inicial = 0.9
costo_adicional = 1.2
precio_devolucion_final = 0.6

#Parámetros a evaluar
compra_inicial = 90
cantidad_devolucion_inicial = 10
compra_adicional = 60

#generación numeros aleatorios
numbers1 = ng.conguencial_mixto(123,129,17,10037)
numbers2 = ng.conguencial_mixto(123,129,17,10037)
#numbers2 = ng.conguencial_mixto(457,129,17,2053)
numbers1.extend(numbers2)

distr_demanda_inicial = {5:0.05, 6:0.1, 7:0.2, 8:0.35, 9:0.6, 10:0.85, 11:1}
distr_demanda_final = {4:0.15, 5:0.35, 6:0.65, 7:0.85, 8:1}

def demanda(numeros:list,distr_demanda:dict)->int:
    demanda_dia = 0
    num = numeros.pop()
    for demanda,valor in distr_demanda.items():
        if(num<valor):
            demanda_dia = demanda
            break
    return demanda_dia

def utilidad(compra_inicial:int,costo_inicial:float,cantidad_devolucion:int,precio_devolucion:float,demanda:int):
    ventas = min(compra_inicial,demanda)
    inventario_remanente = max(0,compra_inicial-demanda)

    ganancia = ventas*precio_venta
    if(demanda > compra_inicial):
        perdida = (demanda-compra_inicial)*costo_inicial
        utilidad = ganancia - perdida
    
    else:
        perdida = inventario_remanente*costo_inicial

        if(cantidad_devolucion > inventario_remanente):
            ganancia_devolucion = inventario_remanente*precio_devolucion
            utilidad = ganancia - perdida + ganancia_devolucion

        else: 
            inventario_remanente = inventario_remanente - cantidad_devolucion
            ganancia_devolucion = cantidad_devolucion*precio_devolucion
            utilidad = ganancia - perdida + ganancia_devolucion
            
    return utilidad,inventario_remanente

def simulacion_mes(numeros):
    demanda_inicial = []
    demanda_total_inicial = 0
    demanda_final = []
    demanda_total_final = 0

    #primeros 10 días
    for i in range(0,10):
        demanda_inicial.append(demanda(numeros,distr_demanda_inicial))
        demanda_total_inicial += demanda_inicial[i]
    print("Demanda primeros 10 días: ")
    print(demanda_inicial)
    utilidad_inicial,inventario_remanente = utilidad(compra_inicial,costo_inicial,cantidad_devolucion_inicial,precio_devolucion_inicial,demanda_total_inicial)
    print(f"Utilidad primeros 10 días: {utilidad_inicial}")
    print(f"Inventario remanente: {inventario_remanente}")

    #siguientes 20 días
    for i in range(0,20):
        demanda_final.append(demanda(numeros,distr_demanda_final))
        demanda_total_final += demanda_final[i]
    print("Demanda 20 días siguientes: ")
    print(demanda_final)
    utilidad_final,inventario_remanente = utilidad(compra_adicional+inventario_remanente,costo_adicional,1000,precio_devolucion_final,demanda_total_final)
    print(f"Utilidad siguientes 20 días: {utilidad_final}")
    print(f"Inventario remanente: {inventario_remanente}")

    return utilidad_inicial+utilidad_final


#print("Utilidad promedio"+mes_inicio(numbers1))
#for i in range(0,10):
 #   print(demanda(numbers1,distr_demanda_inicial))
max_utilidad = 0
compra_optima_inicial = 0
compra_optima_adicional = 0


def cal_max_utilidad(utilidades_anio):
    global max_utilidad, compra_optima_inicial, compra_optima_adicional
    for utilidad in utilidades_anio:
        if(utilidad>max_utilidad):
            max_utilidad = utilidad
            compra_optima_inicial = compra_inicial
            compra_optima_adicional = compra_adicional

utilidades_anio = []
contador_anio = 1
while(compra_inicial < 111):
    compra_adicional = 50
    while(compra_adicional < 81):
        utilidades_mes = 0
        print(f"Año #{contador_anio}")
        print(f"Valor de compra inicial {compra_inicial}")
        print(f"Valor de compra adicional {compra_adicional}")
        print()
        for mes in range(0,12):
                utilidades_mes += (simulacion_mes(numbers1))
        print(f"Utilidad por año -----------> {utilidades_mes}")
        print()
        contador_anio += 1
        utilidades_anio.append(utilidades_mes)
        cal_max_utilidad(utilidades_anio)
        compra_adicional += 10
    compra_inicial += 10



print(f"utilidad máxima {max_utilidad}")
print(f"Compra óptima los primeros 10 días {compra_optima_inicial}")
print(f"Compra óptima los siguientes 20 días {compra_optima_adicional}")