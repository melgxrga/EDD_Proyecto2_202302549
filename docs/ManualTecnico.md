# Manual Técnico

## Proyecto 2: "Llega Rapidito"

### Universidad de San Carlos de Guatemala  
Facultad de Ingeniería  
Escuela de Ciencias y Sistemas  

---

## Descripción General

El sistema "Llega Rapidito" es una aplicación desarrollada en Python que emplea estructuras de datos avanzadas para gestionar información de clientes, vehículos, rutas y viajes. Se basa en principios de memoria dinámica, algoritmos eficientes y generación de gráficos mediante Graphviz. Este manual técnico documenta la implementación, funcionalidad y diseño de la solución.

---

## Funcionalidades Principales

1. **Gestión de Clientes:**
   - Registro de clientes en una lista circular doblemente enlazada ordenada por DPI.
   - Operaciones soportadas: agregar, modificar, eliminar, mostrar información y visualizar estructura.
   - Soporte para carga masiva desde archivos.

2. **Gestión de Vehículos:**
   - Almacenamiento en un árbol B de orden 5 usando la placa como llave.
   - Operaciones soportadas: agregar, modificar, eliminar, mostrar información y visualizar estructura.
   - Soporte para carga masiva desde archivos.

3. **Gestión de Rutas:**
   - Implementación de un grafo mediante listas de adyacencia.
   - Carga inicial desde un archivo para mapear conexiones entre lugares.
   - Determinación de rutas más eficientes.

4. **Gestión de Viajes:**
   - Registro en una lista simplemente enlazada.
   - Operaciones soportadas: crear y mostrar la estructura de datos.
   - Determinación del mejor camino para cada viaje basado en el grafo de rutas.

5. **Generación de Reportes:**
   - Reportes gráficos y tablas: top 5 de viajes más largos, más caros, clientes y vehículos más frecuentes.
   - Visualización de rutas específicas en viajes.

---

## Estructuras de Datos Utilizadas

1. **Lista Circular Doblemente Enlazada (Clientes):**
   - Implementada con nodos que almacenan DPI, nombres, apellidos, género, teléfono y dirección.
   - Se ordena automáticamente al insertar nodos según el DPI.

2. **Árbol B de Orden 5 (Vehículos):**
   - Cada nodo puede almacenar hasta 5 claves (placas) y punteros a nodos hijos.
   - Balanceado dinámicamente para mantener la estructura eficiente en búsquedas e inserciones.

3. **Lista de Adyacencia (Rutas):**
   - Cada lugar es representado como un nodo con una lista de conexiones (destinos).
   - Incluye tiempos de ruta como pesos en las aristas.

4. **Lista Simplemente Enlazada (Viajes):**
   - Almacena detalles del viaje como ID, cliente, vehículo y la ruta tomada.

---

## Estructura de Directorios

```plaintext
[LlegaRapidito]
├── data/                     # Archivos de entrada
│   ├── clientes.txt          # Datos de clientes para carga masiva
│   ├── vehiculos.txt         # Datos de vehículos para carga masiva
│   └── rutas.txt             # Datos de rutas para inicialización
├── src/                      # Código fuente
│   ├── models/               # Definición de estructuras de datos
│   │   ├── cliente.py        # Implementación de Lista Circular
│   │   ├── vehiculo.py       # Implementación de Árbol B
│   │   ├── ruta.py           # Implementación de Grafo
│   │   └── viaje.py          # Implementación de Lista Simple
│   ├── controllers/          # Lógica de negocio
│   │   ├── cliente_controller.py
│   │   ├── vehiculo_controller.py
│   │   ├── ruta_controller.py
│   │   └── viaje_controller.py
│   ├── utils/                # Funciones auxiliares
│   │   └── graphviz_utils.py # Generación de gráficos
│   └── app.py                # Archivo principal
├── reports/                  # Reportes generados
└── README.md                 # Manual de usuario
```

---

## Implementación y Explicación

### Gestión de Clientes
- **Estructura:** Lista Circular Doblemente Enlazada.
- **Operaciones:**
  - **Agregar Cliente:** Inserta un nuevo nodo y lo posiciona según el DPI.
  - **Modificar Cliente:** Busca el nodo por DPI y actualiza los datos.
  - **Eliminar Cliente:** Desconecta el nodo correspondiente al DPI.
  - **Mostrar Información:** Muestra los datos almacenados en el nodo solicitado.
  - **Visualizar Estructura:** Utiliza Graphviz para graficar la lista.

### Gestión de Vehículos
- **Estructura:** Árbol B de orden 5.
- **Operaciones:**
  - **Agregar Vehículo:** Inserta una placa y los datos correspondientes, balanceando el árbol si es necesario.
  - **Modificar/Eliminar:** Encuentra la placa y actualiza o elimina el nodo.
  - **Visualizar Estructura:** Genera un gráfico del árbol B.

### Gestión de Rutas
- **Estructura:** Grafo (Listas de Adyacencia).
- **Operaciones:**
  - **Cargar Archivo:** Procesa las rutas iniciales desde un archivo de texto.
  - **Determinar Rutas:** Encuentra caminos más eficientes utilizando algoritmos como Dijkstra.

### Gestión de Viajes
- **Estructura:** Lista Simplemente Enlazada.
- **Operaciones:**
  - **Crear Viaje:** Asocia cliente, vehículo y ruta al viaje, almacenando nodos con detalles del trayecto.
  - **Visualizar Rutas:** Representa la lista del recorrido gráficamente.

---

## Herramientas y Bibliotecas

1. **Python 3.11:** Lenguaje de programación.
2. **Tkinter o PyQt:** Para la interfaz gráfica.
3. **Graphviz:** Generación de reportes gráficos.
4. **Pandas:** Manejo y análisis de datos.

---

## Recomendaciones

- Mantener los archivos de datos organizados en el directorio `data/`.
- Validar la estructura de los archivos de entrada antes de la carga masiva.
- Verificar la instalación de Graphviz para asegurar la correcta generación de gráficos.

---

## Referencias

- Documentación oficial de [Python](https://docs.python.org/3/).
- Tutorial de [Graphviz](https://graphviz.org/documentation/).
