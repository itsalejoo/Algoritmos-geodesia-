import tkinter as tk
from tkinter import ttk, messagebox
import math
from scipy.integrate import quad
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Variables globales para las constantes del elipsoide
a = 6378137.0  # Radio ecuatorial en metros
b = 6356752.314245  # Radio polar en metros
e2 = 1 - (b**2 / a**2)  # Excentricidad al cuadrado
f = (a - b) / a  # Aplanamiento
e = math.sqrt(e2)  # Primera excentricidad

# Funciones auxiliares de conversión
def sexagesimal_a_decimal(grados, minutos, segundos):
    return grados + (minutos / 60.0) + (segundos / 3600.0)

def primera_vertical(latitud_rad):
    return a / math.sqrt(1 - e2 * math.sin(latitud_rad)**2)

def longitud_arco_paralelo(latitud_deg, delta_longitud_deg):
    latitud_rad = math.radians(latitud_deg)
    delta_longitud_rad = math.radians(delta_longitud_deg)
    N_phi = primera_vertical(latitud_rad)
    longitud_arco = N_phi * math.cos(latitud_rad) * delta_longitud_rad
    return longitud_arco

def longitud_arco_paralelo_con_longitudes(latitud_deg, longitud1_deg, longitud2_deg):
    latitud_rad = math.radians(latitud_deg)
    longitud1_rad = math.radians(longitud1_deg)
    longitud2_rad = math.radians(longitud2_deg)
    delta_longitud_rad = abs(longitud1_rad - longitud2_rad)
    N_phi = primera_vertical(latitud_rad)
    longitud_arco = N_phi * math.cos(latitud_rad) * delta_longitud_rad
    return longitud_arco

def calcular_coeficientes(e2):
    A = 1 + (3/4) * e2 + (45/64) * e2**2 + (175/256) * e2**3 + (11025/16384) * e2**4 + (43659/65536) * e2**5
    B = (3/4) * e2 + (15/16) * e2**2 + (525/512) * e2**3 + (2205/2048) * e2**4 + (72765/65536) * e2**5
    C = (15/64) * e2**2 + (105/256) * e2**3 + (2205/4096) * e2**4 + (10395/16384) * e2**5
    D = (35/512) * e2**3 + (315/2048) * e2**4 + (31185/131072) * e2**5
    E = (315/16384) * e2**4 + (3465/65536) * e2**5
    F = (693/131072) * e2**5
    return A, B, C, D, E, F

def calcular_arco_meridiano(lat1, lat2, a, f):
    e2 = 2 * f - f**2
    A, B, C, D, E, F = calcular_coeficientes(e2)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    delta_lat = lat2 - lat1
    s = a * (1 - e2) * (A * delta_lat 
                        - (B / 2) * (math.sin(2 * lat2) - math.sin(2 * lat1))
                        + (C / 4) * (math.sin(4 * lat2) - math.sin(4 * lat1))
                        - (D / 6) * (math.sin(6 * lat2) - math.sin(6 * lat1))
                        + (E / 8) * (math.sin(8 * lat2) - math.sin(8 * lat1)))
    return s

def integrando(phi, e2):
    sin_phi = math.sin(phi)
    return (sin_phi + (2/3) * e2 * sin_phi**3 + (3/5) * e2**2 * sin_phi**5 + (4/7) * e2**3 * sin_phi**7)

