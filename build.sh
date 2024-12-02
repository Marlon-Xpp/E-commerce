# #!/usr/bin/env bash
# # Exit on error
# set -o errexit
# # Modify this line as needed for your package manager (pip, poetry, etc.)
# pip install -r requirements.txt
# # Convert static asset files
# python manage.py collectstatic --no-input

# python manage.py makemigrations

# # Apply any outstanding database migrations
# python manage.py migrate


# # python manage.py loaddata data.json
# python manage.py loaddata data_utf8.json




#!/usr/bin/env bash
# Exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Convertir archivos estáticos
python manage.py collectstatic --no-input

# Crear migraciones solo para la app 'main' si hay cambios
python manage.py makemigrations main

# Aplicar migraciones pendientes en todas las apps
python manage.py migrate

# Cargar datos desde el archivo fixture
python manage.py loaddata data_utf8.json