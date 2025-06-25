import math
from decimal import Decimal, getcontext, ROUND_HALF_UP
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from tkinter import ttk

# Configurar la precisión global para el método de bisección
getcontext().prec = 28  # Precisión de 28 dígitos decimales

# Funciones para el método de triseción
def convertir_a_decimal(grados, minutos, segundos):
    return Decimal(grados) + (Decimal(minutos) / Decimal(60)) + (Decimal(segundos) / Decimal(3600))

def calcular_distancias(a, b, c):
    """
    Calcula las distancias entre los puntos A, B y C.
    """
    E_a, N_a = a
    E_b, N_b = b
    E_c, N_c = c

    distancia_ab = math.sqrt((E_b - E_a)*2 + (N_b - N_a)*2)
    distancia_bc = math.sqrt((E_c - E_b)*2 + (N_c - N_b)*2)
    distancia_ac = math.sqrt((E_c - E_a)*2 + (N_c - N_a)*2)

    return distancia_ab, distancia_bc, distancia_ac

def calcular_angulos_internos(distancias):
    """
    Calcula los ángulos internos del triángulo formado por los puntos A, B y C usando el teorema del coseno.
    """
    ab, bc, ac = distancias

    A = math.degrees(math.acos((bc*2 + ac2 - ab*2) / (2 * bc * ac)))
    B = math.degrees(math.acos((ab*2 + ac2 - bc*2) / (2 * ab * ac)))
    C = math.degrees(math.acos((ab*2 + bc2 - ac*2) / (2 * ab * bc)))

    return A, B, C

def cotangente(angulo):
    """
    Calcula la cotangente de un ángulo en grados.
    """
    return 1 / math.tan(math.radians(angulo))

def calcular_constantes_k(angulos, azimut_a, azimut_b, azimut_c):
    """
    Calcula las constantes k1, k2 y k3.
    """
    A, B, C = angulos

    k1 = 1 / (cotangente(A) - cotangente(azimut_a))
    k2 = 1 / (cotangente(B) - cotangente(azimut_b))
    k3 = 1 / (cotangente(C) - cotangente(azimut_c))

    return k1, k2, k3

def calcular_coordenadas_p(a, b, c, azimut_a, azimut_b, azimut_c):
    """
    Calcula las coordenadas del punto P usando el método inverso de trisección.
    """
    distancias = calcular_distancias(a, b, c)
    angulos = calcular_angulos_internos(distancias)
    k1, k2, k3 = calcular_constantes_k(angulos, azimut_a, azimut_b, azimut_c)

    E_a, N_a = a
    E_b, N_b = b
    E_c, N_c = c

    E_p = (k1 * E_a + k2 * E_b + k3 * E_c) / (k1 + k2 + k3)
    N_p = (k1 * N_a + k2 * N_b + k3 * N_c) / (k1 + k2 + k3)

    return E_p, N_p

def convertir_a_radianes(grados, minutos, segundos):
    """
    Convierte grados, minutos y segundos a radianes.
    """
    grados_decimales = grados + minutos / 60 + segundos / 3600
    return math.radians(grados_decimales)

def cot(x):
    return Decimal(1) / Decimal(math.tan(x))

def verificar_angulos(x, y, z):
    if x == 90 and y == 90 and z == 90:
        print("Error: Los ángulos forman un cuadrado.")
        return False
    return True

def generar_grafica(a, b, c, p):
    """
    Genera una gráfica con los puntos A, B, C y P.
    """
    fig, ax = plt.subplots()
    ax.plot([a[0], b[0]], [a[1], b[1]], 'ro-', label='A-B')
    ax.plot([b[0], c[0]], [b[1], c[1]], 'go-', label='B-C')
    ax.plot([c[0], a[0]], [c[1], a[1]], 'bo-', label='C-A')
    ax.plot(p[0], p[1], 'ko', label='P')

    # Líneas punteadas desde A, B y C hasta P
    ax.plot([a[0], p[0]], [a[1], p[1]], 'r--')
    ax.plot([b[0], p[0]], [b[1], p[1]], 'g--')
    ax.plot([c[0], p[0]], [c[1], p[1]], 'b--')

    ax.annotate('A', (a[0], a[1]), textcoords="offset points", xytext=(0,10), ha='center')
    ax.annotate('B', (b[0], b[1]), textcoords="offset points", xytext=(0,10), ha='center')
    ax.annotate('C', (c[0], c[1]), textcoords="offset points", xytext=(0,10), ha='center')
    ax.annotate('P', (p[0], p[1]), textcoords="offset points", xytext=(0,10), ha='center')

    ax.set_xlabel('Este')
    ax.set_ylabel('Norte')
    ax.legend()
    ax.grid(True)
    plt.show()

