import os
import csv

def get_directory_sizes(root_dir):
    sizes = {}
    count_dirs = 0
    # Recorre el árbol de directorios de abajo hacia arriba
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        count_dirs += 1
        total = 0
        # Suma el tamaño de los archivos directos en el directorio
        for file in filenames:
            filepath = os.path.join(dirpath, file)
            try:
                if os.path.isfile(filepath):
                    total += os.path.getsize(filepath)
            except Exception as e:
                print(f"Error al obtener el tamaño de {filepath}: {e}")
        # Suma el tamaño de las subcarpetas (ya calculado previamente)
        for d in dirnames:
            subdir = os.path.join(dirpath, d)
            total += sizes.get(subdir, 0)
        sizes[dirpath] = total
    print(f"Total de directorios procesados: {count_dirs}")
    return sizes

def main():
    root_dir = input("Introduce el directorio raíz a analizar (por ejemplo, C:\\\\ o /home/usuario): ")
    # Comprobar si la ruta ingresada es un directorio válido
    if not os.path.isdir(root_dir):
        print(f"La ruta '{root_dir}' no es un directorio válido.")
        return

    print("Calculando tamaños, por favor espere...")
    sizes = get_directory_sizes(root_dir)
    
    if not sizes:
        print("No se encontraron directorios o archivos en el directorio especificado.")
        return

    # Convertir de bytes a gigabytes
    sizes_gb = {folder: size / (1024**3) for folder, size in sizes.items()}
    sorted_sizes = sorted(sizes_gb.items(), key=lambda x: x[1], reverse=True)

    print("\nTamaños de carpetas (en GB):")
    for folder, size in sorted_sizes:
        print(f"{folder}  {size:.2f} GB")

    output_file = "carpetas_tamanos.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Carpeta", "Tamaño (GB)"])
        for folder, size in sorted_sizes:
            writer.writerow([folder, f"{size:.4f}"])
    
    print(f"\nArchivo CSV generado: {output_file}")

if __name__ == "__main__":
    main()
