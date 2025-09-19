# 🚗 Sistema de Gestión de Lavadero - Aplicación de Escritorio

## 📌 Descripción
Este proyecto es un **sistema de gestión para un lavadero de vehículos**, desarrollado en **Python (Tkinter + MySQL)** como aplicación de escritorio.  
Se gestionan usuarios con dos roles principales:

- **Administrador** 🛠️  
  - Dashboard con métricas y reportes.  
  - Gestión de usuarios y roles.  
  - Definición de servicios y precios.  
  - Reportes financieros.  
  - Consulta de historial completo.  

- **Secretario** 🗂️  
  - Registro de vehículos y servicios prestados.  
  - Consulta de historial de servicios por cliente/vehículo.  
  - Cierre de caja diario.  

---

## ⚙️ Requisitos
- **Python 3.x**  
- **MySQL** (Workbench o XAMPP)  
- Librerías necesarias (se instalarán con `requirements.txt`):  
  - `mysql-connector-python`  
  - `tkinter`  
  - `pillow` (para imágenes, íconos)  

Instalar dependencias:
```bash
pip install -r requirements.txt
```

---

## 📂 Estructura del Proyecto

```
lavadero-escritorio/
│
├── README.md                 # Documentación del proyecto
├── .gitignore                # Ignorar archivos innecesarios
├── requirements.txt          # Dependencias de Python
│
├── database/
│   ├── db_config.py          # Configuración de conexión a MySQL
│   └── schema.sql            # Script de creación de tablas
│
├── src/
│   ├── main.py               # Punto de entrada de la app
│   │
│   ├── auth/
│   │   └── login.py          # Pantalla de Login
│   │
│   ├── admin/                # Funcionalidades de administrador
│   │   ├── dashboard.py      # Panel principal (gráficas, KPIs)
│   │   ├── users.py          # Gestión de usuarios y roles
│   │   ├── services.py       # Edición de servicios y precios
│   │   ├── reports.py        # Reportes y finanzas
│   │   └── history.py        # Historial completo
│   │
│   ├── secretary/            # Funcionalidades del secretario
│   │   ├── register.py       # Registro de vehículos/servicios
│   │   ├── history.py        # Consulta de historial
│   │   └── cash.py           # Cierre de caja
│   │
│   ├── ui/                   # Interfaz gráfica y recursos
│   │   ├── styles.py         # Estilos comunes
│   │   └── components.py     # Botones, menús, tablas reutilizables
│   │
│   └── utils/                # Utilidades compartidas
│       ├── validators.py     # Validaciones de datos
│       └── helpers.py        # Funciones generales
│
├── tests/                    # Pruebas unitarias
│   ├── test_auth.py
│   ├── test_admin.py
│   └── test_secretary.py
│
└── docs/                     # Documentación adicional
    └── manual_usuario.md      # Manual de usuario
```

---

## 🚀 Instalación y Uso
1. Clonar el repositorio:  
   ```bash
   git clone https://github.com/TU_USUARIO/lavadero-escritorio.git
   cd lavadero-escritorio
   ```
2. Crear base de datos en MySQL usando `database/schema.sql`.  
3. Configurar credenciales en `database/db_config.py`.  
4. Instalar dependencias:  
   ```bash
   pip install -r requirements.txt
   ```
5. Ejecutar el programa:  
   ```bash
   python src/main.py
   ```

---

## 📦 Empaquetado en .exe
Cuando el sistema esté listo, se podrá generar un ejecutable en Windows:  
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/main.py
```

---

## 🛠️ Roadmap
- [ ] Implementar conexión a MySQL.  
- [ ] Pantalla de Login.  
- [ ] Módulo de secretario (registro, historial, caja).  
- [ ] Módulo de administrador (dashboard, usuarios, servicios, reportes).  
- [ ] Reportes financieros con gráficos.  
- [ ] Empaquetado final en `.exe`.  

---

## 📄 Licencia
Uso académico y educativo.
