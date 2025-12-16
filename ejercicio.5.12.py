import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PARÁMETROS DEL SISTEMA
# ============================================================

tasa_llegada = 20  # clientes por hora
tasa_llegada_minuto = 60 / tasa_llegada
media_entre_llegadas = 1 / tasa_llegada_minuto
media_servicio_est1 = 2
min_servicio_est2 = 1
max_servicio_est2 = 2

# Números aleatorios proporcionados
aleatorios_proporcionados = [
    0.5992431641, 0.9508666992, 0.3063964844, 0.9158325195, 0.0291748047,
    0.8964233398, 0.767578125, 0.8926391602, 0.5216064453, 0.9044799805,
    0.2912597656, 0.9319458008, 0.0765380859, 0.9750366211, 0.8774414062,
    0.0337524414, 0.6939697266, 0.1080932617, 0.5261230469, 0.198059082,
    0.3739013672, 0.3036499023, 0.2373046875, 0.4248657227, 0.1163330078,
    0.561706543, 0.0109863281, 0.7141723633, 0.9212646484, 0.8822631836,
    0.8471679688, 0.0659790039, 0.7886962891, 0.2653198242, 0.7458496094,
    0.4802856445, 0.7186279297, 0.7108764648, 0.70703125, 0.9570922852,
    0.7110595703, 0.2189331055, 0.7307128906, 0.4963989258, 0.7659912109,
    0.7894897461, 0.8168945312, 0.0982055664, 0.8834228516, 0.4225463867,
    0.9655761719, 0.762512207, 0.0633544922, 0.1181030273, 0.1767578125,
    0.4893188477, 0.3057861328, 0.876159668, 0.4504394531, 0.2786254883
]

num_clientes = len(aleatorios_proporcionados)

# ============================================================
# GENERACIÓN DE TIEMPOS
# ============================================================

tiempos_entre_llegadas = [-(media_entre_llegadas) * np.log(1 - a) for a in aleatorios_proporcionados]
tiempos_servicio_est1 = [-media_servicio_est1 * np.log(1 - a) for a in aleatorios_proporcionados]
tiempos_servicio_est2 = [min_servicio_est2 + (max_servicio_est2 - min_servicio_est2) * a for a in aleatorios_proporcionados]

# Inicialización
llegadas_est1 = np.zeros(num_clientes)
inicio_servicio_est1 = np.zeros(num_clientes)
fin_servicio_est1 = np.zeros(num_clientes)
espera_cola1 = np.zeros(num_clientes)

llegadas_est2 = np.zeros(num_clientes)
inicio_servicio_est2 = np.zeros(num_clientes)
fin_servicio_est2 = np.zeros(num_clientes)
espera_cola2 = np.zeros(num_clientes)

tiempo_total_sistema = np.zeros(num_clientes)

# ============================================================
# SIMULACIÓN EVENTO A EVENTO
# ============================================================

for i in range(num_clientes):
    # Llegadas a estación 1
    llegadas_est1[i] = tiempos_entre_llegadas[i] if i == 0 else llegadas_est1[i-1] + tiempos_entre_llegadas[i]
    
    # Estación 1
    inicio_servicio_est1[i] = max(llegadas_est1[i], fin_servicio_est1[i-1]) if i > 0 else llegadas_est1[i]
    fin_servicio_est1[i] = inicio_servicio_est1[i] + tiempos_servicio_est1[i]
    espera_cola1[i] = inicio_servicio_est1[i] - llegadas_est1[i]

    # Estación 2
    llegadas_est2[i] = fin_servicio_est1[i]
    inicio_servicio_est2[i] = max(llegadas_est2[i], fin_servicio_est2[i-1]) if i > 0 else llegadas_est2[i]
    fin_servicio_est2[i] = inicio_servicio_est2[i] + tiempos_servicio_est2[i]
    espera_cola2[i] = inicio_servicio_est2[i] - llegadas_est2[i]

    # Total en el sistema
    tiempo_total_sistema[i] = fin_servicio_est2[i] - llegadas_est1[i]

# ============================================================
# L(t) EN TIEMPO REAL
# ============================================================

t_max = max(fin_servicio_est2)
dt = 0.1
timeline = np.arange(0, t_max, dt)

cola1_Lt = []
cola2_Lt = []

for t in timeline:
    cola1_Lt.append(np.sum((llegadas_est1 <= t) & (inicio_servicio_est1 > t)))
    cola2_Lt.append(np.sum((llegadas_est2 <= t) & (inicio_servicio_est2 > t)))

# ============================================================
# INTERFAZ TABULAR SOLICITADA
# ============================================================

df_interfaz = pd.DataFrame({
    "ID Cliente": np.arange(1, num_clientes + 1),
    "Hora llegada": llegadas_est1,
    
    "Inicio servicio Est1": inicio_servicio_est1,
    "Tiempo atención Cola1": tiempos_servicio_est1,
    "Espera Cola 1": espera_cola1,

    "Inicio servicio Est2": inicio_servicio_est2,
    "Tiempo atención Cola2": tiempos_servicio_est2,
    "Hora salida final": fin_servicio_est2
})

print("\n========== INTERFAZ DEL SISTEMA ==========\n")
print(df_interfaz.to_string(index=False))

# ============================================================
# ÚNICA GRÁFICA FINAL: EVOLUCIÓN DE LAS COLAS
# ============================================================

plt.figure()
plt.step(timeline, cola1_Lt, where="post", label="Cola 1")
plt.step(timeline, cola2_Lt, where="post", label="Cola 2")
plt.xlabel("Tiempo (min)")
plt.ylabel("Clientes en cola")
plt.title("Evolución de las colas en el tiempo")
plt.legend()
plt.grid()
plt.show()