def calcular_area_cuadrilatero(lat1, lat2, lon1, lon2, b, e2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    integral, _ = quad(integrando, phi1, phi2, args=(e2))
    area = (b**2 * delta_lambda) * integral
    return area

def validar_entradas(*entradas):
    for entrada in entradas:
        if not entrada.get():
            messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return False
    return True

def actualizar_constantes():
    global a, b, e2, f, e
    try:
        a = float(entry_a_elipsoide.get())
        b = float(entry_b_elipsoide.get())
        e2 = 1 - (b**2 / a**2)
        f = (a - b) / a
        e = math.sqrt(e2)
        messagebox.showinfo("Éxito", "Constantes del elipsoide actualizadas correctamente.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos para las constantes del elipsoide.")

def calcular_arco_meridiano_gui():
    if not validar_entradas(entry_lat1_g, entry_lat1_m, entry_lat1_s, entry_lat2_g, entry_lat2_m, entry_lat2_s):
        return
    try:
        lat1 = sexagesimal_a_decimal(float(entry_lat1_g.get()), float(entry_lat1_m.get()), float(entry_lat1_s.get()))
        lat2 = sexagesimal_a_decimal(float(entry_lat2_g.get()), float(entry_lat2_m.get()), float(entry_lat2_s.get()))
        arco_metros = calcular_arco_meridiano(lat1, lat2, a, f)
        arco_kilometros = arco_metros / 1000
        messagebox.showinfo("Resultado", f"La longitud del arco de meridiano es {arco_metros:.3f} metros ({arco_kilometros:.3f} kilómetros).")
        mostrar_grafico_2d(lat1, lat2)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

def mostrar_grafico_2d(lat1, lat2):
    fig, ax = plt.subplots()

    # Crear el elipsoide
    latitudes = np.linspace(-90, 90, 400)
    x = a * np.cos(np.radians(latitudes))
    y = b * np.sin(np.radians(latitudes))

    ax.plot(x, y, color='b', alpha=0.5)

    # Convertir las coordenadas a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)

    # Calcular las coordenadas en el elipsoide
    x1 = a * math.cos(lat1_rad)
    y1 = b * math.sin(lat1_rad)

    x2 = a * math.cos(lat2_rad)
    y2 = b * math.sin(lat2_rad)

    # Dibujar el arco de meridiano
    arco_latitudes = np.linspace(lat1, lat2, 100)
    arco_x = a * np.cos(np.radians(arco_latitudes))
    arco_y = b * np.sin(np.radians(arco_latitudes))

    ax.plot(arco_x, arco_y, color='r')

    ax.set_xlabel('Eje X (metros)')
    ax.set_ylabel('Eje Y (metros)')
    ax.set_title('Arco de Meridiano en el Elipsoide')

    plt.show()

def calcular_arco_paralelo_gui():
    if not validar_entradas(entry_lat_g, entry_lat_m, entry_lat_s):
        return
    try:
        lat = sexagesimal_a_decimal(float(entry_lat_g.get()), float(entry_lat_m.get()), float(entry_lat_s.get()))
        if metodo_var.get() == 1:
            if not validar_entradas(entry_delta_lon_g, entry_delta_lon_m, entry_delta_lon_s):
                return
            delta_lon = sexagesimal_a_decimal(float(entry_delta_lon_g.get()), float(entry_delta_lon_m.get()), float(entry_delta_lon_s.get()))
            arco_paralelo_metros = longitud_arco_paralelo(lat, delta_lon)
        else:
            if not validar_entradas(entry_lon1_g, entry_lon1_m, entry_lon1_s, entry_lon2_g, entry_lon2_m, entry_lon2_s):
                return
            lon1 = sexagesimal_a_decimal(float(entry_lon1_g.get()), float(entry_lon1_m.get()), float(entry_lon1_s.get()))
            lon2 = sexagesimal_a_decimal(float(entry_lon2_g.get()), float(entry_lon2_m.get()), float(entry_lon2_s.get()))
            arco_paralelo_metros = longitud_arco_paralelo_con_longitudes(lat, lon1, lon2)
        
        arco_paralelo_kilometros = arco_paralelo_metros / 1000
        messagebox.showinfo("Resultado", f"La longitud del arco de paralelo es {arco_paralelo_metros:.3f} metros ({arco_paralelo_kilometros:.3f} kilómetros).")
        mostrar_grafico_2D(lat, delta_lon if metodo_var.get() == 1 else lon1, lon2 if metodo_var.get() == 2 else None)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

def mostrar_grafico_2D(lat, delta_lon=None, lon2=None):
    fig, ax = plt.subplots()

    # Crear el elipsoide
    latitudes = np.linspace(-90, 90, 400)
    x = a * np.cos(np.radians(latitudes))
    y = b * np.sin(np.radians(latitudes))

    ax.plot(x, y, color='b', alpha=0.5)

    # Convertir las coordenadas a radianes
    lat_rad = math.radians(lat)

    # Calcular las coordenadas en el elipsoide
    x_lat = a * math.cos(lat_rad)
    y_lat = b * math.sin(lat_rad)

    if delta_lon is not None:
        delta_lon_rad = math.radians(delta_lon)
        x_delta = a * math.cos(lat_rad) * math.cos(delta_lon_rad)
        y_delta = a * math.cos(lat_rad) * math.sin(delta_lon_rad)
        arco_longitudes = np.linspace(0, delta_lon, 100)
        arco_x = a * math.cos(lat_rad) * np.cos(np.radians(arco_longitudes))
        arco_y = a * math.cos(lat_rad) * np.sin(np.radians(arco_longitudes))
        ax.plot(arco_x, arco_y, color='r')
    elif lon2 is not None:
        lon2_rad = math.radians(lon2)
        x_lon2 = a * math.cos(lat_rad) * math.cos(lon2_rad)
        y_lon2 = a * math.cos(lat_rad) * math.sin(lon2_rad)
        arco_longitudes = np.linspace(0, lon2, 100)
        arco_x = a * math.cos(lat_rad) * np.cos(np.radians(arco_longitudes))
        arco_y = a * math.cos(lat_rad) * np.sin(np.radians(arco_longitudes))
        ax.plot(arco_x, arco_y, color='r')

    ax.set_xlabel('Eje X (metros)')
    ax.set_ylabel('Eje Y (metros)')
    ax.set_title('Arco de Paralelo en el Elipsoide')

    plt.show()

def calcular_area_cuadrilatero_gui():
    if not validar_entradas(entry_lat1_g_cuad, entry_lat1_m_cuad, entry_lat1_s_cuad, entry_lat2_g_cuad, entry_lat2_m_cuad, entry_lat2_s_cuad, entry_lon1_g_cuad, entry_lon1_m_cuad, entry_lon1_s_cuad, entry_lon2_g_cuad, entry_lon2_m_cuad, entry_lon2_s_cuad):
        return
    try:
        lat1 = sexagesimal_a_decimal(float(entry_lat1_g_cuad.get()), float(entry_lat1_m_cuad.get()), float(entry_lat1_s_cuad.get()))
        lat2 = sexagesimal_a_decimal(float(entry_lat2_g_cuad.get()), float(entry_lat2_m_cuad.get()), float(entry_lat2_s_cuad.get()))
        lon1 = sexagesimal_a_decimal(float(entry_lon1_g_cuad.get()), float(entry_lon1_m_cuad.get()), float(entry_lon1_s_cuad.get()))
        lon2 = sexagesimal_a_decimal(float(entry_lon2_g_cuad.get()), float(entry_lon2_m_cuad.get()), float(entry_lon2_s_cuad.get()))
        area = calcular_area_cuadrilatero(lat1, lat2, lon1, lon2, b, e2)
        area_km2 = area / 1e6  # Convertir a kilómetros cuadrados
        messagebox.showinfo("Resultado", f"El área del cuadrilátero es {area:.3f} metros cuadrados ({area_km2:.3f} kilómetros cuadrados).")
        mostrar_grafico_3d(lat1, lat2, lon1, lon2)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")

def mostrar_grafico_3d(lat1, lat2, lon1, lon2):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Crear el elipsoide
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = a * np.outer(np.cos(u), np.sin(v))
    y = a * np.outer(np.sin(u), np.sin(v))
    z = b * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot_surface(x, y, z, color='b', alpha=0.1)

    # Convertir las coordenadas a radianes
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)

    # Calcular las coordenadas en el elipsoide
    x1 = a * math.cos(lat1_rad) * math.cos(lon1_rad)
    y1 = a * math.cos(lat1_rad) * math.sin(lon1_rad)
    z1 = b * math.sin(lat1_rad)

    x2 = a * math.cos(lat2_rad) * math.cos(lon1_rad)
    y2 = a * math.cos(lat2_rad) * math.sin(lon1_rad)
    z2 = b * math.sin(lat2_rad)

    x3 = a * math.cos(lat2_rad) * math.cos(lon2_rad)
    y3 = a * math.cos(lat2_rad) * math.sin(lon2_rad)
    z3 = b * math.sin(lat2_rad)

    x4 = a * math.cos(lat1_rad) * math.cos(lon2_rad)
    y4 = a * math.cos(lat1_rad) * math.sin(lon2_rad)
    z4 = b * math.sin(lat1_rad)

    # Dibujar el área del cuadrilátero
    ax.plot([x1, x2], [y1, y2], [z1, z2], color='r')
    ax.plot([x2, x3], [y2, y3], [z2, z3], color='r')
    ax.plot([x3, x4], [y3, y4], [z3, z4], color='r')
    ax.plot([x4, x1], [y4, y1], [z4, z1], color='r')

    plt.show()

