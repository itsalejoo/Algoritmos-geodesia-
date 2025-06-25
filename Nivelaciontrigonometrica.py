import math
import matplotlib.pyplot as plt

def dms_a_grados_decimal(grados, minutos, segundos):
    return grados + minutos / 60 + segundos / 3600

def nivelacion_trigonometrica():
    print("NIVELACIÓN TRIGONOMÉTRICA")
    
    # Preguntar si desea ingresar cotas
    respuesta = input("¿Desea ingresar las cotas? (s/n): ").strip().lower()
    
    # Entrada de datos comunes
    distancia = float(input("\nIngrese la distancia inclinada (D) en metros: "))

    print("\nIngrese el ángulo zenital:")
    grados = int(input("  Grados: "))
    minutos = int(input("  Minutos: "))
    segundos = float(input("  Segundos: "))

    angulo_decimal = dms_a_grados_decimal(grados, minutos, segundos)

    altura_instrumento = float(input("\nIngrese la altura del instrumento (h_i) en metros: "))
    altura_prisma = float(input("Ingrese la altura del punto visado (h_r) en metros: "))
    
    # Manejo de cotas según respuesta
    if respuesta == 's':
        cota_inicial = float(input("\nIngrese la cota del punto donde está el instrumento (m): "))
    else:
        cota_inicial = 0.0

    # Cálculo de ΔH
    angulo_complementario_rad = math.radians(90 - angulo_decimal)
    delta_h = distancia * math.sin(angulo_complementario_rad) + altura_instrumento - altura_prisma
    cota_final = cota_inicial + delta_h

    # Resultados según tipo de cálculo
    print(f"\n{'='*50}")
    print("RESULTADOS:")
    print(f"{'='*50}")
    print(f"Diferencia de altura (ΔH): {delta_h:.3f} metros")
    if respuesta == 's':
        print(f"Cota del punto visado: {cota_final:.3f} metros")
    else:
        print(f"Altura relativa del punto visado: {cota_final:.3f} metros")
    print(f"Distancia horizontal: {distancia * math.cos(angulo_complementario_rad):.3f} metros")
    print(f"Ángulo zenital: {angulo_decimal:.4f}°")

    # Coordenadas para graficar
    x1 = 0
    y1 = cota_inicial + altura_instrumento
    x2 = distancia * math.cos(angulo_complementario_rad)
    y2 = cota_final

    # Gráfica
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot([x1, x2], [y1, y2], 'bo-', linewidth=2, markersize=8, label="Línea de visión")
    ax.hlines(y1, x1, x2, colors='green', linestyles='dashed', linewidth=2, label="Altura del instrumento")
    ax.hlines(y2, x2, x2 + 5, colors='red', linestyles='dotted', linewidth=2, label="Punto visado")

    # Etiquetas mejoradas
    ax.annotate(f"Instrumento\nCota: {cota_inicial:.2f} m",
                xy=(x1, y1), xytext=(-15, y1 + 3),
                arrowprops=dict(arrowstyle="->", color='black'),
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.7),
                fontsize=10)

    ax.annotate(f"Punto visado\n{'Cota' if respuesta == 's' else 'Altura'}: {cota_final:.2f} m",
                xy=(x2, y2), xytext=(x2 - 15, y2 - 8),
                arrowprops=dict(arrowstyle="->", color='black'),
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7),
                fontsize=10)

    # Información adicional en el gráfico
    info_text = f"D = {distancia:.1f} m\nZ = {angulo_decimal:.2f}°\nΔH = {delta_h:.3f} m"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=9,
            verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

    ax.set_xlabel("Distancia horizontal (m)", fontsize=12)
    ax.set_ylabel("Altura / Cota (m)", fontsize=12)
    ax.set_title(f"Nivelación Trigonométrica {'con Cotas' if respuesta == 's' else 'sin Cotas'}", fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    # Margen automático
    margen = max(10, abs(max(y1, y2) - min(y1, y2)) * 0.1)
    ax.set_xlim(min(x1, x2) - margen, max(x1, x2) + margen)
    ax.set_ylim(min(y1, y2) - margen, max(y1, y2) + margen)

    plt.tight_layout()
    plt.savefig('nivelacion_trigonometrica.png', dpi=300, bbox_inches='tight')
    print(f"\nImagen guardada como 'nivelacion_trigonometrica.png'")
    plt.show()

def main():
    """Función principal con bucle para múltiples cálculos"""
    print("="*60)
    print("    PROGRAMA DE NIVELACIÓN TRIGONOMÉTRICA")
    print("="*60)
    
    contador_calculos = 1
    
    while True:
        print(f"\nCÁLCULO #{contador_calculos}")
        print("-" * 30)
        
        try:
            nivelacion_trigonometrica()
            
            print(f"\n{'='*50}")
            continuar = input("¿Desea realizar otro cálculo? (s/n): ").strip().lower()
            
            if continuar != 's':
                print("\n¡Gracias por usar el programa!")
                print("="*60)
                break
            
            contador_calculos += 1
            print("\n" + "="*60)
            
        except ValueError:
            print("\n Error: Por favor ingrese valores numéricos válidos.")
            continuar = input("¿Desea intentar nuevamente? (s/n): ").strip().lower()
            if continuar != 's':
                break
        except Exception as e:
            print(f"\n Error inesperado: {e}")
            continuar = input("¿Desea intentar nuevamente? (s/n): ").strip().lower()
            if continuar != 's':
                break

# Ejecutar programa principal
if __name__ == "__main__":
    main()
