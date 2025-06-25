import numpy as np
import matplotlib.pyplot as plt

def ingresar_datos(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print("Error: Ingrese un número válido")

n = int(ingresar_datos("Ingrese el número de puntos de control: "))

h = []
N = []

print("\nINGRESO DE ALTURAS ELIPSOIDALES (h)")
for i in range(n):
    h.append(ingresar_datos(f"h[{i+1}] en metros: "))

print("\nINGRESO DE ONDULACIONES DEL GEOIDE (N)")
for i in range(n):
    N.append(ingresar_datos(f"N[{i+1}] en metros: "))

h = np.array(h)
N = np.array(N)
H = np.round(h - N, 4)

# ==============================================
# NUEVOS CÁLCULOS AGREGADOS
# ==============================================
# Cálculo de niveles diferenciales entre puntos consecutivos
delta_H = np.round(np.diff(H), 4)

# Verificación de consistencia (cierre de circuito)
desnivel_total = np.round(H[-1] - H[0], 4)
suma_desniveles = np.round(np.sum(delta_H), 4)
error_cierre = np.round(suma_desniveles - desnivel_total, 4)
# ==============================================

plt.figure(figsize=(12, 6))
plt.plot(H, 'o-', color='#1f77b4', linewidth=2, markersize=8)
plt.title('Perfil de Nivelación Geodésica Diferencial', fontsize=14, pad=20)
plt.xlabel('Puntos de Control', fontsize=12)
plt.ylabel('Altura Física (m)', fontsize=12)
plt.grid(linestyle='--', alpha=0.7)
plt.xticks(ticks=range(n), labels=[f'P{i+1}' for i in range(n)])
plt.ylim(min(H)-0.5, max(H)+0.5)

for i, (hi, Ni, Hi) in enumerate(zip(h, N, H)):
    plt.annotate(f'H = {hi:.3f} - {Ni:.3f}\n= {Hi:.3f} m',
                 xy=(i, H[i]), xytext=(0, 15),
                 textcoords='offset points',
                 ha='center', va='bottom',
                 fontsize=9,
                 arrowprops=dict(arrowstyle="->", color='gray', alpha=0.5))

print("\nRESULTADOS:")
print(f"{'Punto':<6} {'h (m)':<10} {'N (m)':<10} {'H (m)':<10}")
for i in range(n):
    print(f"P{i+1:<5} {h[i]:<10.4f} {N[i]:<10.4f} {H[i]:<10.4f}")

# ==============================================
# NUEVOS RESULTADOS IMPRESOS
# ==============================================
print("\nNIVELES DIFERENCIALES:")
for i in range(len(delta_H)):
    print(f"ΔH P{i+1}-P{i+2}: {delta_H[i]:.4f} m")

print("\nVERIFICACIÓN DE CONSISTENCIA:")
print(f"Desnivel total (P1-P{n}): {desnivel_total} m")
print(f"Suma de desniveles parciales: {suma_desniveles} m")
print(f"Error de cierre: {error_cierre} m")

if abs(error_cierre) < 0.0001:
    print("\n✅ La nivelación es consistente (error < 0.0001 m)")
else:
    print(f"\n⚠️ Aviso: Error de cierre superior al permitido ({error_cierre} m)")
# ==============================================

plt.tight_layout()
plt.show()