def actualizar_campos():
    if metodo_var.get() == 1:
        entry_delta_lon_g.grid()
        entry_delta_lon_m.grid()
        entry_delta_lon_s.grid()
        entry_lon1_g.grid_remove()
        entry_lon1_m.grid_remove()
        entry_lon1_s.grid_remove()
        entry_lon2_g.grid_remove()
        entry_lon2_m.grid_remove()
        entry_lon2_s.grid_remove()
    else:
        entry_delta_lon_g.grid_remove()
        entry_delta_lon_m.grid_remove()
        entry_delta_lon_s.grid_remove()
        entry_lon1_g.grid()
        entry_lon1_m.grid()
        entry_lon1_s.grid()
        entry_lon2_g.grid()
        entry_lon2_m.grid()
        entry_lon2_s.grid()

# Crear la ventana principal
root = tk.Tk()
root.title("Cálculos Geodésicos")

# Crear un notebook para organizar mejor la interfaz
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

# Crear los frames para cada cálculo
frame_elipsoide = ttk.Frame(notebook, width=400, height=280)
frame_meridiano = ttk.Frame(notebook, width=400, height=280)
frame_paralelo = ttk.Frame(notebook, width=400, height=280)
frame_cuadrilatero = ttk.Frame(notebook, width=400, height=280)

