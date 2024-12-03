# import chardet

# # Detectar la codificación
# input_file = 'data.json'

# with open(input_file, 'rb') as f:
#     result = chardet.detect(f.read())
#     print(result)


# Cambiar la codificación del archivo a UTF-8
input_file = 'products_product.json'  # Archivo original
output_file = 'product_utf8.json'  # Archivo convertido

# Leer el archivo en UTF-16 y guardarlo como UTF-8
with open(input_file, 'r', encoding='UTF-16') as f_in:
    data = f_in.read()

with open(output_file, 'w', encoding='utf-8') as f_out:
    f_out.write(data)

print(f"Archivo convertido y guardado como {output_file}")
