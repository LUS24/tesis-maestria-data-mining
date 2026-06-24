"""
Contar las partes del Código de Minería por tipo_parte.

Lee el diccionario desde data/codigo_de_mineria_actualizado_2025_08_02.py
y cuenta recursivamente todas las partes según su "tipo_parte".
"""

import sys
import os

# Agregar la raíz del proyecto al path para poder importar el diccionario
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "data"))

# Importar el diccionario norma
from codigo_de_mineria_actualizado_2025_08_02 import norma


def contar_por_tipo(partes, contador=None):
    """Recorre recursivamente las partes y cuenta por tipo_parte."""
    if contador is None:
        contador = {}

    for parte in partes:
        tipo = parte.get("tipo_parte", "desconocido")
        contador[tipo] = contador.get(tipo, 0) + 1

        # Si tiene sub-partes, recorrer recursivamente
        sub_partes = parte.get("partes", [])
        if sub_partes:
            contar_por_tipo(sub_partes, contador)

    return contador


def main():
    # Contar todas las partes del corpus
    contador = contar_por_tipo(norma.get("partes", []))

    print("=== Estadísticas del Corpus: Código de Minería Argentino ===")
    print()
    print(f"Total de partes: {sum(contador.values())}")
    print()
    print("Desglose por tipo de parte:")
    print(f"  {'Tipo de parte':<25} {'Cantidad':>8}")
    print(f"  {'-'*25} {'-'*8}")
    for tipo, cantidad in sorted(contador.items(), key=lambda x: -x[1]):
        print(f"  {tipo:<25} {cantidad:>8}")

    # Información adicional
    print()
    print("Información adicional del corpus:")
    print(f"  País: {norma.get('pais', 'N/A')}")
    print(f"  Título: {norma.get('titulo', 'N/A')}")
    print(f"  Fecha de sanción: {norma.get('fecha_sancion', 'N/A')}")
    print(f"  Fecha de última actualización: {norma.get('fecha_ultima_actualizacion', 'N/A')}")
    print(f"  Estado: {norma.get('estado', 'N/A')}")


if __name__ == "__main__":
    main()