frame_elipsoide.pack(fill='both', expand=True)
frame_meridiano.pack(fill='both', expand=True)
frame_paralelo.pack(fill='both', expand=True)
frame_cuadrilatero.pack(fill='both', expand=True)

notebook.add(frame_elipsoide, text='Constantes del Elipsoide')
notebook.add(frame_meridiano, text='Arco de Meridiano')
notebook.add(frame_paralelo, text='Arco de Paralelo')
notebook.add(frame_cuadrilatero, text='Área del Cuadrilátero')

# Widgets para las constantes del elipsoide
ttk.Label(frame_elipsoide, text="Radio ecuatorial (a):").grid(column=0, row=0)
entry_a_elipsoide = ttk.Entry(frame_elipsoide)
entry_a_elipsoide.grid(column=1, row=0)
entry_a_elipsoide.insert(0, str(a))

ttk.Label(frame_elipsoide, text="Radio polar (b):").grid(column=0, row=1)
entry_b_elipsoide = ttk.Entry(frame_elipsoide)
entry_b_elipsoide.grid(column=1, row=1)
entry_b_elipsoide.insert(0, str(b))

ttk.Button(frame_elipsoide, text="Actualizar Constantes", command=actualizar_constantes).grid(column=0, row=2, columnspan=2)

# Widgets para el cálculo del arco de meridiano
ttk.Label(frame_meridiano, text="Latitud inicial - Grados:").grid(column=0, row=0)
entry_lat1_g = ttk.Entry(frame_meridiano)
entry_lat1_g.grid(column=1, row=0)

