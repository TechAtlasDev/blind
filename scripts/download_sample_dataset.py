import os
import openneuro as on

def main():
    """
    Script para descargar datasets de OpenNeuro.
    """
    print("=== Script para descargar datasets de OpenNeuro ===")
    ds_choice = input("Ingrese el dataset (dsXXXXXX): ")

    if not ds_choice.startswith("ds"):
        print("❌ Formato inválido. Debe comenzar por 'ds'. Ejemplo: ds001810")
        return
    
    custom = input("Quieres elegir una ruta personalizada? (s/n): ").lower().strip()
    
    # Ruta por defecto: ./data/<dataset_id>
    if custom == "s":
        path_choice = input("Ingrese la ruta de descarga: ").strip()
        target_dir = os.path.abspath(path_choice)
    elif custom == "n":
        target_dir = os.path.abspath(os.path.join("data", ds_choice))
    else:
        print("❌ Opción no válida")

    # Crear la carpeta si no existe
    os.makedirs(target_dir, exist_ok=True)

    print(f"Descargando '{ds_choice}' en: {target_dir}")

    try:
        on.download(dataset=ds_choice, target_dir=target_dir)
        print(f"✅ Descarga completada: {target_dir}")
    except Exception as e:
        print(f"❌ Error al descargar el dataset '{ds_choice}': {e}")

if __name__ == "__main__":
    main()
