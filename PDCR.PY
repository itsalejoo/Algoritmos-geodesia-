import math
import matplotlib.pyplot as plt

# Función que resuelve el problema directo de coordenadas
def problema_directo(x_a, y_a, distancia, azimut_grados):
    azimut_rad = math.radians(azimut_grados)
    x_b = x_a + distancia * math.sin(azimut_rad)
    y_b = y_a + distancia * math.cos(azimut_rad)
    return x_b, y_b

# Función para graficar el vector desde A hasta B
def graficar_vector(x_a, y_a, x_b, y_b):
    plt.figure(figsize=(8, 6))
    plt.plot([x_a, x_b], [y_a, y_b], 'ro-', linewidth=2, label='Vector A → B')
    plt.text(x_a, y_a, 'A', fontsize=12, ha='right', va='bottom')
    plt.text(x_b, y_b, 'B', fontsize=12, ha='left', va='bottom')
    plt.xlabel('X (Este)')
    plt.ylabel('Y (Norte)')
    plt.title('Problema Directo de Coordenadas Rectangulares')
    plt.grid(True)
    plt.axis('equal')
    plt.legend()
    plt.show()

# === INICIO DEL PROGRAMA ===
print("=== Problema Directo de Coordenadas Rectangulares ===")

# Entrada de datos por parte del usuario
try:
    x_a = float(input("Ingrese la coordenada X del punto A (en metros): "))
    y_a = float(input("Ingrese la coordenada Y del punto A (en metros): "))
    distancia = float(input("Ingrese la distancia entre A y B (en metros): "))
    azimut = float(input("Ingrese el azimut en grados decimales (ej. 313.1223): "))

    # Cálculo de coordenadas del punto B
    x_b, y_b = problema_directo(x_a, y_a, distancia, azimut)

    # Mostrar resultados
    print("\n=== Resultado ===")
    print(f"Azimut: {azimut:.6f}°")
    print(f"Coordenada X del punto B: {x_b:.3f}")
    print(f"Coordenada Y del punto B: {y_b:.3f}")

    # Graficar el vector
    graficar_vector(x_a, y_a, x_b, y_b)

except Exception as e:
    print(f"Ocurrió un error: {e}")
    