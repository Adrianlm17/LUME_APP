import polib
import os

# Ruta base del proyecto
base_dir = os.path.dirname(os.path.abspath(__file__))

# Función para compilar archivos .po a .mo
def compile_messages(locale_path):
    for root, dirs, files in os.walk(locale_path):
        for file in files:
            if file.endswith('.po'):
                po_path = os.path.join(root, file)
                mo_path = os.path.splitext(po_path)[0] + '.mo'
                po = polib.pofile(po_path)
                po.save_as_mofile(mo_path)
                print(f'Compiled {po_path} to {mo_path}')

# Compilar archivos de traducción
compile_messages(os.path.join(base_dir, 'locale'))