ttk.Label(frame_meridiano, text="Minutos:").grid(column=0, row=1)
entry_lat1_m = ttk.Entry(frame_meridiano)
entry_lat1_m.grid(column=1, row=1)

ttk.Label(frame_meridiano, text="Segundos:").grid(column=0, row=2)
entry_lat1_s = ttk.Entry(frame_meridiano)
entry_lat1_s.grid(column=1, row=2)

ttk.Label(frame_meridiano, text="Latitud final - Grados:").grid(column=0, row=3)
entry_lat2_g = ttk.Entry(frame_meridiano)
entry_lat2_g.grid(column=1, row=3)

ttk.Label(frame_meridiano, text="Minutos:").grid(column=0, row=4)
entry_lat2_m = ttk.Entry(frame_meridiano)
entry_lat2_m.grid(column=1, row=4)

ttk.Label(frame_meridiano, text="Segundos:").grid(column=0, row=5)
entry_lat2_s = ttk.Entry(frame_meridiano)
entry_lat2_s.grid(column=1, row=5)

ttk.Button(frame_meridiano, text="Calcular Arco de Meridiano", command=calcular_arco_meridiano_gui).grid(column=0, row=6, columnspan=2)

# Widgets para el cálculo del arco de paralelo
ttk.Label(frame_paralelo, text="Latitud - Grados:").grid(column=0, row=0)
entry_lat_g = ttk.Entry(frame_paralelo)
entry_lat_g.grid(column=1, row=0)

ttk.Label(frame_paralelo, text="Minutos:").grid(column=0, row=1)
entry_lat_m = ttk.Entry(frame_paralelo)
entry_lat_m.grid(column=1, row=1)

ttk.Label(frame_paralelo, text="Segundos:").grid(column=0, row=2)
entry_lat_s = ttk.Entry(frame_paralelo)
entry_lat_s.grid(column=1, row=2)

# Opción para seleccionar el método de cálculo
metodo_var = tk.IntVar(value=1)
ttk.Radiobutton(frame_paralelo, text="Ángulo entre longitudes", variable=metodo_var, value=1, command=lambda: actualizar_campos()).grid(column=0, row=3, columnspan=2)
ttk.Radiobutton(frame_paralelo, text="Longitudes inicial y final", variable=metodo_var, value=2, command=lambda: actualizar_campos()).grid(column=0, row=4, columnspan=2)

# Widgets para el ángulo entre longitudes
ttk.Label(frame_paralelo, text="Ángulo entre longitudes - Grados:").grid(column=0, row=5)
entry_delta_lon_g = ttk.Entry(frame_paralelo)
entry_delta_lon_g.grid(column=1, row=5)

ttk.Label(frame_paralelo, text="Minutos:").grid(column=0, row=6)
entry_delta_lon_m = ttk.Entry(frame_paralelo)
entry_delta_lon_m.grid(column=1, row=6)

ttk.Label(frame_paralelo, text="Segundos:").grid(column=0, row=7)
entry_delta_lon_s = ttk.Entry(frame_paralelo)
entry_delta_lon_s.grid(column=1, row=7)

# Widgets para las longitudes inicial y final
ttk.Label(frame_paralelo, text="Longitud inicial - Grados:").grid(column=0, row=8)
entry_lon1_g = ttk.Entry(frame_paralelo)
entry_lon1_g.grid(column=1, row=8)

ttk.Label(frame_paralelo, text="Minutos:").grid(column=0, row=9)
entry_lon1_m = ttk.Entry(frame_paralelo)
entry_lon1_m.grid(column=1, row=9)

ttk.Label(frame_paralelo, text="Segundos:").grid(column=0, row=10)
entry_lon1_s = ttk.Entry(frame_paralelo)
entry_lon1_s.grid(column=1, row=10)

