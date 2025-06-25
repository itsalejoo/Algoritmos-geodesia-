import math
import matplotlib.pyplot as plt

def calcular_posicion_geodesica(lat1, lon1, azimut, distancia):
    a = 6378137.0  # Semieje mayor [m]
    f = 1 / 298.257223563
    b = a * (1 - f)  # Semieje menor

    # Conversión a radianes
    phi1 = math.radians(lat1)
    lambda1 = math.radians(lon1)
    alpha1 = math.radians(azimut)

    # Cálculos intermedios
    U1 = math.atan2((1 - f) * math.sin(phi1), math.cos(phi1))
    sigma1 = math.atan2(math.tan(U1), math.cos(alpha1))
    sin_alpha = math.cos(U1) * math.sin(alpha1)
    cos2_alpha = 1 - sin_alpha**2

    # Coeficientes
    u2 = cos2_alpha * ((a**2 - b**2) / b**2)
    A = 1 + (u2 / 16384) * (4096 + u2 * (-768 + u2 * (320 - 175 * u2)))
    B = (u2 / 1024) * (256 + u2 * (-128 + u2 * (74 - 47 * u2)))

    # Sigma angular
    sigma = distancia / (b * A)

    # Iteración
    for _ in range(2):
        cos2sigma = math.cos(2 * sigma1 + sigma)
        sin_sigma = math.sin(sigma)
        cos_sigma = math.cos(sigma)
        delta_sigma = B * sin_sigma * (cos2sigma + 
                     (B/4) * (cos_sigma * (-1 + 2 * cos2sigma**2) - 
                     (B/6) * cos2sigma * (-3 + 4 * sin_sigma**2) * (-3 + 4 * cos2sigma**2)))
        sigma = distancia / (b * A) + delta_sigma

    # Cálculo de coordenadas finales
    phi2 = math.atan2(math.sin(U1) * math.cos(sigma) + math.cos(U1) * math.sin(sigma) * math.cos(alpha1),
                      (1 - f) * math.sqrt(sin_alpha**2 + (math.sin(U1) * math.sin(sigma) - math.cos(U1) * math.cos(sigma) * math.cos(alpha1))**2))

    lambda2 = lambda1 + math.atan2(math.sin(sigma) * math.sin(alpha1),
                                  math.cos(U1) * math.cos(sigma) - math.sin(U1) * math.sin(sigma) * math.cos(alpha1))

    # Azimut inverso original
    alpha2 = math.atan2(sin_alpha, -math.sin(U1) * math.sin(sigma) + math.cos(U1) * math.cos(sigma) * math.cos(alpha1))
    alpha2_deg = math.degrees(alpha2)

    # Normalizar a rango [0, 360°]
    if alpha2_deg < 0:
        alpha2_deg += 360

    # Azimut inverso corregido matemáticamente
    if alpha2_deg <= 180:
        azimut_inverso_corregido = alpha2_deg + 180
    else:
        azimut_inverso_corregido = alpha2_deg - 180

    return math.degrees(phi2), math.degrees(lambda2), alpha2_deg, azimut_inverso_corregido

# Entrada de usuario
print("Cálculo de Posición Geodésica")
lat1 = float(input("Latitud inicial (grados): "))
lon1 = float(input("Longitud inicial (grados): "))
azimut = float(input("Acimut inicial (grados): "))
distancia = float(input("Distancia (metros): "))

# Cálculo
lat2, lon2, az_inv_orig, az_inv_corr = calcular_posicion_geodesica(lat1, lon1, azimut, distancia)

# Resultados
print(f"\nPosición final: Lat {lat2:.7f}°, Lon {lon2:.7f}°")
print(f"Azimut inverso original: {az_inv_orig:.7f}°")
print(f"Azimut inverso corregido: {az_inv_corr:.7f}°")

# Generación de gráfico
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_title('Proyección Geodésica', fontsize=14)
ax.plot(lon1, lat1, 'ro', markersize=8, label='Punto Inicial')
ax.plot(lon2, lat2, 'bo', markersize=8, label='Punto Final')
ax.arrow(lon1, lat1, (lon2-lon1)*0.9, (lat2-lat1)*0.9, 
         head_width=0.3, head_length=0.4, fc='g', ec='g', label='Trayectoria')
ax.set_xlabel('Longitud [°]', fontsize=12)
ax.set_ylabel('Latitud [°]', fontsize=12)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(loc='best')
plt.tight_layout()
plt.savefig('proyeccion_geodesica.png', dpi=300)
print("\n proyeccion_geodesica.png'")
plt.show()
