import math
import matplotlib.pyplot as plt

# Calcular azimut en grados decimales (0° a 360°)
def azimut_en_grados(delta_x, delta_y):
    azimut_rad = math.atan2(delta_x, delta_y)
    azimut_deg = math.degrees(azimut_rad)
    if azimut_deg < 0:
        azimut_deg += 360
    return azimut_deg

# Convertir azimut a rumbo (grados decimales) y cuadrante
def rumbo_y_cuadrante(azimut):
    if 0 <= azimut < 90:
        rumbo = azimut
        cuadrante = "NE"
    elif 90 <= azimut < 180:
        rumbo = 180 - azimut
        cuadrante = "SE"
    elif 180 <= azimut < 270:
        rumbo = azimut - 180
        cuadrante = "SW"
    else:  # 270 <= azimut < 360
        rumbo = 360 - azimut
        cuadrante = "NW"
    return rumbo, cuadrante

# Resolver problema inverso
def problema_inverso(x_a, y_a, x_b, y_b):
    delta_x = x_b - x_a
    delta_y = y_b - y_a
    distancia = math.hypot(delta_x, delta_y)
    azimut = azimut_en_grados(delta_x, delta_y)
    rumbo, cuadrante = rumbo_y_cuadrante(azimut)
    return distancia, azimut, rumbo, cuadrante

# Graficar vector desde A hasta B
def graficar_vector(x_a, y_a, x_b, y_b):
    plt.figure(figsize=(8, 6))
    plt.plot([x_a, x_b], [y_a, y_b], 'bo-', linewidth=2, label='Vector A → B')
    plt.text(x_a, y_a, 'A', fontsize=12, ha='right', va='bottom')
    plt.text(x_b, y_b, 'B', fontsize=12, ha='left', va='bottom')
    plt.xlabel('X (Este)')
    plt.ylabel('Y (Norte)')
    plt.title('Problema Inverso de Coordenadas Rectangulares')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()

# === PROGRAMA PRINCIPAL ===
print("=== Problema Inverso de Coordenadas Rectangulares ===")

try:
    # Entrada de datos
    x_a = float(input("Ingrese la coordenada X del punto A (en metros): "))
    y_a = float(input("Ingrese la coordenada Y del punto A (en metros): "))
    x_b = float(input("Ingrese la coordenada X del punto B (en metros): "))
    y_b = float(input("Ingrese la coordenada Y del punto B (en metros): "))

    # Cálculo
    distancia, azimut, rumbo, cuadrante = problema_inverso(x_a, y_a, x_b, y_b)

    # Mostrar resultados
    print("\n=== Resultado ===")
    print(f"Distancia entre A y B: {distancia:.3f} metros")
    print(f"Azimut: {azimut:.6f}°")
    print(f"Rumbo: {rumbo:.6f}° hacia el {cuadrante}")

    # Gráfica
    graficar_vector(x_a, y_a, x_b, y_b)

except Exception as e:
    print(f"Ocurrió un error: {e}")