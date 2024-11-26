from rembg import remove
from PIL import Image
import os

def remove_background():
    image_path = input("Ingrese la ruta de la imagen: ")
    
    if not os.path.isfile(image_path):
        print("La ruta ingresada no es válida o el archivo no existe.")
        return
    
    with open(image_path, "rb") as input_file:
        result = remove(input_file.read())
    
    file_dir, file_name = os.path.split(image_path)
    file_name_no_ext, file_ext = os.path.splitext(file_name)
    output_path = os.path.join(file_dir, f"{file_name_no_ext}_nobg{file_ext}")
    
    with open(output_path, "wb") as output_file:
        output_file.write(result)
    
    print(f"Imagen procesada y guardada en: {output_path}")

remove_background ()