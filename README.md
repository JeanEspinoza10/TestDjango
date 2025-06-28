# Como ejecutar el proyecto

Para el presente proyecto debemos realizar lo siguiente:
    
    1. Clonar el repositorio.
    2. Crear un entorno virtual con: python -m venv env y activarlo.
    3. Instalar las dependencias: pip instal  - r requirements.txt
    3. Crear archivo .env en la raiz del proyecto con las siguientes variables:
        '''
            PASSWORD_USERS = 'fasdsad'
            SECRET_KEY = 'fasdsd'
            DEBUG = False
        ''' 
    4. Aplicar las migraciones con el siguiente comando: python manage.py migrate
    5. Correr el servidor con el comando: python manage.py runserver

# Cómo poblar los datos
Para llenar los datos realizamos la creación de una "semilla" esto se encuentra en la carpeta ./scripts/seed.py. La ejecutamos de la siguiente manera:

    1. Actiamos el entorno virutal que creamos anteriormente.
    2. Ejecutamos: python ./scripts/seed.py

# Cómo acceder a la vista principal
Para acceder a la vista principal debemos ingresar a la ruta:
    
    http://127.0.0.1:8000/

# Extra
El presente proyecto hice el despliegue en la siguiente ruta:

    https://testupc.jespinoza.site/