ttk.Label(frame_paralelo, text="Longitud final - Grados:").grid(column=0, row=11)
entry_lon2_g = ttk.Entry(frame_paralelo)
entry_lon2_g.grid(column=1, row=11)

ttk.Label(frame_paralelo, text="Minutos:").grid(column=0, row=12)
entry_lon2_m = ttk.Entry(frame_paralelo)
entry_lon2_m.grid(column=1, row=12)

ttk.Label(frame_paralelo, text="Segundos:").grid(column=0, row=13)
entry_lon2_s = ttk.Entry(frame_paralelo)
entry_lon2_s.grid(column=1, row=13)

ttk.Button(frame_paralelo, text="Calcular Arco de Paralelo", command=calcular_arco_paralelo_gui).grid(column=0, row=14, columnspan=2)

# Widgets para el cálculo del área del cuadrilátero
ttk.Label(frame_cuadrilatero, text="Latitud inicial - Grados:").grid(column=0, row=0)
entry_lat1_g_cuad = ttk.Entry(frame_cuadrilatero)
entry_lat1_g_cuad.grid(column=1, row=0)

ttk.Label(frame_cuadrilatero, text="Minutos:").grid(column=0, row=1)
entry_lat1_m_cuad = ttk.Entry(frame_cuadrilatero)
entry_lat1_m_cuad.grid(column=1, row=1)

ttk.Label(frame_cuadrilatero, text="Segundos:").grid(column=0, row=2)
entry_lat1_s_cuad = ttk.Entry(frame_cuadrilatero)
entry_lat1_s_cuad.grid(column=1, row=2)

ttk.Label(frame_cuadrilatero, text="Latitud final - Grados:").grid(column=0, row=3)
entry_lat2_g_cuad = ttk.Entry(frame_cuadrilatero)
entry_lat2_g_cuad.grid(column=1, row=3)

ttk.Label(frame_cuadrilatero, text="Minutos:").grid(column=0, row=4)
entry_lat2_m_cuad = ttk.Entry(frame_cuadrilatero)
entry_lat2_m_cuad.grid(column=1, row=4)

ttk.Label(frame_cuadrilatero, text="Segundos:").grid(column=0, row=5)
entry_lat2_s_cuad = ttk.Entry(frame_cuadrilatero)
entry_lat2_s_cuad.grid(column=1, row=5)

ttk.Label(frame_cuadrilatero, text="Longitud inicial - Grados:").grid(column=0, row=6)
entry_lon1_g_cuad = ttk.Entry(frame_cuadrilatero)
entry_lon1_g_cuad.grid(column=1, row=6)

ttk.Label(frame_cuadrilatero, text="Minutos:").grid(column=0, row=7)
entry_lon1_m_cuad = ttk.Entry(frame_cuadrilatero)
entry_lon1_m_cuad.grid(column=1, row=7)

ttk.Label(frame_cuadrilatero, text="Segundos:").grid(column=0, row=8)
entry_lon1_s_cuad = ttk.Entry(frame_cuadrilatero)
entry_lon1_s_cuad.grid(column=1, row=8)

ttk.Label(frame_cuadrilatero, text="Longitud final - Grados:").grid(column=0, row=9)
entry_lon2_g_cuad = ttk.Entry(frame_cuadrilatero)
entry_lon2_g_cuad.grid(column=1, row=9)

ttk.Label(frame_cuadrilatero, text="Minutos:").grid(column=0, row=10)
entry_lon2_m_cuad = ttk.Entry(frame_cuadrilatero)
entry_lon2_m_cuad.grid(column=1, row=10)

ttk.Label(frame_cuadrilatero, text="Segundos:").grid(column=0, row=11)
entry_lon2_s_cuad = ttk.Entry(frame_cuadrilatero)
entry_lon2_s_cuad.grid(column=1, row=11)

ttk.Button(frame_cuadrilatero, text="Calcular Área del Cuadrilátero", command=calcular_area_cuadrilatero_gui).grid(column=0, row=12, columnspan=2)

# Inicializar la visibilidad de los campos
actualizar_campos()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