def calcular():
    a = (float(entry_E_a.get()), float(entry_N_a.get()))
    b = (float(entry_E_b.get()), float(entry_N_b.get()))
    c = (float(entry_E_c.get()), float(entry_N_c.get()))

    azimut_a = convertir_a_radianes(float(entry_azimut_a_g.get()), float(entry_azimut_a_m.get()), float(entry_azimut_a_s.get()))
    azimut_b = convertir_a_radianes(float(entry_azimut_b_g.get()), float(entry_azimut_b_m.get()), float(entry_azimut_b_s.get()))
    azimut_c = convertir_a_radianes(float(entry_azimut_c_g.get()), float(entry_azimut_c_m.get()), float(entry_azimut_c_s.get()))

    coordenadas_p = calcular_coordenadas_p(a, b, c, azimut_a, azimut_b, azimut_c)
    distancias = calcular_distancias(a, b, c)

    label_result.config(text=f"Coordenadas de P: E={coordenadas_p[0]:.6f}, N={coordenadas_p[1]:.6f}\n"
                             f"Distancias: AB={distancias[0]:.6f}, BC={distancias[1]:.6f}, AC={distancias[2]:.6f}")

    generar_grafica(a, b, c, coordenadas_p)

# Funciones para el método de bisección
def cot(angle_deg):
    """Función para calcular la cotangente dado un ángulo en grados utilizando alta precisión."""
    angle_rad = Decimal(math.radians(angle_deg))  # Convertir el ángulo a radianes con alta precisión
    return Decimal(1) / Decimal(math.tan(angle_rad))  # Retornar la cotangente utilizando Decimal

def calcular_punto_p1(N_A, E_A, N_B, E_B, alpha, beta):
    """Calcula las coordenadas del punto P utilizando el método de bisección con alta precisión."""
    
    # Convertir las coordenadas y los ángulos a tipo Decimal para mayor precisión
    N_A = Decimal(N_A)
    E_A = Decimal(E_A)
    N_B = Decimal(N_B)
    E_B = Decimal(E_B)
    
    # Calcular las cotangentes de los ángulos con alta precisión
    cot_alpha = cot(alpha)
    cot_beta = cot(beta)
    
    # Calcular las coordenadas Este y Norte del punto P con fórmulas usando alta precisión
    E_P = ((N_B - N_A) + E_A * cot_beta + E_B * cot_alpha) / (cot_alpha + cot_beta)
    N_P = ((E_A - E_B) + N_A * cot_beta + N_B * cot_alpha) / (cot_alpha + cot_beta)
    
    return N_P, E_P

def metodo_biseccion():
    N_A = Decimal(NA_var.get())
    E_A = Decimal(EA_var.get())
    N_B = Decimal(NB_var.get())
    E_B = Decimal(EB_var.get())
    alpha = convertir_a_decimal(int(alpha_grados_var.get()), int(alpha_minutos_var.get()), float(alpha_segundos_var.get()))
    beta = convertir_a_decimal(int(beta_grados_var.get()), int(beta_minutos_var.get()), float(beta_segundos_var.get()))
    
    N_P, E_P = calcular_punto_p1(N_A, E_A, N_B, E_B, alpha, beta)
    N_P = N_P.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    E_P = E_P.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)
    messagebox.showinfo("Coordenadas del punto P", f"Norte (N_P): {N_P:.3f}\nEste (E_P): {E_P:.3f}")
    graficar_puntos(N_A, E_A, N_B, E_B, N_P, E_P)

def graficar_puntos(NA, EA, NB, EB, NP, EP):
    plt.figure()
    plt.plot([EA, EB], [NA, NB], 'bo-', label='Línea AB')
    plt.plot([EA, EP], [NA, NP], 'ro-', label='Línea AP')
    plt.plot([EB, EP], [NB, NP], 'go-', label='Línea BP')
    plt.scatter([EA, EB, EP], [NA, NB, NP], color=['blue', 'blue', 'red'])
    plt.text(EA, NA, f'A ({EA:.3f}, {NA:.3f})', fontsize=12, ha='right')
    plt.text(EB, NB, f'B ({EB:.3f}, {NB:.3f})', fontsize=12, ha='right')
    plt.text(EP, NP, f'P ({EP:.3f}, {NP:.3f})', fontsize=12, ha='right')
    plt.xlabel('Coordenada Este')
    plt.ylabel('Coordenada Norte')
    plt.title('Gráfico de los puntos A, B y P')
    plt.legend()
    plt.grid(True)
    plt.show()

# Crear la ventana principal
root = tk.Tk()
root.title("Selección de Método")

# Variables para almacenar las entradas del usuario
punto_var = tk.StringVar()
suma_angulos_var = tk.StringVar()
NA_var = tk.StringVar()
EA_var = tk.StringVar()
NB_var = tk.StringVar()
EB_var = tk.StringVar()
NC_var = tk.StringVar()
EC_var = tk.StringVar()
x_grados_var = tk.StringVar()
x_minutos_var = tk.StringVar()
x_segundos_var = tk.StringVar()
y_grados_var = tk.StringVar()
y_minutos_var = tk.StringVar()
y_segundos_var = tk.StringVar()
z_grados_var = tk.StringVar()
z_minutos_var = tk.StringVar()
z_segundos_var = tk.StringVar()
alpha_grados_var = tk.StringVar()
alpha_minutos_var = tk.StringVar()
alpha_segundos_var = tk.StringVar()
beta_grados_var = tk.StringVar()
beta_minutos_var = tk.StringVar()
beta_segundos_var = tk.StringVar()

