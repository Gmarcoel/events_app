

# M Enjoy - Sistema de Recomendación de Eventos en Madrid

Este proyecto es una prueba de concepto para una página web de eventos en Madrid, M Enjoy, que incorpora un algoritmo de recomendación específico impulsado por inteligencia artificial. El proyecto consta de tres componentes principales:

### 1. ETL (Extract, Transform, Load)
- Utiliza APIs y scraping web para recopilar datos de eventos
- Procesa y categoriza datos utilizando inteligencia artificial basada en Python
- La categorización se realiza mediante técnicas de aprendizaje automático
- El código de esta parte se encuentra en el directorio `src/etl`

### 2. Base de datos (MongoDB)
- Gestiona los datos estructurados de eventos
- Se utiliza MongoDB como solución de base de datos
- Los datos se almacenan y recuperan para el uso de la aplicación
- El código relacionado con la base de datos se encuentra en el directorio `src/database`

### 3. App (Frontend con Flask)
- Aplicación frontend utilizando Python y Flask
- Interactúa con los datos procesados en la base de datos
- Proporciona una interfaz de usuario para interactuar con el sistema de recomendación
- El código de la aplicación se encuentra en el directorio `src/app`

### Herramientas Compartidas
- El proyecto emplea un sistema de herramientas compartidas para acceder a funcionalidades externas
- Estas herramientas están escritas en Python y se almacenan en el directorio `src/tools`

### Ejecución
- El primer paso, necesario para el correcto funcionamiento del programa es añadir claves de APIs correspondientes a los servicios de [AEMET](https://opendata.aemet.es/) en el archivo meteorology.py (tools), y de [Google Maps](https://developers.google.com/maps) en list_page.html y event_detail, además de como variable global MAPS_API_KEY en el enviroment.
- Cada componente se ejecuta en un contenedor Docker separado
- Utiliza Docker Compose dentro del directorio `docker` o ejecuta el script `execute.sh` para iniciar todos los componentes simultáneamente
- Nota: La ejecución del proceso ETL lleva mucho tiempo (varias horas, dependiendo del sistema)
- Como prueba de concepto, el proceso ETL está diseñado para ejecutarse solo una vez, verificando si la base de datos existe; si está presente, no volverá a ejecutar el ETL
- Para volver a ejecutar el ETL, ejecuta `docker rm docker-mongo-1` y reinicia la aplicación

### Notas Importantes
- Debido al largo tiempo de ejecución del proceso ETL, se recomienda ejecutarlo con moderación
- Para reiniciar todo el proceso, elimina el contenedor Docker de MongoDB `docker rm docker-mongo-1` y reinicia la aplicación

