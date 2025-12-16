import re
import math
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import random
import csv
from openpyxl import Workbook
import pandas as pd

class GeneradorCongruencialMixto:
    def __init__(self):
        self.a = 19
        self.c = 61
        self.m = 74
        self.x0 = 25
        self.current_x = 25
        self.numeros_generados = []
    
    def generar_parametros_aleatorios(self):
        """Genera parámetros aleatorios pequeños"""
        self.a = random.randint(2, 50)
        self.c = random.randint(1, 50)
        primos = [71, 73, 74, 79, 83, 89, 97]
        self.m = random.choice(primos)
        self.generar_semilla()
    
    def generar_semilla(self):
        """Genera una semilla aleatoria entre 1 y m-1"""
        self.x0 = random.randint(1, max(1, self.m-1))
        self.current_x = self.x0
    
    def generar_numeros(self, cantidad):
        """Genera la cantidad especificada de números aleatorios"""
        self.numeros_generados = []
        x = self.current_x
        
        for _ in range(cantidad):
            producto = self.a * x + self.c
            siguiente = producto % self.m
            normalizado = siguiente / self.m if self.m != 0 else 0.0
            
            self.numeros_generados.append(normalizado)
            x = siguiente
        
        self.current_x = x
        return self.numeros_generados

class ProblemaResolver:
    def __init__(self):
        self.media = None
        self.preguntas = []
        self.distribucion = None
        self.parametros = {}
        self.generador = GeneradorCongruencialMixto()
        self.numeros_aleatorios = []
        self.metodo_normal = None
        
    def seleccionar_distribucion(self):
        """Paso 1: Seleccionar la distribución a usar"""
        distribuciones = [
            "Exponencial",
            "Uniforme", 
            "Normal",
            "Erlang",
            "Poisson",
            "Binomial"
        ]
        
        root = tk.Tk()
        root.withdraw()
        
        seleccion = simpledialog.askstring(
            "Seleccionar Distribución",
            "Seleccione la distribución a usar:\n\n" +
            "\n".join([f"{i+1}. {dist}" for i, dist in enumerate(distribuciones)]) +
            "\n\nIngrese el número:"
        )
        
        if not seleccion:
            return False
            
        try:
            opcion = int(seleccion)
            if 1 <= opcion <= len(distribuciones):
                self.distribucion = distribuciones[opcion-1]
                
                # Si es Normal, preguntar por el método
                if self.distribucion == "Normal":
                    metodo = simpledialog.askstring(
                        "Método para Distribución Normal",
                        "Seleccione el método para generar números normales:\n\n" +
                        "1. Método de 12 números aleatorios\n" +
                        "2. Método Box-Muller\n\n" +
                        "Ingrese el número:"
                    )
                    
                    if metodo == "1":
                        self.metodo_normal = "12_numeros"
                    elif metodo == "2":
                        self.metodo_normal = "box_muller"
                    else:
                        messagebox.showerror("Error", "Método inválido")
                        return False
                
                return True
        except:
            pass
            
        messagebox.showerror("Error", "Selección inválida")
        return False
    
    def obtener_parametros_distribucion(self):
        """Paso 2: Obtener los parámetros necesarios para la distribución seleccionada"""
        if self.distribucion == "Exponencial":
            media = simpledialog.askfloat("Parámetro Exponencial", 
                                        "Ingrese la media:", 
                                        initialvalue=10)
            if media is not None:
                self.parametros = {"media": media}
                return True
                
        elif self.distribucion == "Uniforme":
            a = simpledialog.askfloat("Parámetro Uniforme", "Ingrese a (límite inferior):", initialvalue=0)
            b = simpledialog.askfloat("Parámetro Uniforme", "Ingrese b (límite superior):", initialvalue=1)
            if a is not None and b is not None:
                self.parametros = {"a": a, "b": b}
                return True
                
        elif self.distribucion == "Normal":
            mu = simpledialog.askfloat("Parámetro Normal", "Ingrese μ (media):", initialvalue=0)
            sigma = simpledialog.askfloat("Parámetro Normal", "Ingrese σ (desviación estándar):", initialvalue=1)
            if mu is not None and sigma is not None:
                self.parametros = {"mu": mu, "sigma": sigma}
                return True
                
        elif self.distribucion == "Erlang":
            k = simpledialog.askinteger("Parámetro Erlang", "Ingrese k (número de etapas):", initialvalue=2)
            media = simpledialog.askfloat("Parámetro Erlang", "Ingrese la media:", initialvalue=10)
            if k is not None and media is not None:
                self.parametros = {"k": k, "media": media}
                return True
                
        elif self.distribucion == "Poisson":
            lambd = simpledialog.askfloat("Parámetro Poisson", "Ingrese λ (tasa):", initialvalue=5)
            if lambd is not None:
                self.parametros = {"lambda": lambd}
                return True
                
        elif self.distribucion == "Binomial":
            n = simpledialog.askinteger("Parámetro Binomial", "Ingrese n (número de ensayos):", initialvalue=10)
            p = simpledialog.askfloat("Parámetro Binomial", "Ingrese p (probabilidad de éxito):", initialvalue=0.5)
            if n is not None and p is not None:
                self.parametros = {"n": n, "p": p}
                return True
        
        return False

    def generar_numeros_aleatorios(self):
        """Paso 3: Generar o cargar números aleatorios"""
        root = tk.Tk()
        root.withdraw()
        
        # Preguntar si usar generador automático
        usar_generador = messagebox.askyesno(
            "Generador de Números Aleatorios",
            "¿Desea usar el generador congruencial mixto para generar números aleatorios?\n\n"
            "Sí: Se generarán números automáticamente\n"
            "No: Podrá cargar números desde un archivo Excel"
        )
        
        if usar_generador:
            # Configuración automática del generador
            self.generador.generar_parametros_aleatorios()
            
            # Pedir cantidad de números a generar
            cantidad = simpledialog.askinteger(
                "Cantidad de Números",
                "¿Cuántos números aleatorios desea generar?",
                initialvalue=100,
                minvalue=10,
                maxvalue=10000
            )
            
            if cantidad is None:
                return False
            
            # Generar números
            self.numeros_aleatorios = self.generador.generar_numeros(cantidad)
            
            messagebox.showinfo(
                "Generación Completada",
                f"Se generaron {cantidad} números aleatorios\n"
                f"Parámetros usados:\n"
                f"a={self.generador.a}, c={self.generador.c}, m={self.generador.m}, X₀={self.generador.x0}"
            )
            
            # Mostrar números generados
            self.mostrar_numeros_generados()
            
        else:
            # Cargar desde Excel
            if not self.cargar_numeros_excel():
                return False
        
        return True

    def mostrar_numeros_generados(self):
        """Muestra los números aleatorios generados en una ventana"""
        if not self.numeros_aleatorios:
            return
        
        # Crear ventana para mostrar números
        ventana_numeros = tk.Toplevel()
        ventana_numeros.title("Números Aleatorios Generados")
        ventana_numeros.geometry("600x400")
        
        # Frame para controles
        frame_controles = tk.Frame(ventana_numeros)
        frame_controles.pack(pady=10)
        
        tk.Button(frame_controles, text="Exportar a Excel", 
                 command=self.exportar_numeros_excel).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controles, text="Cerrar", 
                 command=ventana_numeros.destroy).pack(side=tk.LEFT, padx=5)
        
        # Texto con scroll
        frame_texto = tk.Frame(ventana_numeros)
        frame_texto.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        texto = tk.Text(frame_texto, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(frame_texto, command=texto.yview)
        texto.config(yscrollcommand=scrollbar.set)
        
        texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insertar números en el texto
        texto.insert(tk.END, f"Números aleatorios generados ({len(self.numeros_aleatorios)} total):\n\n")
        for i, numero in enumerate(self.numeros_aleatorios, 1):
            texto.insert(tk.END, f"{i:4d}: {numero:.6f}\n")
        
        texto.config(state=tk.DISABLED)
    
    def cargar_numeros_excel(self):
        """Carga números aleatorios desde archivo Excel"""
        archivo_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel con números aleatorios",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )
        
        if not archivo_path:
            return False
        
        try:
            data = pd.read_excel(archivo_path)
            # Tomar la primera columna
            col = data.columns[0]
            self.numeros_aleatorios = data[col].dropna().tolist()
            
            # Convertir a float y asegurar que estén en (0,1)
            self.numeros_aleatorios = [min(max(float(x), 1e-12), 1-1e-12) for x in self.numeros_aleatorios]
            
            messagebox.showinfo(
                "Carga Exitosa",
                f"Se cargaron {len(self.numeros_aleatorios)} números aleatorios"
            )
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
            return False
    
    def exportar_numeros_excel(self):
        """Exporta los números aleatorios a Excel"""
        if not self.numeros_aleatorios:
            messagebox.showwarning("Advertencia", "No hay números aleatorios para exportar")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            title="Guardar números aleatorios en Excel",
            filetypes=[("Archivos Excel", "*.xlsx")]
        )
        
        if not archivo:
            return
        
        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Números Aleatorios"
            
            # Encabezados
            ws.append(["Números Aleatorios U(0,1)"])
            ws.append([f"Total generados: {len(self.numeros_aleatorios)}"])
            if hasattr(self.generador, 'a'):
                ws.append([f"Parámetros: a={self.generador.a}, c={self.generador.c}, m={self.generador.m}, X₀={self.generador.x0}"])
            ws.append([])  # Línea en blanco
            
            # Agregar números
            for numero in self.numeros_aleatorios:
                ws.append([numero])
            
            wb.save(archivo)
            messagebox.showinfo("Éxito", f"Números aleatorios exportados a: {archivo}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar el archivo: {e}")
    
    def seleccionar_tipos_preguntas(self):
        """Paso 4: Seleccionar qué tipos de preguntas resolver"""
        root = tk.Tk()
        root.withdraw()
        
        self.preguntas = []
        
        # Preguntar por cada tipo de pregunta
        tipos_preguntas = [
            {
                "tipo": "probabilidad_menor_que",
                "nombre": "Probabilidad P(X < a) - Menor que un valor",
                "parametro": "a (límite superior)"
            },
            {
                "tipo": "probabilidad_entre", 
                "nombre": "Probabilidad P(a < X < b) - Entre dos valores",
                "parametro": "a y b (límites)"
            },
            {
                "tipo": "probabilidad_mayor_que",
                "nombre": "Probabilidad P(X > a) - Mayor que un valor", 
                "parametro": "a (límite inferior)"
            },
            {
                "tipo": "valor_esperado",
                "nombre": "Valor esperado E[X]",
                "parametro": "Ninguno"
            }
        ]
        
        for tipo_pregunta in tipos_preguntas:
            respuesta = messagebox.askyesno(
                "Seleccionar Preguntas",
                f"¿Desea calcular: {tipo_pregunta['nombre']}?"
            )
            
            if respuesta:
                if tipo_pregunta["tipo"] == "probabilidad_menor_que":
                    a = simpledialog.askfloat(
                        "Parámetro para P(X < a)",
                        f"Ingrese el valor de a (límite superior):",
                        initialvalue=10
                    )
                    if a is not None:
                        self.preguntas.append({
                            "tipo": "probabilidad_menor_que",
                            "a": a,
                            "descripcion": f"Probabilidad de que X sea menor que {a} - P(X < {a})"
                        })
                
                elif tipo_pregunta["tipo"] == "probabilidad_entre":
                    a = simpledialog.askfloat(
                        "Parámetro para P(a < X < b)",
                        "Ingrese el valor de a (límite inferior):",
                        initialvalue=6
                    )
                    b = simpledialog.askfloat(
                        "Parámetro para P(a < X < b)", 
                        "Ingrese el valor de b (límite superior):",
                        initialvalue=18
                    )
                    if a is not None and b is not None:
                        self.preguntas.append({
                            "tipo": "probabilidad_entre",
                            "a": a,
                            "b": b,
                            "descripcion": f"Probabilidad de que X esté entre {a} y {b} - P({a} < X < {b})"
                        })
                
                elif tipo_pregunta["tipo"] == "probabilidad_mayor_que":
                    a = simpledialog.askfloat(
                        "Parámetro para P(X > a)",
                        f"Ingrese el valor de a (límite inferior):",
                        initialvalue=12
                    )
                    if a is not None:
                        self.preguntas.append({
                            "tipo": "probabilidad_mayor_que",
                            "a": a,
                            "descripcion": f"Probabilidad de que X sea mayor que {a} - P(X > {a})"
                        })
                
                elif tipo_pregunta["tipo"] == "valor_esperado":
                    self.preguntas.append({
                        "tipo": "valor_esperado",
                        "descripcion": "Valor esperado de X - E[X]"
                    })
        
        return len(self.preguntas) >= 0
    
    def generar_muestras_normal(self):
        """Genera muestras para distribución normal según el método seleccionado"""
        muestras = []
        mu = self.parametros["mu"]
        sigma = self.parametros["sigma"]
        
        if self.metodo_normal == "12_numeros":
            # Método de 12 números aleatorios (Teorema del Límite Central)
            for i in range(0, len(self.numeros_aleatorios) - 11, 12):
                grupo = self.numeros_aleatorios[i:i+12]
                z = sum(grupo) - 6  # Suma de 12 U(0,1) - 6 ≈ N(0,1)
                x = mu + sigma * z
                muestras.append(x)
        else:  # box_muller
            # Método Box-Muller
            for i in range(0, len(self.numeros_aleatorios) - 1, 2):
                u1 = self.numeros_aleatorios[i]
                u2 = self.numeros_aleatorios[i+1]
                
                z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
                x = mu + sigma * z0
                muestras.append(x)
        
        return muestras
    
    def calcular_respuestas(self):
        """Calcula las respuestas para todas las preguntas seleccionadas"""
        resultados = []
        
        for pregunta in self.preguntas:
            if pregunta["tipo"] == "probabilidad_menor_que":
                resultado = self.calcular_probabilidad_menor_que(pregunta["a"])
                resultados.append(resultado)
                
            elif pregunta["tipo"] == "probabilidad_entre":
                resultado = self.calcular_probabilidad_entre(pregunta["a"], pregunta["b"])
                resultados.append(resultado)
                
            elif pregunta["tipo"] == "probabilidad_mayor_que":
                resultado = self.calcular_probabilidad_mayor_que(pregunta["a"])
                resultados.append(resultado)
                
            elif pregunta["tipo"] == "valor_esperado":
                resultado = self.calcular_valor_esperado()
                resultados.append(resultado)
        
        return resultados
    
    def calcular_probabilidad_menor_que(self, a):
        """Calcula P(X < a)"""
        if self.distribucion == "Exponencial":
            media = self.parametros["media"]
            lambda_param = 1 / media
            probabilidad = 1 - math.exp(-lambda_param * a)
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [-media * math.log(u) for u in self.numeros_aleatorios]
                simulacion = sum(1 for x in muestras if x < a) / len(muestras)
            
            return {
                "pregunta": f"P(X < {a})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución exponencial con media {media}:\nP(X < {a}) = 1 - e^(-λ × {a}) = 1 - e^(-{a}/{media}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
            
        elif self.distribucion == "Uniforme":
            a_param, b_param = self.parametros["a"], self.parametros["b"]
            if a <= a_param:
                probabilidad = 0.0
            elif a >= b_param:
                probabilidad = 1.0
            else:
                probabilidad = (a - a_param) / (b_param - a_param)
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [a_param + (b_param - a_param) * u for u in self.numeros_aleatorios]
                simulacion = sum(1 for x in muestras if x < a) / len(muestras)
                
            return {
                "pregunta": f"P(X < {a})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución uniforme en [{a_param}, {b_param}]:\nP(X < {a}) = ({a} - {a_param}) / ({b_param} - {a_param}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
            
        elif self.distribucion == "Normal":
            mu, sigma = self.parametros["mu"], self.parametros["sigma"]
            
            z = (a - mu) / sigma
            probabilidad = 0.5 * (1 + math.erf(z / math.sqrt(2)))
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = self.generar_muestras_normal()
                if muestras:
                    simulacion = sum(1 for x in muestras if x < a) / len(muestras)
            
            return {
                "pregunta": f"P(X < {a})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución normal con μ={mu}, σ={sigma}:\nP(X < {a}) = Φ(({a} - {mu})/{sigma}) = Φ({z:.4f}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
        
        return {
            "pregunta": f"P(X < {a})",
            "respuesta": "No implementado para esta distribución",
            "simulacion": None,
            "explicacion": "Cálculo no disponible",
            "porcentaje": "N/A"
        }
    
    def calcular_probabilidad_entre(self, a, b):
        """Calcula P(a < X < b)"""
        if self.distribucion == "Exponencial":
            media = self.parametros["media"]
            lambda_param = 1 / media
            probabilidad = math.exp(-lambda_param * a) - math.exp(-lambda_param * b)
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [-media * math.log(u) for u in self.numeros_aleatorios]
                simulacion = sum(1 for x in muestras if a < x < b) / len(muestras)
            
            return {
                "pregunta": f"P({a} < X < {b})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución exponencial con media {media}:\nP({a} < X < {b}) = e^(-λ × {a}) - e^(-λ × {b}) = e^(-{a}/{media}) - e^(-{b}/{media}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
            
        elif self.distribucion == "Uniforme":
            a_param, b_param = self.parametros["a"], self.parametros["b"]
            low = max(a_param, a)
            high = min(b_param, b)
            if low >= high:
                probabilidad = 0.0
            else:
                probabilidad = (high - low) / (b_param - a_param)
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [a_param + (b_param - a_param) * u for u in self.numeros_aleatorios]
                simulacion = sum(1 for x in muestras if a < x < b) / len(muestras)
                
            return {
                "pregunta": f"P({a} < X < {b})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución uniforme en [{a_param}, {b_param}]:\nP({a} < X < {b}) = ({high} - {low}) / ({b_param} - {a_param}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
            
        elif self.distribucion == "Normal":
            mu, sigma = self.parametros["mu"], self.parametros["sigma"]
            
            z1 = (a - mu) / sigma
            z2 = (b - mu) / sigma
            prob1 = 0.5 * (1 + math.erf(z1 / math.sqrt(2)))
            prob2 = 0.5 * (1 + math.erf(z2 / math.sqrt(2)))
            probabilidad = prob2 - prob1
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = self.generar_muestras_normal()
                if muestras:
                    simulacion = sum(1 for x in muestras if a < x < b) / len(muestras)
            
            return {
                "pregunta": f"P({a} < X < {b})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución normal con μ={mu}, σ={sigma}:\nP({a} < X < {b}) = Φ(({b}-{mu})/{sigma}) - Φ(({a}-{mu})/{sigma}) = Φ({z2:.4f}) - Φ({z1:.4f}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
        
        return {
            "pregunta": f"P({a} < X < {b})",
            "respuesta": "No implementado para esta distribución",
            "simulacion": None,
            "explicacion": "Cálculo no disponible",
            "porcentaje": "N/A"
        }
    
    def calcular_probabilidad_mayor_que(self, a):
        """Calcula P(X > a)"""
        if self.distribucion == "Exponencial":
            media = self.parametros["media"]
            lambda_param = 1 / media
            probabilidad = math.exp(-lambda_param * a)
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [-media * math.log(u) for u in self.numeros_aleatorios]
                simulacion = sum(1 for x in muestras if x > a) / len(muestras)
            
            return {
                "pregunta": f"P(X > {a})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución exponencial con media {media}:\nP(X > {a}) = e^(-λ × {a}) = e^(-{a}/{media}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
            
        elif self.distribucion == "Uniforme":
            a_param, b_param = self.parametros["a"], self.parametros["b"]
            if a >= b_param:
                probabilidad = 0.0
            elif a <= a_param:
                probabilidad = 1.0
            else:
                probabilidad = (b_param - a) / (b_param - a_param)
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [a_param + (b_param - a_param) * u for u in self.numeros_aleatorios]
                simulacion = sum(1 for x in muestras if x > a) / len(muestras)
                
            return {
                "pregunta": f"P(X > {a})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución uniforme en [{a_param}, {b_param}]:\nP(X > {a}) = ({b_param} - {a}) / ({b_param} - {a_param}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
            
        elif self.distribucion == "Normal":
            mu, sigma = self.parametros["mu"], self.parametros["sigma"]
            
            z = (a - mu) / sigma
            probabilidad = 1 - 0.5 * (1 + math.erf(z / math.sqrt(2)))
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = self.generar_muestras_normal()
                if muestras:
                    simulacion = sum(1 for x in muestras if x > a) / len(muestras)
            
            return {
                "pregunta": f"P(X > {a})",
                "respuesta": probabilidad,
                "simulacion": simulacion,
                "explicacion": f"Para distribución normal con μ={mu}, σ={sigma}:\nP(X > {a}) = 1 - Φ(({a} - {mu})/{sigma}) = 1 - Φ({z:.4f}) = {probabilidad:.6f}",
                "porcentaje": f"{probabilidad * 100:.2f}%"
            }
        
        return {
            "pregunta": f"P(X > {a})",
            "respuesta": "No implementado para esta distribución",
            "simulacion": None,
            "explicacion": "Cálculo no disponible",
            "porcentaje": "N/A"
        }
    
    def calcular_valor_esperado(self):
        """Calcula E[X]"""
        if self.distribucion == "Exponencial":
            valor = self.parametros["media"]
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [-self.parametros["media"] * math.log(u) for u in self.numeros_aleatorios]
                simulacion = sum(muestras) / len(muestras)
            
            return {
                "pregunta": "E[X]",
                "respuesta": valor,
                "simulacion": simulacion,
                "explicacion": f"Para distribución exponencial: E[X] = media = {valor}",
                "unidad": "unidades"
            }
            
        elif self.distribucion == "Uniforme":
            a, b = self.parametros["a"], self.parametros["b"]
            valor = (a + b) / 2
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = [a + (b - a) * u for u in self.numeros_aleatorios]
                simulacion = sum(muestras) / len(muestras)
            
            return {
                "pregunta": "E[X]",
                "respuesta": valor,
                "simulacion": simulacion,
                "explicacion": f"Para distribución uniforme: E[X] = (a + b) / 2 = ({a} + {b}) / 2 = {valor}",
                "unidad": "unidades"
            }
            
        elif self.distribucion == "Normal":
            valor = self.parametros["mu"]
            
            simulacion = None
            if self.numeros_aleatorios:
                muestras = self.generar_muestras_normal()
                if muestras:
                    simulacion = sum(muestras) / len(muestras)
            
            return {
                "pregunta": "E[X]",
                "respuesta": valor,
                "simulacion": simulacion,
                "explicacion": f"Para distribución normal: E[X] = μ = {valor}",
                "unidad": "unidades"
            }
        
        return {
            "pregunta": "E[X]",
            "respuesta": "No implementado para esta distribución",
            "simulacion": None,
            "explicacion": "Cálculo no disponible",
            "unidad": "N/A"
        }
    
    def mostrar_resultados(self, resultados):
        """Muestra los resultados en una ventana"""
        if not resultados:
            messagebox.showinfo("Resultados", "No hay resultados para mostrar")
            return
        
        texto_resultados = f"=== RESULTADOS - Distribución {self.distribucion} ===\n\n"
        texto_resultados += f"Parámetros usados: {self.parametros}\n\n"
        
        if self.distribucion == "Normal" and self.metodo_normal:
            texto_resultados += f"Método usado para Normal: {self.metodo_normal}\n\n"
        
        if self.numeros_aleatorios:
            texto_resultados += f"Números aleatorios usados: {len(self.numeros_aleatorios)}\n\n"
        
        for resultado in resultados:
            texto_resultados += f"{resultado['pregunta']}:\n"
            texto_resultados += f"  Respuesta teórica: {resultado['respuesta']}\n"
            if resultado['simulacion'] is not None:
                texto_resultados += f"  Simulación: {resultado['simulacion']:.6f}\n"
            if 'porcentaje' in resultado:
                texto_resultados += f"  Porcentaje: {resultado['porcentaje']}\n"
            if 'unidad' in resultado:
                texto_resultados += f"  Unidad: {resultado['unidad']}\n"
            texto_resultados += f"  Explicación: {resultado['explicacion']}\n\n"
        
        # Mostrar en ventana
        root = tk.Tk()
        root.title("Resultados del Problema")
        root.geometry("800x600")
        
        text_widget = tk.Text(root, wrap=tk.WORD)
        text_widget.insert(tk.END, texto_resultados)
        text_widget.config(state=tk.DISABLED)
        
        scrollbar = tk.Scrollbar(root, command=text_widget.yview)
        text_widget.config(yscrollcommand=scrollbar.set)
        
        text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        def guardar_resultados():
            archivo = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivo de texto", "*.txt")]
            )
            if archivo:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(texto_resultados)
                messagebox.showinfo("Guardado", f"Resultados guardados en: {archivo}")
        
        tk.Button(root, text="Guardar Resultados", command=guardar_resultados).pack(pady=10)
        
        root.mainloop()

def main():
    resolver = ProblemaResolver()
    
    # Paso 1: Seleccionar distribución
    if not resolver.seleccionar_distribucion():
        return
    
    # Paso 2: Obtener parámetros de la distribución
    if not resolver.obtener_parametros_distribucion():
        messagebox.showerror("Error", "No se pudieron obtener los parámetros de la distribución")
        return
    
    # Paso 3: Generar o cargar números aleatorios
    if not resolver.generar_numeros_aleatorios():
        return
    
    # Paso 4: Seleccionar tipos de preguntas
    if not resolver.seleccionar_tipos_preguntas():
        messagebox.showerror("Error", "No se seleccionaron preguntas")
        return
    
    # Paso 5: Calcular respuestas
    resultados = resolver.calcular_respuestas()
    
    # Paso 6: Mostrar resultados
    resolver.mostrar_resultados(resultados)

if __name__ == "__main__":
    main()