# Crear widgets para el método de bisección
tk.Label(root, text="Método de Bisección").grid(row=13, column=0, columnspan=2)
tk.Label(root, text="Coordenada Norte de A:").grid(row=14, column=0)
tk.Entry(root, textvariable=NA_var).grid(row=14, column=1)
tk.Label(root, text="Coordenada Este de A:").grid(row=15, column=0)
tk.Entry(root, textvariable=EA_var).grid(row=15, column=1)
tk.Label(root, text="Coordenada Norte de B:").grid(row=16, column=0)
tk.Entry(root, textvariable=NB_var).grid(row=16, column=1)
tk.Label(root, text="Coordenada Este de B:").grid(row=17, column=0)
tk.Entry(root, textvariable=EB_var).grid(row=17, column=1)
tk.Label(root, text="Ángulo alfa (grados, minutos, segundos):").grid(row=18, column=0)
tk.Entry(root, textvariable=alpha_grados_var).grid(row=18, column=1)
tk.Entry(root, textvariable=alpha_minutos_var).grid(row=18, column=2)
tk.Entry(root, textvariable=alpha_segundos_var).grid(row=18, column=3)
tk.Label(root, text="Ángulo beta (grados, minutos, segundos):").grid(row=19, column=0)
tk.Entry(root, textvariable=beta_grados_var).grid(row=19, column=1)
tk.Entry(root, textvariable=beta_minutos_var).grid(row=19, column=2)
tk.Entry(root, textvariable=beta_segundos_var).grid(row=19, column=3)
tk.Button(root, text="Calcular Bisección", command=metodo_biseccion).grid(row=20, column=0, columnspan=2)

# Crear y colocar los widgets
ttk.Label(root, text="Coordenadas de A (Este, Norte):").grid(column=0, row=0, padx=10, pady=5)
entry_E_a = ttk.Entry(root)
entry_N_a = ttk.Entry(root)
entry_E_a.grid(column=1, row=0, padx=10, pady=5)
entry_N_a.grid(column=2, row=0, padx=10, pady=5)

ttk.Label(root, text="Coordenadas de B (Este, Norte):").grid(column=0, row=1, padx=10, pady=5)
entry_E_b = ttk.Entry(root)
entry_N_b = ttk.Entry(root)
entry_E_b.grid(column=1, row=1, padx=10, pady=5)
entry_N_b.grid(column=2, row=1, padx=10, pady=5)

ttk.Label(root, text="Coordenadas de C (Este, Norte):").grid(column=0, row=2, padx=10, pady=5)
entry_E_c = ttk.Entry(root)
entry_N_c = ttk.Entry(root)
entry_E_c.grid(column=1, row=2, padx=10, pady=5)
entry_N_c.grid(column=2, row=2, padx=10, pady=5)

ttk.Label(root, text="Azimut A (Grados, Minutos, Segundos):").grid(column=0, row=3, padx=10, pady=5)
entry_azimut_a_g = ttk.Entry(root, width=5)
entry_azimut_a_m = ttk.Entry(root, width=5)
entry_azimut_a_s = ttk.Entry(root, width=5)
entry_azimut_a_g.grid(column=1, row=3, padx=5, pady=5)
entry_azimut_a_m.grid(column=2, row=3, padx=5, pady=5)
entry_azimut_a_s.grid(column=3, row=3, padx=5, pady=5)

ttk.Label(root, text="Azimut B (Grados, Minutos, Segundos):").grid(column=0, row=4, padx=10, pady=5)
entry_azimut_b_g = ttk.Entry(root, width=5)
entry_azimut_b_m = ttk.Entry(root, width=5)
entry_azimut_b_s = ttk.Entry(root, width=5)
entry_azimut_b_g.grid(column=1, row=4, padx=5, pady=5)
entry_azimut_b_m.grid(column=2, row=4, padx=5, pady=5)
entry_azimut_b_s.grid(column=3, row=4, padx=5, pady=5)

ttk.Label(root, text="Azimut C (Grados, Minutos, Segundos):").grid(column=0, row=5, padx=10, pady=5)
entry_azimut_c_g = ttk.Entry(root, width=5)
entry_azimut_c_m = ttk.Entry(root, width=5)
entry_azimut_c_s = ttk.Entry(root, width=5)
entry_azimut_c_g.grid(column=1, row=5, padx=5, pady=5)
entry_azimut_c_m.grid(column=2, row=5, padx=5, pady=5)
entry_azimut_c_s.grid(column=3, row=5, padx=5, pady=5)

ttk.Button(root, text="Calcular", command=calcular).grid(column=0, row=6, columnspan=4, padx=10, pady=10)

label_result = ttk.Label(root, text="Coordenadas de P: ")
label_result.grid(column=0, row=7, columnspan=4, padx=10, pady=10)

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()