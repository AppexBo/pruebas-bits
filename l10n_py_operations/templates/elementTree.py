import xml.etree.ElementTree as ET
import re

# Cargar el archivo XSD
xsd_file = './l10n_py/l10n_py_operations/templates/DE_Types_v150.xsd'  # Reemplaza con la ruta a tu archivo XSD


# Espacio de nombres en el archivo XSD
namespace = {'xs': 'http://www.w3.org/2001/XMLSchema'}

# Función para extraer las definiciones de simpleType en un diccionario
def extract_simple_types(xsd_file, tag_name):
    tree = ET.parse(xsd_file)
    root = tree.getroot()
    simple_types = {}
    for simple_type in root.findall('xs:simpleType', namespace):
        name = simple_type.get('name')
        if name == tag_name:
            print(name)
        restriction = simple_type.find('xs:restriction', namespace)
        
        if restriction is not None:
            # Extraer el patrón si existe
            pattern = restriction.find('xs:pattern', namespace)
            if pattern is not None:
                simple_types[name] = {
                    'type': 'pattern',
                    'value': pattern.get('value')
                }
            
            # Extraer minLength y maxLength si existen
            min_length = restriction.find('xs:minLength', namespace)
            max_length = restriction.find('xs:maxLength', namespace)
            
            if min_length is not None or max_length is not None:
                simple_types[name] = {
                    'type': 'length',
                    'minLength': min_length.get('value') if min_length is not None else None,
                    'maxLength': max_length.get('value') if max_length is not None else None
                }
    return simple_types

# Función para validar el XML
def validate_xml(str_xml, simple_types, tag_name):
    try:
        # Extraer el valor del XML
        root_xml = ET.fromstring(str_xml)
        value = root_xml.text
        
        if value is None:
            return False, f"{tag_name}, El valor está vacío"

        # Buscar el tipo simple correspondiente
        simple_type = simple_types.get(tag_name)
        
        if simple_type:
            if simple_type['type'] == 'pattern':
                # Validar con patrón
                pattern = simple_type['value']
                if re.fullmatch(pattern, value):
                    return True, "Validación exitosa"
                else:
                    return False, f"{tag_name}, No coincide con el patrón"
            
            elif simple_type['type'] == 'length':
                min_length = simple_type.get('minLength')
                max_length = simple_type.get('maxLength')
                if min_length and len(value) < int(min_length):
                    return False, f"La longitud mínima es {min_length}"
                if max_length and len(value) > int(max_length):
                    return False, f"La longitud máxima es {max_length}"
                return True, "Validación exitosa"
        
        return False, f"{tag_name}, Tipo no encontrado"
    
    except ET.ParseError:
        return False, "Error al analizar el XML"

# Extraer tipos simples
simple_types = extract_simple_types(xsd_file, 'tEmail')

# Ejemplo con un email válido
srt_xml_valid = """<tEmailRec>hinojosafloresluisfernando@gmail.com</tEmailRec>"""
is_valid_valid, message_valid = validate_xml(srt_xml_valid, simple_types, 'tEmail')
print("Resultado de validación para tEmail (válido):", message_valid)
