# Algoritmo Genético

Este proyecto implementa un algoritmo genético en Python. A continuación, se detallan las instrucciones para ejecutar el programa y una breve descripción de su funcionamiento.

## Requisitos

- Python > 3.11

## Instalación

1. Clona este repositorio en tu máquina local:
    ```bash
    git clone https://github.com/tu_usuario/algoritmo-genetico.git
    ```
2. Navega al directorio del proyecto:
    ```bash
    cd algoritmo-genetico
    ```
3. (Opcional) Crea un entorno virtual y actívalo:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```
4. Instala las dependencias necesarias:
    ```bash
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar el programa, simplemente corre el archivo `main.py`:
```bash
python main.py
```

## Descripción

El archivo `main.py` contiene la implementación principal del algoritmo genético. A continuación, se describe brevemente su estructura y funcionamiento:

- **Inicialización**: Se genera una población inicial de soluciones aleatorias.
- **Evaluación**: Cada solución en la población se evalúa utilizando una función de aptitud.
- **Selección**: Se seleccionan las mejores soluciones para reproducirse.
- **Cruzamiento**: Se combinan pares de soluciones para crear nuevas soluciones.
- **Mutación**: Se aplican pequeñas modificaciones aleatorias a las nuevas soluciones.
- **Reemplazo**: Las nuevas soluciones reemplazan a las antiguas en la población.
- **Iteración**: El proceso se repite durante un número determinado de generaciones o hasta que se cumpla un criterio de parada.

## Menú de Opciones

Al ejecutar `main.py`, se presenta un menú con las siguientes opciones:

1. **Ejecutar experimento personalizado**: Permite al usuario ingresar manualmente los parámetros del algoritmo genético y ejecutar un experimento con esos parámetros.
2. **Ejecutar experimentos con múltiples configuraciones predefinidas**: Ejecuta una serie de experimentos con diferentes configuraciones predefinidas del algoritmo genético. Este proceso puede tardar varias horas.
3. **Ejecutar experimento usando aleatoriamente una de las mejores soluciones obtenidas de los experimentos**: Selecciona aleatoriamente una de las mejores configuraciones obtenidas de experimentos previos y ejecuta un nuevo experimento con esa configuración.
4. **Mostrar los mejores resultados obtenidos en los experimentos**: Muestra un análisis de los mejores resultados obtenidos en los experimentos previos.
5. **Salir**: Termina la ejecución del programa.

## Ejecutable compilado

El proyecto tiene dentro de la carpeta dist, un archivo ejecutable que permite correrlo facilmente en windows sin necesidad de utilizar python directamente en caso de que desee probar el programa sin cambios en el codigo.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT.
