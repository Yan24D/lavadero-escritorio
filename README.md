# 🚗 Sistema de Gestión de Lavadero de Vehículos

## 📌 Descripción
Aplicación de escritorio desarrollada en **Python (Tkinter + MySQL)** para digitalizar la gestión de un lavadero de vehículos.  
Permite registrar servicios, gestionar caja, controlar usuarios (administrador y secretario) y generar reportes de ingresos y estadísticas.

La aplicación reemplaza el registro manual en planillas físicas por un sistema seguro y centralizado.

---

## 👥 Roles y Permisos

### 🔑 Administrador (Admin)
- Acceso total al sistema.
- Panel **Dashboard** con estadísticas (gráficas de servicios, ingresos, vehículos atendidos).
- Gestión de **usuarios y roles** (crear/eliminar secretarios).
- CRUD de **servicios y precios**.
- Acceso a **reportes financieros e historial de caja**.
- Visualización de **historial de lavados**.

### 📝 Secretario
- Acceso restringido (no puede gestionar usuarios ni reportes financieros).
- **Registrar vehículos y servicios** con los campos del formato físico:
  - Hora, Vehículo, Placa, Tipo de lavado, Costo, %, Lavador, Observaciones, Método de pago.
- **Consultar historial** de servicios registrados.
- **Generar cierre de caja diario** (ingresos del día).

---

## 📊 Módulos del Sistema

1. **🔐 Login**
   - Inicio de sesión por rol (admin / secretario).

2. **📋 Gestión de servicios (Admin)**
   - Crear, editar y eliminar tipos de lavados.
   - Definir precios de cada servicio.

3. **🛠️ Registro de lavados (Secretario)**
   - Interfaz que replica la planilla física.
   - Registro automático en la base de datos.
   - Asociación de lavador y cálculo de comisiones.

4. **📚 Historial de servicios**
   - Búsqueda por fecha, vehículo, placa, lavador.
   - Exportación a Excel/PDF (opcional).

5. **💰 Caja**
   - Registro automático de ingresos.
   - Cierre de caja diario con resumen de ingresos/egresos.

6. **📈 Dashboard (Admin)**
   - Gráficas y métricas:
     - Servicios más vendidos.
     - Ingresos diarios/mensuales.
     - Vehículos atendidos.
     - Comisiones de lavadores.

---

## 🗂️ Estructura de Base de Datos (MySQL)

- **usuarios**
  - id, usuario, password, rol

- **servicios**
  - id, nombre, precio, descripción

- **Registros**
  - id, fecha, hora, vehiculo, placa, tipo_lavado, costo, porcentaje, lavador, observaciones, pago, usuario_id

- **caja**
  - id, fecha, ingresos, egresos, balance, responsable

---

## ⚙️ Requisitos

- Python 3.10+
- MySQL Server
- Conector de Python para MySQL (`mysql-connector-python` o `pymysql`)
- Librerías recomendadas:
  - `tkinter`
  - `pandas`
  - `matplotlib`

---

## 🚀 Instalación

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repo>
   cd lavadero-electron
   ```

2. Crear y activar entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate   # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar la base de datos MySQL:
   - Crear base de datos `cleancar`
   - Importar el archivo `schema.sql` (incluido en el proyecto).

5. Ejecutar la aplicación:
   ```bash
   python main.py
   ```

---

## 📦 Futuras Mejoras

- Exportación avanzada a Excel/PDF.
- Reportes de comisiones individuales por lavador.
- Módulo de egresos (gastos del lavadero).
- Integración con facturación electrónica.

---

## 👨‍💻 Autores
- Proyecto académico desarrollado por el equipo de software victorius.
