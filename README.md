# Proyecto BTG Pactual - Gestión de Fondos

Este proyecto proporciona una API para gestionar la suscripción a fondos de inversión, cancelar suscripciones y revisar el historial de transacciones. También se incluye la funcionalidad de envío de notificaciones por correo electrónico y SMS.

### Nota importante

Antes de iniciar los contenedores, cambia los valores de `email` y `phone` en el script de inicialización para que coincidan con tus datos de prueba. Esto asegura que las notificaciones de correo y SMS se envíen a tus datos.

### El archivo se encuentra en la siguiente ruta: /config/script_init_db.py línea 20 y 30.

```python
new_user = {
    "_id": str(uuid.uuid4()),
    "name": "Tu Nombre",
    "email": "tu_correo@gmail.com",  # Cambiar por tu correo
    "phone": "+57300xxxxxxx",         # Cambiar por tu número de teléfono
    "balance": INITIAL_BALANCE,
    "transactions": [],
    "notification_preference": ["email", "sms"],
}
```

## Requisitos

- Docker
- Docker Compose

## Uso del Makefile

Este proyecto incluye un Makefile que automatiza varios comandos relacionados con la construcción y el manejo de contenedores Docker.

### Comandos disponibles

- **build**: Build the Docker images and containers.
- **up**: Start the Docker containers in detached mode.
- **down**: Stop the Docker containers.
- **logs**: Show the logs from the running Docker containers.
- **clean**: Stop and remove containers, networks, and volumes.
- **start**: Build, start, and show the logs for the containers.
- **build-up**: Build the Docker images and start the containers.
- **pre-commit-check**: Run pre-commit hooks to check if they are working.
- **help**: Show this help message.

## Despliegue del proyecto en local

Para desplegar el proyecto en local utilizando la última **tag** creada, sigue los siguientes pasos:

1. **Clonar el repositorio**:
   Clona el repositorio en tu máquina local utilizando el siguiente comando:

   ```bash
   git clone https://github.com/SixTanDev/BTG.git
   ```
2. Navegar al directorio del proyecto: Una vez clonado, accede al directorio del proyecto:
   ```bash
   cd BTG
   ```
3. Checkout a la tag: Realiza un checkout a la última tag que se creó para garantizar que estás trabajando con la versión estable más reciente:
    ```bash
   git checkout tags/v1.0.0
   ```
4. Construir y desplegar los contenedores: Utiliza el Makefile incluido en el proyecto para construir las imágenes y desplegar los contenedores de Docker:
    ```bash
   make build-up
   ```
5.Acceder a la aplicación:
Una vez que los contenedores se han creado y están en ejecución, puedes acceder a la aplicación a través del siguiente enlace:

[Acceder a la aplicación](http://0.0.0.0:8000/)


## Inicialización de datos

El proyecto incluye un script para inicializar la base de datos MongoDB con datos de ejemplo (usuario y fondos).

### Ejecución del script

El script se ejecuta automáticamente al iniciar los contenedores, creando un usuario con un balance inicial y varios fondos disponibles para la suscripción.

### Usuario inicial:

- **Nombre**: Emmanuel
- **Email**: sixtandev@gmail.com
- **Teléfono**: +573043543065
- **Balance inicial**: COP $500,000

### Fondos disponibles:

- FPV_BTG_PACTUAL_RECAUDADORA
- FPV_BTG_PACTUAL_ECOPETROL
- DEUDAPRIVADA
- FDO-ACCIONES
- FPV_BTG_PACTUAL_DINAMICA

## Integración continuo

El proyecto utiliza **GitHub Actions** para implementar un flujo de integración continua. Los tests unitarios y los analizadores de código como `pylint`, `black`, y `bandit` se ejecutan automáticamente en cada push y pull request, garantizando la calidad del código en cada etapa del desarrollo.
