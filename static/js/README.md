# 🐆 Jaguar Corp
### Sistema de Facturación de Clientes

## 1. Descripción

Jaguar Corp es un proyecto académico desarrollado para administrar facturas de clientes mediante una aplicación web.

El sistema permite registrar facturas, consultar información, aplicar descuentos, registrar pagos y eliminar facturas.

También cuenta con un panel principal que muestra las estadísticas generales.

## 2. Tecnologías utilizadas

| Tecnología | ¿Para qué la utilizamos? |
|---|---|
| Python | Para programar las operaciones y validaciones de las facturas. |
| Flask | Para conectar Python con nuestra aplicación web. |
| HTML5 | Para crear la estructura de las páginas. |
| CSS3 | Para personalizar el diseño. |
| JavaScript | Para controlar botones, formularios e interacciones. |
| Bootstrap 5 | Para crear una interfaz adaptable y organizada. |
| Bootstrap Icons | Para agregar iconos a los botones y menús. |
| SweetAlert2 | Para mostrar mensajes y confirmaciones. |
| Jinja2 | Para mostrar información de Python dentro del HTML. |

## 3. Estructura del proyecto

```text
Jaguar-Corp/
│
├── app.py
├── main.py
├── factura_cliente.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── nueva_factura.html
│   ├── facturas.html
│   └── detalle_factura.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js
│       ├── facturas.js
│       └── detalle_factura.js
│
└── README.md
```

### Archivos principales

- **app.py:** administra las rutas y las operaciones de la aplicación.
- **factura_cliente.py:** contiene la clase, los atributos y los métodos de facturación.
- **main.py:** permite comprobar el funcionamiento de los métodos desde la terminal.
- **base.html:** contiene la estructura principal de las páginas.
- **style.css:** contiene los estilos personalizados.

## 4. Funciones JavaScript utilizadas

JavaScript permite que nuestra aplicación sea interactiva.

| Función | ¿Para qué sirve? |
|---|---|
| `addEventListener()` | Detecta acciones del usuario. |
| `DOMContentLoaded` | Espera a que cargue el HTML. |
| `getElementById()` | Busca un elemento por su identificador. |
| `querySelectorAll()` | Busca varios elementos de la página. |
| `forEach()` | Recorre elementos. |
| `preventDefault()` | Detiene temporalmente el envío de un formulario. |
| `reportValidity()` | Comprueba las validaciones HTML. |
| `submit()` | Envía un formulario. |
| `Swal.fire()` | Muestra ventanas de confirmación. |
| `.then()` | Procesa el resultado de una confirmación. |
| `window.print()` | Abre la opción de imprimir. |

### Archivos JavaScript

- **app.js:** controla las funciones generales de la aplicación.
- **facturas.js:** confirma la eliminación de facturas.
- **detalle_factura.js:** confirma pagos, descuentos y eliminaciones.

## 5. Clase Factura_Cliente

La clase contiene cinco atributos:

1. `cliente`: nombre del cliente.
2. `numero_factura`: número de identificación.
3. `monto`: valor de la factura.
4. `fecha`: fecha de emisión.
5. `estado_pago`: Pendiente o Pagado.

Los dos primeros son obligatorios y los otros tres tienen valores predeterminados.

### Métodos principales

| Método | Función |
|---|---|
| `__init__()` | Inicializa una factura. |
| `get_*()` | Permite consultar los atributos. |
| `set_*()` | Permite modificar y validar los atributos. |
| `aplicar_descuento()` | Aplica descuentos entre 0 % y 100 %. |
| `marcar_pagado()` | Registra el pago cuando el monto es mayor que cero. |
| `mostrar_factura()` | Genera un resumen de la factura. |

## 6. Funciones de Flask

| Función | ¿Para qué sirve? |
|---|---|
| `Flask()` | Crea la aplicación web. |
| `@app.route()` | Define las rutas. |
| `render_template()` | Muestra las páginas HTML. |
| `request` | Recibe información del usuario. |
| `redirect()` | Redirige a otra página. |
| `url_for()` | Genera direcciones de la aplicación. |
| `flash()` | Guarda mensajes temporales. |
| `abort()` | Genera errores HTTP, como el 404. |

## 7. Funcionamiento del sistema

El usuario puede:

- Registrar una factura.
- Consultar y buscar facturas.
- Filtrar por estado de pago.
- Aplicar descuentos.
- Marcar facturas como pagadas.
- Revisar el historial de operaciones.
- Imprimir o eliminar una factura.

**Importante:** Los datos se almacenan temporalmente en diccionarios de Python. Al reiniciar el servidor, las facturas registradas se pierden.

## 8. Instalación y ejecución

### 1. Crear el entorno virtual

```bash
python3 -m venv .venv
```

### 2. Activarlo en macOS

```bash
source .venv/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python app.py
```

Abrir en el navegador:

http://127.0.0.1:5000

### 5. Ejecutar las pruebas de consola

```bash
python main.py
```

---

**Jaguar Corp © 2026**  
*Proyecto académico desarrollado con Python y Flask.*