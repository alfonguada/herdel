import os

# Nombre de la carpeta que contiene los archivos HTML
TEMPLATES_DIR = "templates"
SCRIPT_TAG = '<script src="https://kit.fontawesome.com/a991bc5d64.js" crossorigin="anonymous"></script>\n'

def insert_script_in_templates(directory, script_tag):
    """
    Busca archivos HTML en el directorio especificado, y agrega un script antes del primer <style>.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):  # Procesar solo archivos HTML
                file_path = os.path.join(root, file)
                try:
                    # Leer el contenido del archivo
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()

                    # Revisar si ya contiene el script para evitar duplicados
                    if any(script_tag.strip() in line for line in lines):
                        print(f"El script ya existe en: {file_path}")
                        continue

                    # Buscar la posición del primer <style> e insertar el script
                    for i, line in enumerate(lines):
                        if "<style>" in line:
                            lines.insert(i, script_tag)
                            break

                    # Guardar los cambios en el archivo
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(lines)

                    print(f"Script insertado en: {file_path}")

                except Exception as e:
                    print(f"Error procesando {file_path}: {e}")

# Ejecutar el script en la carpeta templates
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    templates_path = os.path.join(current_dir, TEMPLATES_DIR)
    insert_script_in_templates(templates_path, SCRIPT_TAG)
