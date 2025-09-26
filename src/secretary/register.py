"""
Módulo de Registro de Servicios para Secretario - Actualizado para nueva BD
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, date, time
from database.db_config import db

class SecretaryRegisterPanel:
    """Panel principal de registro de servicios para secretario"""
    
    def __init__(self, parent, user_data, on_logout_callback):
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout_callback
        self.vehicle_types = []
        self.lavadores_data = []
        self.current_services = []
        self.selected_service = None
        
        self.setup_ui()
        self.load_initial_data()
    
    def setup_ui(self):
        """Configurar interfaz principal"""
        # Limpiar ventana
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.parent.configure(bg='#f8fafc')
        self.parent.geometry("1400x900")
        self.parent.title("Clean Car - Panel Secretario")
        
        # Header (estático)
        self.create_header()
        
        # Contenido principal con scroll
        main_canvas = tk.Canvas(self.parent, bg='#f8fafc')
        main_scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=main_canvas.yview)
        main_container = tk.Frame(main_canvas, bg='#f8fafc')
        
        # Configurar scroll
        main_container.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=main_container, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        main_canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        main_scrollbar.pack(side="right", fill="y", pady=10)
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        main_canvas.bind("<MouseWheel>", _on_mousewheel)  # Windows
        main_canvas.bind("<Button-4>", lambda e: main_canvas.yview_scroll(-1, "units"))  # Linux
        main_canvas.bind("<Button-5>", lambda e: main_canvas.yview_scroll(1, "units"))   # Linux
        
        # Navegación por pestañas
        self.create_navigation(main_container)
        
        # Contenido de la pestaña actual
        self.content_frame = tk.Frame(main_container, bg='#f8fafc')
        self.content_frame.pack(fill='both', expand=True, pady=(20, 0))
        
        # Mostrar pestaña por defecto (Registrar Vehículo)
        self.show_register_tab()
    
    def create_header(self):
        """Crear header de la aplicación"""
        header_frame = tk.Frame(self.parent, bg='#2563eb', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Contenido del header
        header_content = tk.Frame(header_frame, bg='#2563eb')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Título y fecha (lado izquierdo)
        left_frame = tk.Frame(header_content, bg='#2563eb')
        left_frame.pack(side='left', fill='y')
        
        title_label = tk.Label(
            left_frame,
            text="Clean Car - Panel Secretario",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#2563eb'
        )
        title_label.pack(side='left')
        
        # Información del usuario (lado derecho)
        right_frame = tk.Frame(header_content, bg='#2563eb')
        right_frame.pack(side='right', fill='y')
        
        # Botón cerrar sesión
        logout_btn = tk.Button(
            right_frame,
            text="Cerrar Sesión",
            font=('Segoe UI', 9),
            bg='#dc2626',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.on_logout
        )
        logout_btn.pack(side='right')

        # Usuario
        user_label = tk.Label(
            right_frame,
            text=f"👤 {self.user_data['nombre']}",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#2563eb'
        )
        user_label.pack(side='right', padx=(0, 20))

        # Fecha actual
        today = datetime.now()
        date_label = tk.Label(
            right_frame,
            text=f"📅 {today.strftime('%A, %d de %B de %Y')}",
            font=('Segoe UI', 10),
            fg='white',
            bg='#2563eb'
        )
        date_label.pack(side='right', padx=(0, 20))
        
    def create_navigation(self, parent):
        """Crear navegación por pestañas incluyendo Cierre de Caja"""
        nav_frame = tk.Frame(parent, bg='#f8fafc')
        nav_frame.pack(fill='x', pady=(0, 10))
        
        # Estilo de botones de navegación
        btn_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 12
        }
        
        # Pestaña Registrar Vehículo
        self.btn_register = tk.Button(
            nav_frame,
            text="➕ Registrar Vehículo",
            bg='#2563eb',
            fg='white',
            command=self.show_register_tab,
            **btn_style
        )
        self.btn_register.pack(side='left', padx=(0, 2))
        
        # Pestaña Consultar Historial
        self.btn_history = tk.Button(
            nav_frame,
            text="🔍 Consultar Historial",
            bg='#64748b',
            fg='white',
            command=self.show_history_tab,
            **btn_style
        )
        self.btn_history.pack(side='left', padx=2)
        
        # Pestaña Cierre de Caja
        self.btn_cash = tk.Button(
            nav_frame,
            text="💰 Cierre de Caja",
            bg='#64748b',
            fg='white',
            command=self.show_cash_tab,
            **btn_style
        )
        self.btn_cash.pack(side='left', padx=2)   

    def show_register_tab(self):
        """Mostrar pestaña de registro"""
        self.update_nav_buttons('register')
        self.clear_content()
        
        # Título de la sección
        title_frame = tk.Frame(self.content_frame, bg='#f8fafc')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="Nuevo Registro de Servicio",
            font=('Segoe UI', 20, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(side='left')
        
        # Contenedor principal
        main_container = tk.Frame(self.content_frame, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        # Formulario de registro (pantalla completa)
        self.create_form_section(main_container)

        # Recargar los combobox
        self.load_vehicle_types()
        self.load_lavadores()

    def create_form_section(self, parent):
        """Crear formulario de registro"""
        form_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        form_frame.pack(fill='both', expand=True, padx=50)
        
        # Padding interno
        form_content = tk.Frame(form_frame, bg='white')
        form_content.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Título del formulario
        form_title = tk.Label(
            form_content,
            text="Detalles del Servicio",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='white'
        )
        form_title.pack(anchor='w', pady=(0, 20))
        
        # Primera fila - Fecha y Hora
        row1 = tk.Frame(form_content, bg='white')
        row1.pack(fill='x', pady=(0, 15))
        
        # Fecha
        date_frame = tk.Frame(row1, bg='white')
        date_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            date_frame,
            text="Fecha:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.date_entry = tk.Entry(
            date_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.date_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Hora
        time_frame = tk.Frame(row1, bg='white')
        time_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(
            time_frame,
            text="Hora:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.time_entry = tk.Entry(
            time_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.time_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))
        
        # Segunda fila - Tipo de Vehículo y Placa
        row2 = tk.Frame(form_content, bg='white')
        row2.pack(fill='x', pady=(0, 15))
        
        # Tipo de Vehículo
        vehicle_frame = tk.Frame(row2, bg='white')
        vehicle_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            vehicle_frame,
            text="Tipo de Vehículo:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.vehicle_var = tk.StringVar()
        self.vehicle_combo = ttk.Combobox(
            vehicle_frame,
            textvariable=self.vehicle_var,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.vehicle_combo.pack(fill='x', pady=(5, 0), ipady=8)
        self.vehicle_combo.bind('<<ComboboxSelected>>', self.on_vehicle_selected)
        
        # Placa
        plate_frame = tk.Frame(row2, bg='white')
        plate_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(
            plate_frame,
            text="Placa:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.plate_entry = tk.Entry(
            plate_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.plate_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Tercera fila - Servicio
        row3 = tk.Frame(form_content, bg='white')
        row3.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            row3,
            text="Servicio:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.service_var = tk.StringVar()
        self.service_combo = ttk.Combobox(
            row3,
            textvariable=self.service_var,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.service_combo.pack(fill='x', pady=(5, 0), ipady=8)
        self.service_combo.bind('<<ComboboxSelected>>', self.on_service_selected)
        
        # Cuarta fila - Costo y Porcentaje
        row4 = tk.Frame(form_content, bg='white')
        row4.pack(fill='x', pady=(0, 15))
        
        # Costo
        cost_frame = tk.Frame(row4, bg='white')
        cost_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            cost_frame,
            text="Costo ($):",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.cost_entry = tk.Entry(
            cost_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.cost_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Porcentaje
        percent_frame = tk.Frame(row4, bg='white')
        percent_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        tk.Label(
            percent_frame,
            text="Porcentaje (%):",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.percent_entry = tk.Entry(
            percent_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.percent_entry.pack(fill='x', pady=(5, 0), ipady=8)
        self.percent_entry.insert(0, "50.00")
        
        # Quinta fila - Lavador
        row5 = tk.Frame(form_content, bg='white')
        row5.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            row5,
            text="Lavador:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.lavador_var = tk.StringVar()
        self.lavador_combo = ttk.Combobox(
            row5,
            textvariable=self.lavador_var,
            font=('Segoe UI', 10),
            state='readonly'
        )
        self.lavador_combo.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Sexta fila - Estado de Pago
        row6 = tk.Frame(form_content, bg='white')
        row6.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            row6,
            text="Estado del Pago:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.payment_status_var = tk.BooleanVar(value=False)
        
        payment_checkbox = tk.Checkbutton(
            row6,
            text="Pagado",
            variable=self.payment_status_var,
            font=('Segoe UI', 10),
            bg='white',
            fg='#374151'
        )
        payment_checkbox.pack(anchor='w', pady=(5, 0))
        
        # Séptima fila - Observaciones
        row7 = tk.Frame(form_content, bg='white')
        row7.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            row7,
            text="Observaciones:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.observations_text = tk.Text(
            row7,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb',
            height=3
        )
        self.observations_text.pack(fill='x', pady=(5, 0))
        
        # Botones
        buttons_frame = tk.Frame(form_content, bg='white')
        buttons_frame.pack(fill='x', pady=(10, 0))
        
        # Botón Limpiar
        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ Limpiar",
            font=('Segoe UI', 11, 'bold'),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.clear_form
        )
        clear_btn.pack(side='left', padx=(0, 10))
        
        # Botón Registrar
        register_btn = tk.Button(
            buttons_frame,
            text="✅ Registrar Servicio",
            font=('Segoe UI', 11, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.register_service
        )
        register_btn.pack(side='right')
    
    def load_initial_data(self):
        """Cargar datos iniciales"""
        self.load_vehicle_types()
        self.load_lavadores()
    
    def load_vehicle_types(self):
        """Cargar tipos de vehículos"""
        try:
            self.vehicle_types = [
                {'value': 'motorcycle', 'display': 'Motocicleta'},
                {'value': 'car', 'display': 'Automóvil'},
                {'value': 'pickup', 'display': 'Camioneta'},
                {'value': 'suv', 'display': 'SUV'},
                {'value': 'truck', 'display': 'Camión'}
            ]
            
            if hasattr(self, 'vehicle_combo'):
                vehicle_names = [item['display'] for item in self.vehicle_types]
                self.vehicle_combo['values'] = vehicle_names
                
        except Exception as e:
            print(f"Error cargando tipos de vehículos: {e}")
    
    def load_lavadores(self):
        """Cargar lista de lavadores"""
        try:
            query = "SELECT id, CONCAT(nombre, ' ', apellido) as nombre_completo FROM lavadores WHERE activo = 1 ORDER BY nombre"
            self.lavadores_data = db.execute_query(query)
            
            if self.lavadores_data and hasattr(self, 'lavador_combo'):
                lavador_names = [lavador['nombre_completo'] for lavador in self.lavadores_data]
                self.lavador_combo['values'] = lavador_names
                
        except Exception as e:
            print(f"Error cargando lavadores: {e}")
    
    def on_vehicle_selected(self, event=None):
        """Cuando se selecciona un tipo de vehículo"""
        try:
            selected_display = self.vehicle_var.get()
            if not selected_display:
                return
            
            # Encontrar el valor interno del vehículo
            selected_vehicle = None
            for item in self.vehicle_types:
                if item['display'] == selected_display:
                    selected_vehicle = item['value']
                    break
            
            if selected_vehicle:
                # Cargar servicios disponibles para este tipo de vehículo
                self.load_services_for_vehicle(selected_vehicle)
                
        except Exception as e:
            print(f"Error al seleccionar vehículo: {e}")
    
    def load_services_for_vehicle(self, vehicle_type):
        try:
            query = """
                SELECT s.id, s.nombre, s.descripcion, sp.precio,
                    CONCAT('$', FORMAT(sp.precio, 0)) as precio_formato
                FROM servicios s
                INNER JOIN servicio_precios sp ON s.id = sp.id_servicio
                WHERE sp.tipo_vehiculo = %s AND sp.activo = 1
                ORDER BY sp.precio ASC
            """
            
            results = db.execute_query(query, (vehicle_type,))
            self.current_services = results or []
            
            if results and hasattr(self, 'service_combo'):
                service_names = [f"{s['nombre']} - {s['precio_formato']}" for s in results]
                self.service_combo['values'] = service_names
                self.service_combo.set("")
                
        except Exception as e:
            print(f"Error cargando servicios para vehículo: {e}")
    
    def on_service_selected(self, event=None):
        """Cuando se selecciona un servicio"""
        try:
            selected_service_text = self.service_var.get()
            if not selected_service_text:
                return
            
            # Encontrar el servicio seleccionado
            selected_service = None
            for service in self.current_services:
                service_text = f"{service['nombre']} - {service['precio_formato']}"
                if service_text == selected_service_text:
                    selected_service = service
                    break
            
            if selected_service:
                self.selected_service = selected_service
                # Actualizar el campo de costo automáticamente
                self.cost_entry.delete(0, tk.END)
                self.cost_entry.insert(0, f"{selected_service['precio']:,.0f}")
                
        except Exception as e:
            print(f"Error al seleccionar servicio: {e}")
    
    def clear_form(self):
        """Limpiar formulario"""
        # Mantener fecha y hora actuales
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))
        
        # Limpiar otros campos
        self.vehicle_var.set("")
        self.plate_entry.delete(0, tk.END)
        self.service_var.set("")
        self.cost_entry.delete(0, tk.END)
        self.percent_entry.delete(0, tk.END)
        self.percent_entry.insert(0, "50.00")
        self.lavador_var.set("")
        self.payment_status_var.set(False)
        self.observations_text.delete(1.0, tk.END)
        
        # Limpiar servicios actuales
        if hasattr(self, 'service_combo'):
            self.service_combo['values'] = []
        
        self.selected_service = None
    
    def register_service(self):
        """Registrar nuevo servicio"""
        # Validar campos requeridos
        if not self.vehicle_var.get():
            messagebox.showerror("Error", "Debe seleccionar un tipo de vehículo")
            return
            
        if not self.plate_entry.get().strip():
            messagebox.showerror("Error", "El campo Placa es obligatorio")
            return
        
        if not self.selected_service:
            messagebox.showerror("Error", "Debe seleccionar un servicio")
            return
        
        if not self.cost_entry.get().strip():
            messagebox.showerror("Error", "El campo Costo es obligatorio")
            return
            
        if not self.lavador_var.get():
            messagebox.showerror("Error", "Debe seleccionar un lavador")
            return
        
        try:
            # Obtener el valor interno del vehículo seleccionado
            selected_display = self.vehicle_var.get()
            vehicle_value = None
            for item in self.vehicle_types:
                if item['display'] == selected_display:
                    vehicle_value = item['value']
                    break
            
            # Obtener el ID del lavador seleccionado
            selected_lavador_name = self.lavador_var.get()
            lavador_id = None
            for lavador in self.lavadores_data:
                if lavador['nombre_completo'] == selected_lavador_name:
                    lavador_id = lavador['id']
                    break
            
            # Preparar datos
            registro_data = {
                'fecha': self.date_entry.get(),
                'hora': self.time_entry.get(),
                'vehiculo': vehicle_value,
                'placa': self.plate_entry.get().strip().upper(),
                'id_servicio': self.selected_service['id'],  # Cambio: id_servicio
                'costo': float(self.cost_entry.get().replace(',', '')),
                'porcentaje': float(self.percent_entry.get()) if self.percent_entry.get() else 50.0,
                'lavador': selected_lavador_name,
                'observaciones': self.observations_text.get(1.0, tk.END).strip() or None,
                'pago': 'Pagado' if self.payment_status_var.get() else 'Pendiente',
                'id_usuario': self.user_data['id']  # Cambio: id_usuario
            }
            
            # Insertar en base de datos
            query = """
                INSERT INTO registros 
                (fecha, hora, vehiculo, placa, id_servicio, costo, porcentaje, 
                 lavador, observaciones, pago, id_usuario)
                VALUES (%(fecha)s, %(hora)s, %(vehiculo)s, %(placa)s, %(id_servicio)s,
                        %(costo)s, %(porcentaje)s, %(lavador)s, %(observaciones)s, 
                        %(pago)s, %(id_usuario)s)
            """
            
            registro_id = db.execute_insert(query, registro_data)
            
            if registro_id:
                messagebox.showinfo("Éxito", "Servicio registrado correctamente")
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo registrar el servicio")
                
        except ValueError as e:
            messagebox.showerror("Error", "Error en los datos numéricos. Verifique costo y porcentaje.")
        except Exception as e:
            print(f"Error registrando servicio: {e}")
            messagebox.showerror("Error", f"Error al registrar servicio: {str(e)}")
    
    def show_history_tab(self):
        """Mostrar pestaña de historial"""
        self.update_nav_buttons('history')
        self.clear_content()
        
        # Título
        title_label = tk.Label(
            self.content_frame,
            text="Consultar Historial de Servicios",
            font=('Segoe UI', 20, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Filtros
        filters_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        filters_frame.pack(fill='x', pady=(0, 20))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=15)
        
        # Título de filtros
        filters_title = tk.Label(
            filters_content,
            text="🔍 Filtros de Búsqueda",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='white'
        )
        filters_title.pack(anchor='w', pady=(0, 15))
        
        # Fila de filtros
        filters_row = tk.Frame(filters_content, bg='white')
        filters_row.pack(fill='x')
        
        # Filtro por fecha
        date_filter_frame = tk.Frame(filters_row, bg='white')
        date_filter_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            date_filter_frame,
            text="Fecha:",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        self.filter_date = tk.Entry(
            date_filter_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        self.filter_date.pack(fill='x', pady=(5, 0), ipady=8)
        self.filter_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Filtro por placa
        plate_filter_frame = tk.Frame(filters_row, bg='white')
        plate_filter_frame.pack(side='left', fill='x', expand=True, padx=10)
        
        tk.Label(
            plate_filter_frame,
            text="Placa:",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        self.filter_plate = tk.Entry(
            plate_filter_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        self.filter_plate.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Filtro por lavador
        washer_filter_frame = tk.Frame(filters_row, bg='white')
        washer_filter_frame.pack(side='left', fill='x', expand=True, padx=10)
        
        tk.Label(
            washer_filter_frame,
            text="Lavador:",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        ).pack(anchor='w')
        
        self.filter_washer = tk.Entry(
            washer_filter_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1
        )
        self.filter_washer.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Botón buscar
        search_btn_frame = tk.Frame(filters_row, bg='white')
        search_btn_frame.pack(side='right', padx=(10, 0))
        
        tk.Label(search_btn_frame, text="", bg='white').pack()  # Spacer
        
        search_btn = tk.Button(
            search_btn_frame,
            text="🔍 Buscar",
            font=('Segoe UI', 10, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.search_history
        )
        search_btn.pack(pady=(5, 0))
        
        # Tabla de resultados
        self.create_history_table()
        
        # Cargar datos iniciales
        self.search_history()
    
    def create_history_table(self):
        """Crear tabla de historial"""
        table_frame = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Título de la tabla
        table_title_frame = tk.Frame(table_frame, bg='#f8fafc', height=50)
        table_title_frame.pack(fill='x')
        table_title_frame.pack_propagate(False)
        
        table_title = tk.Label(
            table_title_frame,
            text="📋 Resultados de la Búsqueda",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        table_title.pack(side='left', padx=20, pady=15)
        
        # Crear Treeview
        columns = ('ID', 'Fecha', 'Hora', 'Vehículo', 'Placa', 'Servicio', 'Costo', 'Lavador', 'Estado')
        
        self.history_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.history_tree.heading('ID', text='ID')
        self.history_tree.heading('Fecha', text='Fecha')
        self.history_tree.heading('Hora', text='Hora')
        self.history_tree.heading('Vehículo', text='Vehículo')
        self.history_tree.heading('Placa', text='Placa')
        self.history_tree.heading('Servicio', text='Servicio')
        self.history_tree.heading('Costo', text='Costo')
        self.history_tree.heading('Lavador', text='Lavador')
        self.history_tree.heading('Estado', text='Estado')
        
        # Configurar ancho de columnas
        self.history_tree.column('ID', width=50, anchor='center')
        self.history_tree.column('Fecha', width=100, anchor='center')
        self.history_tree.column('Hora', width=80, anchor='center')
        self.history_tree.column('Vehículo', width=100, anchor='center')
        self.history_tree.column('Placa', width=100, anchor='center')
        self.history_tree.column('Servicio', width=150)
        self.history_tree.column('Costo', width=100, anchor='center')
        self.history_tree.column('Lavador', width=120)
        self.history_tree.column('Estado', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.history_tree.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        scrollbar.pack(side='right', fill='y', pady=20, padx=(0, 20))
    
    def search_history(self):
        """Buscar en el historial usando la vista optimizada"""
        try:
            # Limpiar tabla
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Usar la vista vista_registros_completos
            base_query = """
                SELECT id, fecha, hora, vehiculo_nombre, placa, servicio_nombre,
                       costo, lavador, pago
                FROM vista_registros_completos
                WHERE 1=1
            """
            
            params = []
            
            # Filtro por fecha
            if self.filter_date.get().strip():
                base_query += " AND fecha = %s"
                params.append(self.filter_date.get().strip())
            
            # Filtro por placa
            if self.filter_plate.get().strip():
                base_query += " AND placa LIKE %s"
                params.append(f"%{self.filter_plate.get().strip()}%")
            
            # Filtro por lavador
            if self.filter_washer.get().strip():
                base_query += " AND lavador LIKE %s"
                params.append(f"%{self.filter_washer.get().strip()}%")
            
            base_query += " ORDER BY fecha DESC, hora DESC LIMIT 100"
            
            # Ejecutar consulta
            results = db.execute_query(base_query, params if params else None)
            
            if results:
                for row in results:
                    # Formatear datos
                    fecha = row['fecha'].strftime('%Y-%m-%d') if row['fecha'] else ''
                    hora = str(row['hora']) if row['hora'] else ''
                    costo = f"${row['costo']:,.0f}" if row['costo'] else '$0'
                    placa = row['placa'] or 'N/A'
                    lavador = row['lavador'] or 'N/A'
                    
                    self.history_tree.insert('', 'end', values=(
                        row['id'],
                        fecha,
                        hora,
                        row['vehiculo_nombre'],
                        placa,
                        row['servicio_nombre'],
                        costo,
                        lavador,
                        row['pago']
                    ))
            else:
                # Mostrar mensaje de no hay resultados
                self.history_tree.insert('', 'end', values=(
                    '', '', '', 'No se encontraron resultados', '', '', '', '', ''
                ))
                
        except Exception as e:
            print(f"Error buscando historial: {e}")
            messagebox.showerror("Error", "Error al buscar en el historial")
    
    def update_nav_buttons(self, active_tab):
        """Actualizar estilo de botones de navegación"""
        # Reset all buttons
        self.btn_register.config(bg='#64748b')
        self.btn_history.config(bg='#64748b')
        self.btn_cash.config(bg='#64748b')
        
        # Activate selected button
        if active_tab == 'register':
            self.btn_register.config(bg='#2563eb')
        elif active_tab == 'history':
            self.btn_history.config(bg='#2563eb')
        elif active_tab == 'cash':
            self.btn_cash.config(bg='#2563eb')

    def show_cash_tab(self):
        pass

    def create_summary_cards(self):
        pass

    def create_daily_records_table(self):
        pass

    def create_analytics_section(self):
        pass

    def load_cash_data(self):
        pass

    def load_daily_records(self):
        pass

    def load_lavador_stats(self):
        pass

    def load_servicios_stats(self):
        pass

    def show_context_menu(self):
        pass

    def edit_record(self):
        pass

    def create_edit_window(self):
        pass

    def delete_record(self):
        pass

    def export_csv(self):
        pass

    def print_report(self):
        pass

    def clear_content(self):
        """Limpiar contenido actual"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_cash_tab(self):
        """Mostrar pestaña de cierre de caja diario"""
        self.update_nav_buttons('cash')
        self.clear_content()
        
        # Título
        title_label = tk.Label(
            self.content_frame,
            text="Cierre de Caja Diario",
            font=('Segoe UI', 20, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(anchor='w', pady=(0, 20))
        
        # Botones de acción superiores
        actions_frame = tk.Frame(self.content_frame, bg='#f8fafc')
        actions_frame.pack(fill='x', pady=(0, 20))
        
        # Botón Exportar CSV
        export_csv_btn = tk.Button(
            actions_frame,
            text="📄 Exportar CSV",
            font=('Segoe UI', 10, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.export_csv
        )
        export_csv_btn.pack(side='left', padx=(0, 10))
        
        # Botón Imprimir Reporte
        print_report_btn = tk.Button(
            actions_frame,
            text="🖨️ Imprimir Reporte",
            font=('Segoe UI', 10, 'bold'),
            bg='#dc2626',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.print_report
        )
        print_report_btn.pack(side='left', padx=(0, 10))
        
        # Botón Actualizar
        refresh_btn = tk.Button(
            actions_frame,
            text="🔄 Actualizar",
            font=('Segoe UI', 10, 'bold'),
            bg='#0891b2',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.load_cash_data
        )
        refresh_btn.pack(side='right')
        
        # Cards de resumen (4 cards horizontales)
        self.create_summary_cards()
        
        # Tabla de registros del día
        self.create_daily_records_table()
        
        # Sección inferior con estadísticas
        self.create_analytics_section()
        
        # Cargar datos iniciales
        self.load_cash_data()

    def create_summary_cards(self):
        """Crear cards de resumen financiero"""
        cards_frame = tk.Frame(self.content_frame, bg='#f8fafc')
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Card 1 - Ingresos del Día
        ingresos_card = tk.Frame(cards_frame, bg='#3b82f6', relief='solid', borderwidth=1)
        ingresos_card.pack(side='left', fill='x', expand=True, padx=(0, 5))
        
        ingresos_content = tk.Frame(ingresos_card, bg='#3b82f6')
        ingresos_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        tk.Label(
            ingresos_content,
            text="INGRESOS DEL DIA",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#3b82f6'
        ).pack()
        
        self.ingresos_label = tk.Label(
            ingresos_content,
            text="$0",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#3b82f6'
        )
        self.ingresos_label.pack(pady=(5, 0))
        
        # Card 2 - Total Comisiones
        comisiones_card = tk.Frame(cards_frame, bg='#6b7280', relief='solid', borderwidth=1)
        comisiones_card.pack(side='left', fill='x', expand=True, padx=5)
        
        comisiones_content = tk.Frame(comisiones_card, bg='#6b7280')
        comisiones_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        tk.Label(
            comisiones_content,
            text="TOTAL COMISIONES",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#6b7280'
        ).pack()
        
        self.comisiones_label = tk.Label(
            comisiones_content,
            text="$0",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#6b7280'
        )
        self.comisiones_label.pack(pady=(5, 0))
        
        # Card 3 - Balance Neto
        balance_card = tk.Frame(cards_frame, bg='#059669', relief='solid', borderwidth=1)
        balance_card.pack(side='left', fill='x', expand=True, padx=5)
        
        balance_content = tk.Frame(balance_card, bg='#059669')
        balance_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        tk.Label(
            balance_content,
            text="BALANCE NETO",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#059669'
        ).pack()
        
        self.balance_label = tk.Label(
            balance_content,
            text="$0",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#059669'
        )
        self.balance_label.pack(pady=(5, 0))
        
        # Card 4 - Servicios Realizados
        servicios_card = tk.Frame(cards_frame, bg='#2563eb', relief='solid', borderwidth=1)
        servicios_card.pack(side='left', fill='x', expand=True, padx=(5, 0))
        
        servicios_content = tk.Frame(servicios_card, bg='#2563eb')
        servicios_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        tk.Label(
            servicios_content,
            text="SERVICIOS REALIZADOS",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#2563eb'
        ).pack()
        
        self.servicios_label = tk.Label(
            servicios_content,
            text="0",
            font=('Segoe UI', 18, 'bold'),
            fg='white',
            bg='#2563eb'
        )
        self.servicios_label.pack(pady=(5, 0))

    def create_daily_records_table(self):
        """Crear tabla de registros del día"""
        table_container = tk.Frame(self.content_frame, bg='white', relief='solid', borderwidth=1)
        table_container.pack(fill='both', expand=True, pady=(0, 20))
        
        # Encabezado de la tabla
        table_header = tk.Frame(table_container, bg='#f8fafc')
        table_header.pack(fill='x', padx=1, pady=1)
        
        # Fecha selector y título
        header_content = tk.Frame(table_header, bg='#f8fafc')
        header_content.pack(fill='x', padx=15, pady=10)
        
        # Título con fecha
        today_str = datetime.now().strftime('%A, %d de %B de %Y')
        table_title = tk.Label(
            header_content,
            text=f"📋 Registros del Día - {today_str}",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        table_title.pack(side='left')
        
        # Crear Treeview para registros
        columns = ('ID', 'Hora', 'Vehículo', 'Placa', 'Servicio', 'Costo', 'Comisión', 'Lavador', 'Estado')
        
        self.records_tree = ttk.Treeview(table_container, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.records_tree.heading('ID', text='ID')
        self.records_tree.heading('Hora', text='🕐 Hora')
        self.records_tree.heading('Vehículo', text='🚗 Vehículo') 
        self.records_tree.heading('Placa', text='🔢 Placa')
        self.records_tree.heading('Servicio', text='⚙️ Servicio')
        self.records_tree.heading('Costo', text='💲 Costo')
        self.records_tree.heading('Comisión', text='📊 Comisión')
        self.records_tree.heading('Lavador', text='👤 Lavador')
        self.records_tree.heading('Estado', text='📝 Estado')
        
        # Configurar ancho de columnas
        self.records_tree.column('ID', width=50, anchor='center')
        self.records_tree.column('Hora', width=80, anchor='center')
        self.records_tree.column('Vehículo', width=100, anchor='center')
        self.records_tree.column('Placa', width=100, anchor='center')
        self.records_tree.column('Servicio', width=120)
        self.records_tree.column('Costo', width=100, anchor='center')
        self.records_tree.column('Comisión', width=100, anchor='center')
        self.records_tree.column('Lavador', width=120)
        self.records_tree.column('Estado', width=100, anchor='center')
        
        # Menú contextual para acciones
        self.context_menu = tk.Menu(self.records_tree, tearoff=0)
        self.context_menu.add_command(label="✏️ Editar", command=self.edit_record)
        self.context_menu.add_command(label="🗑️ Eliminar", command=self.delete_record)
        
        # Bind del menú contextual
        self.records_tree.bind("<Button-3>", self.show_context_menu)  # Clic derecho
        
        # Scrollbar para la tabla
        table_scrollbar = ttk.Scrollbar(table_container, orient='vertical', command=self.records_tree.yview)
        self.records_tree.configure(yscrollcommand=table_scrollbar.set)
        
        # Pack tabla y scrollbar
        self.records_tree.pack(side='left', fill='both', expand=True, padx=(15, 0), pady=(0, 15))
        table_scrollbar.pack(side='right', fill='y', pady=(0, 15), padx=(0, 15))

    def create_analytics_section(self):
        """Crear sección de análisis (rendimiento y servicios populares)"""
        analytics_frame = tk.Frame(self.content_frame, bg='#f8fafc')
        analytics_frame.pack(fill='x')
        
        # Sección Rendimiento por Lavador
        lavador_frame = tk.Frame(analytics_frame, bg='white', relief='solid', borderwidth=1)
        lavador_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        lavador_content = tk.Frame(lavador_frame, bg='white')
        lavador_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            lavador_content,
            text="👥 Rendimiento por Lavador",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        self.lavador_stats_frame = tk.Frame(lavador_content, bg='white')
        self.lavador_stats_frame.pack(fill='both', expand=True)
        
        # Sección Servicios Más Solicitados
        servicios_frame = tk.Frame(analytics_frame, bg='white', relief='solid', borderwidth=1)
        servicios_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        servicios_content = tk.Frame(servicios_frame, bg='white')
        servicios_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        tk.Label(
            servicios_content,
            text="⭐ Servicios Más Solicitados",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='white'
        ).pack(anchor='w', pady=(0, 15))
        
        self.servicios_stats_frame = tk.Frame(servicios_content, bg='white')
        self.servicios_stats_frame.pack(fill='both', expand=True)

    def load_cash_data(self):
        """Cargar datos del cierre de caja"""
        try:
            # Obtener fecha actual
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Query para obtener resumen del día usando la vista optimizada
            summary_query = """
                SELECT 
                    COUNT(*) as total_servicios,
                    COALESCE(SUM(costo), 0) as total_ingresos,
                    COALESCE(SUM(comision_calculada), 0) as total_comisiones,
                    COALESCE(SUM(ganancia_neta), 0) as balance_neto
                FROM vista_registros_completos
                WHERE fecha = %s
            """
            
            summary_result = db.execute_query(summary_query, (today,))
            
            if summary_result:
                data = summary_result[0]
                
                # Actualizar cards de resumen
                self.ingresos_label.config(text=f"${data['total_ingresos']:,.0f}")
                self.comisiones_label.config(text=f"${data['total_comisiones']:,.0f}")
                self.balance_label.config(text=f"${data['balance_neto']:,.0f}")
                self.servicios_label.config(text=str(data['total_servicios']))
            
            # Cargar registros del día en la tabla
            self.load_daily_records(today)
            
            # Cargar estadísticas de lavadores y servicios
            self.load_lavador_stats(today)
            self.load_servicios_stats(today)
            
        except Exception as e:
            print(f"Error cargando datos de caja: {e}")
            messagebox.showerror("Error", "Error al cargar datos del cierre de caja")

    def load_daily_records(self, date):
        """Cargar registros del día en la tabla"""
        try:
            # Limpiar tabla
            for item in self.records_tree.get_children():
                self.records_tree.delete(item)
            
            # Query para obtener registros del día
            records_query = """
                SELECT id, hora, vehiculo_nombre, placa, servicio_nombre,
                    costo, comision_calculada, lavador, pago
                FROM vista_registros_completos
                WHERE fecha = %s
                ORDER BY hora ASC
            """
            
            records = db.execute_query(records_query, (date,))
            
            if records:
                for record in records:
                    hora = str(record['hora'])[:5] if record['hora'] else ''
                    costo = f"${record['costo']:,.0f}"
                    comision = f"${record['comision_calculada']:,.0f}"
                    
                    self.records_tree.insert('', 'end', values=(
                        record['id'],
                        hora,
                        record['vehiculo_nombre'],
                        record['placa'],
                        record['servicio_nombre'],
                        costo,
                        comision,
                        record['lavador'],
                        record['pago']
                    ))
            else:
                self.records_tree.insert('', 'end', values=(
                    '', '', '', '', 'No hay registros para el día de hoy', '', '', '', ''
                ))
                
        except Exception as e:
            print(f"Error cargando registros diarios: {e}")

    def load_lavador_stats(self, date):
        """Cargar estadísticas de rendimiento por lavador"""
        try:
            # Limpiar frame anterior
            for widget in self.lavador_stats_frame.winfo_children():
                widget.destroy()
            
            stats_query = """
                SELECT lavador, COUNT(*) as servicios, SUM(comision_calculada) as total_comision
                FROM vista_registros_completos
                WHERE fecha = %s
                GROUP BY lavador
                ORDER BY total_comision DESC
                LIMIT 5
            """
            
            stats = db.execute_query(stats_query, (date,))
            
            if stats:
                for i, stat in enumerate(stats, 1):
                    row_frame = tk.Frame(self.lavador_stats_frame, bg='white')
                    row_frame.pack(fill='x', pady=2)
                    
                    # Posición
                    pos_label = tk.Label(
                        row_frame,
                        text=f"{i}.",
                        font=('Segoe UI', 10, 'bold'),
                        bg='white',
                        fg='#374151',
                        width=2
                    )
                    pos_label.pack(side='left')
                    
                    # Nombre del lavador
                    name_label = tk.Label(
                        row_frame,
                        text=stat['lavador'],
                        font=('Segoe UI', 10),
                        bg='white',
                        fg='#1e293b'
                    )
                    name_label.pack(side='left', padx=(5, 0))
                    
                    # Estadísticas
                    stats_label = tk.Label(
                        row_frame,
                        text=f"{stat['servicios']} servicios - ${stat['total_comision']:,.0f}",
                        font=('Segoe UI', 9),
                        bg='white',
                        fg='#6b7280'
                    )
                    stats_label.pack(side='right')
            else:
                no_data_label = tk.Label(
                    self.lavador_stats_frame,
                    text="No hay datos de lavadores para hoy",
                    font=('Segoe UI', 10),
                    fg='#6b7280',
                    bg='white'
                )
                no_data_label.pack(expand=True)
                
        except Exception as e:
            print(f"Error cargando estadísticas de lavadores: {e}")

    def load_servicios_stats(self, date):
        """Cargar estadísticas de servicios más solicitados"""
        try:
            # Limpiar frame anterior
            for widget in self.servicios_stats_frame.winfo_children():
                widget.destroy()
            
            stats_query = """
                SELECT servicio_nombre, COUNT(*) as cantidad, SUM(costo) as total_ingresos
                FROM vista_registros_completos
                WHERE fecha = %s
                GROUP BY servicio_nombre
                ORDER BY cantidad DESC
                LIMIT 5
            """
            
            stats = db.execute_query(stats_query, (date,))
            
            if stats:
                for i, stat in enumerate(stats, 1):
                    row_frame = tk.Frame(self.servicios_stats_frame, bg='white')
                    row_frame.pack(fill='x', pady=2)
                    
                    # Posición
                    pos_label = tk.Label(
                        row_frame,
                        text=f"{i}.",
                        font=('Segoe UI', 10, 'bold'),
                        bg='white',
                        fg='#374151',
                        width=2
                    )
                    pos_label.pack(side='left')
                    
                    # Nombre del servicio
                    name_label = tk.Label(
                        row_frame,
                        text=stat['servicio_nombre'],
                        font=('Segoe UI', 10),
                        bg='white',
                        fg='#1e293b'
                    )
                    name_label.pack(side='left', padx=(5, 0))
                    
                    # Estadísticas
                    stats_label = tk.Label(
                        row_frame,
                        text=f"{stat['cantidad']} veces - ${stat['total_ingresos']:,.0f}",
                        font=('Segoe UI', 9),
                        bg='white',
                        fg='#6b7280'
                    )
                    stats_label.pack(side='right')
            else:
                no_data_label = tk.Label(
                    self.servicios_stats_frame,
                    text="No hay datos de servicios para hoy",
                    font=('Segoe UI', 10),
                    fg='#6b7280',
                    bg='white'
                )
                no_data_label.pack(expand=True)
                
        except Exception as e:
            print(f"Error cargando estadísticas de servicios: {e}")

    def show_context_menu(self, event):
        """Mostrar menú contextual para editar/eliminar"""
        # Seleccionar el item donde se hizo clic
        item = self.records_tree.identify_row(event.y)
        if item:
            self.records_tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

    def edit_record(self):
        """Editar registro seleccionado"""
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro para editar")
            return
        
        item = selected[0]
        values = self.records_tree.item(item, 'values')
        record_id = values[0]
        
        if not record_id or record_id == '':
            messagebox.showwarning("Advertencia", "No se puede editar este registro")
            return
        
        # Crear ventana de edición
        self.create_edit_window(record_id, values)

    def create_edit_window(self, record_id, current_values):
        """Crear ventana para editar registro"""
        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Editar Registro")
        edit_window.geometry("400x500")
        edit_window.configure(bg='white')
        edit_window.grab_set()  # Modal
        
        # Título
        title_label = tk.Label(
            edit_window,
            text=f"Editar Registro #{record_id}",
            font=('Segoe UI', 16, 'bold'),
            bg='white',
            fg='#1e293b'
        )
        title_label.pack(pady=(20, 30))
        
        # Frame para campos
        fields_frame = tk.Frame(edit_window, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=30)
        
        # Campo Costo
        tk.Label(fields_frame, text="Costo:", font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        cost_entry = tk.Entry(fields_frame, font=('Segoe UI', 10), relief='solid', borderwidth=1)
        cost_entry.pack(fill='x', pady=(0, 15), ipady=8)
        cost_entry.insert(0, current_values[5].replace('$', '').replace(',', ''))
        
        # Campo Porcentaje
        tk.Label(fields_frame, text="Porcentaje (%):", font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        percent_entry = tk.Entry(fields_frame, font=('Segoe UI', 10), relief='solid', borderwidth=1)
        percent_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Obtener porcentaje actual de la BD
        try:
            query = "SELECT porcentaje FROM registros WHERE id = %s"
            result = db.execute_query(query, (record_id,))
            current_percent = result[0]['porcentaje'] if result else 50.0
            percent_entry.insert(0, str(current_percent))
        except:
            percent_entry.insert(0, "50.00")
        
        # Campo Estado
        tk.Label(fields_frame, text="Estado:", font=('Segoe UI', 10, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        
        status_var = tk.BooleanVar(value=(current_values[8] == 'Pagado'))
        status_check = tk.Checkbutton(
            fields_frame,
            text="Pagado",
            variable=status_var,
            font=('Segoe UI', 10),
            bg='white'
        )
        status_check.pack(anchor='w', pady=(0, 20))
        
        # Botones
        buttons_frame = tk.Frame(fields_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # Botón Cancelar
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancelar",
            font=('Segoe UI', 10),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            command=edit_window.destroy
        )
        cancel_btn.pack(side='left')
        
        # Botón Guardar
        def save_changes():
            try:
                new_cost = float(cost_entry.get().replace(',', ''))
                new_percent = float(percent_entry.get())
                new_status = 'Pagado' if status_var.get() else 'Pendiente'
                
                update_query = """
                    UPDATE registros 
                    SET costo = %s, porcentaje = %s, pago = %s
                    WHERE id = %s
                """
                
                result = db.execute_update(update_query, (new_cost, new_percent, new_status, record_id))
                
                if result:
                    messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                    edit_window.destroy()
                    self.load_cash_data()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el registro")
                    
            except ValueError:
                messagebox.showerror("Error", "Valores numéricos inválidos")
            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        save_btn = tk.Button(
            buttons_frame,
            text="Guardar",
            font=('Segoe UI', 10, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            command=save_changes
        )
        save_btn.pack(side='right')

    def delete_record(self):
        """Eliminar registro seleccionado"""
        selected = self.records_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
            return
        
        item = selected[0]
        values = self.records_tree.item(item, 'values')
        record_id = values[0]
        
        if not record_id or record_id == '':
            messagebox.showwarning("Advertencia", "No se puede eliminar este registro")
            return
        
        # Confirmar eliminación
        confirm = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro que desea eliminar el registro #{record_id}?\n\nEsta acción no se puede deshacer."
        )
        
        if confirm:
            try:
                delete_query = "DELETE FROM registros WHERE id = %s"
                result = db.execute_update(delete_query, (record_id,))
                
                if result:
                    messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                    self.load_cash_data()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el registro")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def export_csv(self):
        """Exportar datos del día a CSV"""
        try:
            import csv
            from tkinter import filedialog
            
            # Obtener datos del día
            today = datetime.now().strftime('%Y-%m-%d')
            
            query = """
                SELECT fecha, hora, vehiculo_nombre, placa, servicio_nombre,
                    costo, porcentaje, comision_calculada, ganancia_neta, 
                    lavador, pago, usuario_nombre
                FROM vista_registros_completos
                WHERE fecha = %s
                ORDER BY hora ASC
            """
            
            data = db.execute_query(query, (today,))
            
            if not data:
                messagebox.showinfo("Información", "No hay datos para exportar del día de hoy")
                return
            
            # Seleccionar ubicación del archivo (SIN initialname)
            filename = filedialog.asksaveasfilename(
                title="Guardar CSV",
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            
            if filename:
                # Si no termina en .csv, agregarlo
                if not filename.endswith('.csv'):
                    filename += '.csv'
                    
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # Escribir encabezados
                    writer.writerow([
                        'Fecha', 'Hora', 'Vehículo', 'Placa', 'Servicio',
                        'Costo', 'Porcentaje', 'Comisión', 'Ganancia Neta',
                        'Lavador', 'Estado', 'Usuario'
                    ])
                    
                    # Escribir datos
                    for row in data:
                        writer.writerow([
                            row['fecha'],
                            row['hora'],
                            row['vehiculo_nombre'],
                            row['placa'],
                            row['servicio_nombre'],
                            row['costo'],
                            row['porcentaje'],
                            row['comision_calculada'],
                            row['ganancia_neta'],
                            row['lavador'],
                            row['pago'],
                            row['usuario_nombre']
                        ])
                
                messagebox.showinfo("Éxito", f"Datos exportados correctamente a:\n{filename}")
                
        except ImportError:
            messagebox.showerror("Error", "Módulo CSV no disponible")
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV: {str(e)}")

    def print_report(self):
        """Imprimir reporte del día"""
        try:
            # Obtener datos del día
            today = datetime.now().strftime('%Y-%m-%d')
            today_formatted = datetime.now().strftime('%A, %d de %B de %Y')
            
            # Obtener resumen
            summary_query = """
                SELECT 
                    COUNT(*) as total_servicios,
                    COALESCE(SUM(costo), 0) as total_ingresos,
                    COALESCE(SUM(comision_calculada), 0) as total_comisiones,
                    COALESCE(SUM(ganancia_neta), 0) as balance_neto
                FROM vista_registros_completos
                WHERE fecha = %s
            """
            
            summary = db.execute_query(summary_query, (today,))
            
            # Obtener registros detallados
            records_query = """
                SELECT hora, vehiculo_nombre, placa, servicio_nombre, costo, lavador, pago
                FROM vista_registros_completos
                WHERE fecha = %s
                ORDER BY hora ASC
            """
            
            records = db.execute_query(records_query, (today,))
            
            # Crear ventana de vista previa del reporte
            preview_window = tk.Toplevel(self.parent)
            preview_window.title("Vista Previa - Reporte Diario")
            preview_window.geometry("800x600")
            preview_window.configure(bg='white')
            
            # Crear área de texto con scrollbar
            text_frame = tk.Frame(preview_window)
            text_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            text_area = tk.Text(text_frame, font=('Courier New', 10), wrap='none')
            scrollbar_v = ttk.Scrollbar(text_frame, orient='vertical', command=text_area.yview)
            scrollbar_h = ttk.Scrollbar(text_frame, orient='horizontal', command=text_area.xview)
            
            text_area.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
            
            # Generar contenido del reporte
            report_content = f"""
    {'='*80}
                            CLEAN CAR - REPORTE DIARIO
    {'='*80}

    Fecha: {today_formatted}
    Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    Usuario: {self.user_data['nombre']}

    {'='*80}
                                RESUMEN FINANCIERO
    {'='*80}
    """
            
            if summary:
                data = summary[0]
                report_content += f"""
    Total de Servicios:     {data['total_servicios']:>10}
    Ingresos del Día:      ${data['total_ingresos']:>10,.0f}
    Total Comisiones:      ${data['total_comisiones']:>10,.0f}
    Balance Neto:          ${data['balance_neto']:>10,.0f}

    """
            
            report_content += f"""
    {'='*80}
                            DETALLE DE SERVICIOS
    {'='*80}

    {'Hora':<8} {'Vehículo':<12} {'Placa':<10} {'Servicio':<20} {'Costo':<12} {'Lavador':<15} {'Estado':<10}
    {'-'*80}
    """
            
            if records:
                for record in records:
                    hora = str(record['hora'])[:5] if record['hora'] else ''
                    vehiculo = record['vehiculo_nombre'][:11] if record['vehiculo_nombre'] else ''
                    placa = record['placa'][:9] if record['placa'] else ''
                    servicio = record['servicio_nombre'][:19] if record['servicio_nombre'] else ''
                    costo = f"${record['costo']:,.0f}"
                    lavador = record['lavador'][:14] if record['lavador'] else ''
                    estado = record['pago'][:9] if record['pago'] else ''
                    
                    report_content += f"{hora:<8} {vehiculo:<12} {placa:<10} {servicio:<20} {costo:<12} {lavador:<15} {estado:<10}\n"
            else:
                report_content += "No hay registros para mostrar.\n"
            
            report_content += f"""
    {'-'*80}

    Fin del reporte.
    """
            
            # Insertar contenido en el área de texto
            text_area.insert('1.0', report_content)
            text_area.configure(state='disabled')  # Solo lectura
            
            # Pack scrollbars y text area
            text_area.pack(side='left', fill='both', expand=True)
            scrollbar_v.pack(side='right', fill='y')
            scrollbar_h.pack(side='bottom', fill='x')
            
            # Frame para botones
            buttons_frame = tk.Frame(preview_window, bg='white')
            buttons_frame.pack(fill='x', padx=20, pady=(0, 20))
            
            # Botón Cerrar
            close_btn = tk.Button(
                buttons_frame,
                text="Cerrar",
                font=('Segoe UI', 10),
                bg='#6b7280',
                fg='white',
                relief='flat',
                padx=20,
                pady=8,
                command=preview_window.destroy
            )
            close_btn.pack(side='left')
            
            # Botón Guardar como TXT
            def save_report():
                from tkinter import filedialog
                
                filename = filedialog.asksaveasfilename(
                    title="Guardar Reporte",
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                    initialname=f"reporte_diario_{today}.txt"
                )
                
                if filename:
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(report_content)
                        messagebox.showinfo("Éxito", f"Reporte guardado en:\n{filename}")
                    except Exception as e:
                        messagebox.showerror("Error", f"Error al guardar reporte: {str(e)}")
            
            save_btn = tk.Button(
                buttons_frame,
                text="💾 Guardar",
                font=('Segoe UI', 10, 'bold'),
                bg='#059669',
                fg='white',
                relief='flat',
                padx=20,
                pady=8,
                command=save_report
            )
            save_btn.pack(side='right')
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar reporte: {str(e)}")

    # Método para actualizar navegación (agregar este método al update_nav_buttons existente)
    def update_nav_buttons_with_cash(self, active_tab):
        """Actualizar estilo de botones de navegación incluyendo cash"""
        # Reset all buttons
        self.btn_register.config(bg='#64748b')
        self.btn_history.config(bg='#64748b')
        if hasattr(self, 'btn_cash'):
            self.btn_cash.config(bg='#64748b')
        
        # Activate selected button
        if active_tab == 'register':
            self.btn_register.config(bg='#2563eb')
        elif active_tab == 'history':
            self.btn_history.config(bg='#2563eb')
        elif active_tab == 'cash':
            if hasattr(self, 'btn_cash'):
                self.btn_cash.config(bg='#2563eb')

    # También necesitarás agregar el botón de cash en create_navigation:
    def create_navigation_with_cash(self, parent):
        """Crear navegación por pestañas incluyendo Cierre de Caja"""
        nav_frame = tk.Frame(parent, bg='#f8fafc')
        nav_frame.pack(fill='x', pady=(0, 10))
        
        # Estilo de botones de navegación
        btn_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 12
        }
        
        # Pestaña Registrar Vehículo
        self.btn_register = tk.Button(
            nav_frame,
            text="➕ Registrar Vehículo",
            bg='#2563eb',
            fg='white',
            command=self.show_register_tab,
            **btn_style
        )
        self.btn_register.pack(side='left', padx=(0, 2))
        
        # Pestaña Consultar Historial
        self.btn_history = tk.Button(
            nav_frame,
            text="🔍 Consultar Historial",
            bg='#64748b',
            fg='white',
            command=self.show_history_tab,
            **btn_style
        )
        self.btn_history.pack(side='left', padx=2)
        
        # Pestaña Cierre de Caja
        self.btn_cash = tk.Button(
            nav_frame,
            text="💰 Cierre de Caja",
            bg='#64748b',
            fg='white',
            command=self.show_cash_tab,
            **btn_style
        )
        self.btn_cash.pack(side='left', padx=2)  