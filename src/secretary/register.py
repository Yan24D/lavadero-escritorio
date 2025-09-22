"""
Módulo de Registro de Servicios para Secretario
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, time
from database.db_config import db

class SecretaryRegisterPanel:
    """Panel principal de registro de servicios para secretario"""
    
    def __init__(self, parent, user_data, on_logout_callback):
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout_callback
        self.services_data = []
        self.selected_service = None
        
        self.setup_ui()
        self.load_services()
    
    def setup_ui(self):
        """Configurar interfaz principal"""
        # Limpiar ventana
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.parent.configure(bg='#f8fafc')
        self.parent.geometry("1400x900")
        self.parent.title("Clean Car - Panel Secretario")
        
        # Header
        self.create_header()
        
        # Contenido principal
        main_container = tk.Frame(self.parent, bg='#f8fafc')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
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
        
        # Hora actual
        time_label = tk.Label(
            right_frame,
            text=f"🕐 {today.strftime('%H:%M:%S')}",
            font=('Segoe UI', 10),
            fg='white',
            bg='#2563eb'
        )
        time_label.pack(side='right', padx=(0, 20))
        
        # Usuario
        user_label = tk.Label(
            right_frame,
            text=f"👤 {self.user_data['nombre']}",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#2563eb'
        )
        user_label.pack(side='right', padx=(0, 20))
        
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
    
    def create_navigation(self, parent):
        """Crear navegación por pestañas"""
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
        
        # Indicador de notificaciones en Cierre de Caja
        cash_badge = tk.Label(
            nav_frame,
            text="3",
            font=('Segoe UI', 8, 'bold'),
            bg='#dc2626',
            fg='white',
            width=2,
            height=1
        )
        cash_badge.place(in_=self.btn_cash, x=150, y=5)
    
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
        
        # Contenedor principal con dos columnas
        main_container = tk.Frame(self.content_frame, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        # Columna izquierda - Servicios disponibles
        self.create_services_section(main_container)
        
        # Columna derecha - Formulario de registro
        self.create_form_section(main_container)
    
    def create_services_section(self, parent):
        """Crear sección de servicios disponibles"""
        services_frame = tk.Frame(parent, bg='#f8fafc')
        services_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Título
        services_title = tk.Label(
            services_frame,
            text="Servicios Disponibles",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        services_title.pack(anchor='w', pady=(0, 10))
        
        # Subtítulo
        services_subtitle = tk.Label(
            services_frame,
            text="Haga clic para seleccionar rápidamente",
            font=('Segoe UI', 10),
            fg='#64748b',
            bg='#f8fafc'
        )
        services_subtitle.pack(anchor='w', pady=(0, 15))
        
        # Container para las cards de servicios
        self.services_container = tk.Frame(services_frame, bg='#f8fafc')
        self.services_container.pack(fill='both', expand=True)
    
    def create_form_section(self, parent):
        """Crear formulario de registro"""
        # Frame contenedor principal
        form_container = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        form_container.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Canvas para scroll
        form_canvas = tk.Canvas(form_container, bg='white')
        scrollbar = ttk.Scrollbar(form_container, orient="vertical", command=form_canvas.yview)
        form_frame = tk.Frame(form_canvas, bg='white')
        
        # Configurar scroll
        form_frame.bind(
            "<Configure>",
            lambda e: form_canvas.configure(scrollregion=form_canvas.bbox("all"))
        )
        
        form_canvas.create_window((0, 0), window=form_frame, anchor="nw")
        form_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        form_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Padding interno (ahora en form_frame en lugar de form_content)
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
        
        # ... resto del código del formulario igual ...
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
        
        # Segunda fila - Vehículo y Placa
        row2 = tk.Frame(form_content, bg='white')
        row2.pack(fill='x', pady=(0, 15))
        
        # Vehículo
        vehicle_frame = tk.Frame(row2, bg='white')
        vehicle_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        tk.Label(
            vehicle_frame,
            text="Vehículo:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.vehicle_entry = tk.Entry(
            vehicle_frame,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.vehicle_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
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
        
        # Tercera fila - Tipo de Lavado
        row3 = tk.Frame(form_content, bg='white')
        row3.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            row3,
            text="Tipo de Lavado:",
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
        self.percent_entry.insert(0, "0.00")
        
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
        
        self.washer_entry = tk.Entry(
            row5,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        self.washer_entry.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Sexta fila - Método de Pago
        row6 = tk.Frame(form_content, bg='white')
        row6.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            row6,
            text="Método de Pago:",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w')
        
        self.payment_var = tk.StringVar(value="efectivo")
        payment_frame = tk.Frame(row6, bg='white')
        payment_frame.pack(fill='x', pady=(5, 0))
        
        tk.Radiobutton(
            payment_frame,
            text="Efectivo",
            variable=self.payment_var,
            value="efectivo",
            font=('Segoe UI', 10),
            bg='white',
            fg='#374151'
        ).pack(side='left', padx=(0, 20))
        
        tk.Radiobutton(
            payment_frame,
            text="Tarjeta",
            variable=self.payment_var,
            value="tarjeta",
            font=('Segoe UI', 10),
            bg='white',
            fg='#374151'
        ).pack(side='left', padx=(0, 20))
        
        tk.Radiobutton(
            payment_frame,
            text="Transferencia",
            variable=self.payment_var,
            value="transferencia",
            font=('Segoe UI', 10),
            bg='white',
            fg='#374151'
        ).pack(side='left')
        
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
    
    def load_services(self):
        """Cargar servicios disponibles desde la BD"""
        try:
            query = "SELECT id, nombre, descripcion, precio FROM servicios WHERE activo = 1"
            self.services_data = db.execute_query(query)
            
            if self.services_data:
                # Actualizar combobox
                service_names = [f"{s['nombre']} - ${s['precio']:,.0f}" for s in self.services_data]
                if hasattr(self, 'service_combo'):
                    self.service_combo['values'] = service_names
                
                # Crear cards de servicios
                self.create_service_cards()
            
        except Exception as e:
            print(f"Error cargando servicios: {e}")
            messagebox.showerror("Error", "Error al cargar los servicios disponibles")
    
    def create_service_cards(self):
        """Crear cards de servicios disponibles"""
        # Limpiar container
        for widget in self.services_container.winfo_children():
            widget.destroy()
        
        # Grid para las cards
        row = 0
        col = 0
        max_cols = 2
        
        for service in self.services_data:
            card_frame = tk.Frame(
                self.services_container,
                bg='white',
                relief='solid',
                borderwidth=1,
                cursor='hand2'
            )
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Contenido de la card
            card_content = tk.Frame(card_frame, bg='white')
            card_content.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Ícono circular
            icon_frame = tk.Frame(card_content, bg='#2563eb', width=60, height=60)
            icon_frame.pack_propagate(False)
            icon_frame.pack(pady=(0, 15))
            
            icon_label = tk.Label(
                icon_frame,
                text="🚗",
                font=('Segoe UI', 20),
                fg='white',
                bg='#2563eb'
            )
            icon_label.place(relx=0.5, rely=0.5, anchor='center')
            
            # Nombre del servicio
            name_label = tk.Label(
                card_content,
                text=service['nombre'],
                font=('Segoe UI', 12, 'bold'),
                fg='#1e293b',
                bg='white'
            )
            name_label.pack(pady=(0, 5))
            
            # Precio
            price_label = tk.Label(
                card_content,
                text=f"${service['precio']:,.0f}",
                font=('Segoe UI', 14, 'bold'),
                fg='#2563eb',
                bg='white'
            )
            price_label.pack(pady=(0, 5))
            
            # Tipo
            type_label = tk.Label(
                card_content,
                text="Automóvil",
                font=('Segoe UI', 9),
                fg='#64748b',
                bg='white'
            )
            type_label.pack()
            
            # Evento click
            def on_card_click(s=service):
                self.select_service_from_card(s)
            
            card_frame.bind("<Button-1>", lambda e, s=service: self.select_service_from_card(s))
            for child in card_frame.winfo_children():
                child.bind("<Button-1>", lambda e, s=service: self.select_service_from_card(s))
                for grandchild in child.winfo_children():
                    grandchild.bind("<Button-1>", lambda e, s=service: self.select_service_from_card(s))
            
            # Configurar grid
            self.services_container.grid_columnconfigure(col, weight=1)
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
    
    def select_service_from_card(self, service):
        """Seleccionar servicio desde las cards"""
        self.selected_service = service
        
        # Actualizar combobox y costo
        service_text = f"{service['nombre']} - ${service['precio']:,.0f}"
        self.service_var.set(service_text)
        self.cost_entry.delete(0, tk.END)
        self.cost_entry.insert(0, f"{service['precio']:,.0f}")
        
        print(f"Servicio seleccionado: {service['nombre']} - ${service['precio']}")
    
    def clear_form(self):
        """Limpiar formulario"""
        # Mantener fecha y hora actuales
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))
        
        # Limpiar otros campos
        self.vehicle_entry.delete(0, tk.END)
        self.plate_entry.delete(0, tk.END)
        self.service_var.set("")
        self.cost_entry.delete(0, tk.END)
        self.percent_entry.delete(0, tk.END)
        self.percent_entry.insert(0, "0.00")
        self.washer_entry.delete(0, tk.END)
        self.payment_var.set("efectivo")
        self.observations_text.delete(1.0, tk.END)
        
        self.selected_service = None
    
    def register_service(self):
        """Registrar nuevo servicio"""
        # Validar campos requeridos
        if not self.vehicle_entry.get().strip():
            messagebox.showerror("Error", "El campo Vehículo es obligatorio")
            return
        
        if not self.selected_service:
            messagebox.showerror("Error", "Debe seleccionar un tipo de lavado")
            return
        
        if not self.cost_entry.get().strip():
            messagebox.showerror("Error", "El campo Costo es obligatorio")
            return
        
        try:
            # Preparar datos
            registro_data = {
                'fecha': self.date_entry.get(),
                'hora': self.time_entry.get(),
                'vehiculo': self.vehicle_entry.get().strip(),
                'placa': self.plate_entry.get().strip() or None,
                'tipo_lavado_id': self.selected_service['id'],
                'costo': float(self.cost_entry.get().replace(',', '')),
                'porcentaje': float(self.percent_entry.get()) if self.percent_entry.get() else 0.0,
                'lavador': self.washer_entry.get().strip() or None,
                'observaciones': self.observations_text.get(1.0, tk.END).strip() or None,
                'metodo_pago': self.payment_var.get(),
                'usuario_id': self.user_data['id']
            }
            
            # Insertar en base de datos
            query = """
                INSERT INTO registros 
                (fecha, hora, vehiculo, placa, tipo_lavado_id, costo, porcentaje, 
                 lavador, observaciones, metodo_pago, usuario_id)
                VALUES (%(fecha)s, %(hora)s, %(vehiculo)s, %(placa)s, %(tipo_lavado_id)s,
                        %(costo)s, %(porcentaje)s, %(lavador)s, %(observaciones)s, 
                        %(metodo_pago)s, %(usuario_id)s)
            """
            
            registro_id = db.execute_insert(query, registro_data)
            
            if registro_id:
                # Registrar movimiento en caja
                caja_data = {
                    'fecha': registro_data['fecha'],
                    'tipo': 'ingreso',
                    'monto': registro_data['costo'],
                    'concepto': f"Servicio: {self.selected_service['nombre']} - {registro_data['vehiculo']}",
                    'responsable_id': self.user_data['id'],
                    'registro_id': registro_id
                }
                
                caja_query = """
                    INSERT INTO caja (fecha, tipo, monto, concepto, responsable_id, registro_id)
                    VALUES (%(fecha)s, %(tipo)s, %(monto)s, %(concepto)s, %(responsable_id)s, %(registro_id)s)
                """
                
                db.execute_insert(caja_query, caja_data)
                
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
        columns = ('ID', 'Fecha', 'Hora', 'Vehículo', 'Placa', 'Servicio', 'Costo', 'Lavador', 'Pago')
        
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
        self.history_tree.heading('Pago', text='Método Pago')
        
        # Configurar ancho de columnas
        self.history_tree.column('ID', width=50, anchor='center')
        self.history_tree.column('Fecha', width=100, anchor='center')
        self.history_tree.column('Hora', width=80, anchor='center')
        self.history_tree.column('Vehículo', width=120)
        self.history_tree.column('Placa', width=100, anchor='center')
        self.history_tree.column('Servicio', width=150)
        self.history_tree.column('Costo', width=100, anchor='center')
        self.history_tree.column('Lavador', width=120)
        self.history_tree.column('Pago', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.history_tree.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        scrollbar.pack(side='right', fill='y', pady=20, padx=(0, 20))
    
    def search_history(self):
        """Buscar en el historial"""
        try:
            # Limpiar tabla
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Construir query con filtros
            base_query = """
                SELECT r.id, r.fecha, r.hora, r.vehiculo, r.placa, s.nombre as servicio,
                       r.costo, r.lavador, r.metodo_pago
                FROM registros r
                JOIN servicios s ON r.tipo_lavado_id = s.id
                WHERE 1=1
            """
            
            params = []
            
            # Filtro por fecha
            if self.filter_date.get().strip():
                base_query += " AND r.fecha = %s"
                params.append(self.filter_date.get().strip())
            
            # Filtro por placa
            if self.filter_plate.get().strip():
                base_query += " AND r.placa LIKE %s"
                params.append(f"%{self.filter_plate.get().strip()}%")
            
            # Filtro por lavador
            if self.filter_washer.get().strip():
                base_query += " AND r.lavador LIKE %s"
                params.append(f"%{self.filter_washer.get().strip()}%")
            
            base_query += " ORDER BY r.fecha DESC, r.hora DESC LIMIT 100"
            
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
                        row['vehiculo'],
                        placa,
                        row['servicio'],
                        costo,
                        lavador,
                        row['metodo_pago'].title()
                    ))
            else:
                # Mostrar mensaje de no hay resultados
                self.history_tree.insert('', 'end', values=(
                    '', '', '', 'No se encontraron resultados', '', '', '', '', ''
                ))
                
        except Exception as e:
            print(f"Error buscando historial: {e}")
            messagebox.showerror("Error", "Error al buscar en el historial")
    
    def show_cash_tab(self):
        """Mostrar pestaña de cierre de caja"""
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
        
        # Container principal
        main_container = tk.Frame(self.content_frame, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        # Columna izquierda - Resumen del día
        left_column = tk.Frame(main_container, bg='#f8fafc')
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        self.create_daily_summary(left_column)
        
        # Columna derecha - Movimientos detallados
        right_column = tk.Frame(main_container, bg='#f8fafc')
        right_column.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        self.create_movements_detail(right_column)
        
        # Cargar datos del día
        self.load_daily_cash_data()
    
    def create_daily_summary(self, parent):
        """Crear resumen diario de caja"""
        summary_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        summary_frame.pack(fill='both', expand=True)
        
        summary_content = tk.Frame(summary_frame, bg='white')
        summary_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        summary_title = tk.Label(
            summary_content,
            text="📊 Resumen del Día",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='white'
        )
        summary_title.pack(anchor='w', pady=(0, 20))
        
        # Fecha selector
        date_frame = tk.Frame(summary_content, bg='white')
        date_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            date_frame,
            text="Fecha:",
            font=('Segoe UI', 12, 'bold'),
            bg='white'
        ).pack(side='left')
        
        self.cash_date = tk.Entry(
            date_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            width=15
        )
        self.cash_date.pack(side='left', padx=(10, 10), ipady=5)
        self.cash_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        refresh_btn = tk.Button(
            date_frame,
            text="🔄 Actualizar",
            font=('Segoe UI', 10),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.load_daily_cash_data
        )
        refresh_btn.pack(side='left')
        
        # Cards de resumen
        cards_frame = tk.Frame(summary_content, bg='white')
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Card Ingresos
        self.ingresos_card = self.create_summary_card(
            cards_frame, "💰 Ingresos", "$0", "#059669", 0
        )
        
        # Card Servicios
        self.servicios_card = self.create_summary_card(
            cards_frame, "🚗 Servicios", "0", "#2563eb", 1
        )
        
        # Card Método más usado
        self.metodo_card = self.create_summary_card(
            cards_frame, "💳 Método Popular", "Efectivo", "#d97706", 2
        )
        
        # Separador
        separator = tk.Frame(summary_content, bg='#e5e7eb', height=1)
        separator.pack(fill='x', pady=(20, 20))
        
        # Botones de acción
        actions_frame = tk.Frame(summary_content, bg='white')
        actions_frame.pack(fill='x')
        
        export_btn = tk.Button(
            actions_frame,
            text="📄 Exportar Reporte",
            font=('Segoe UI', 11, 'bold'),
            bg='#0891b2',
            fg='white',
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2'
        )
        export_btn.pack(side='left', padx=(0, 10))
        
        close_btn = tk.Button(
            actions_frame,
            text="🔒 Cerrar Caja",
            font=('Segoe UI', 11, 'bold'),
            bg='#dc2626',
            fg='white',
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2',
            command=self.close_daily_cash
        )
        close_btn.pack(side='right')
    
    def create_summary_card(self, parent, title, value, color, column):
        """Crear card de resumen"""
        card = tk.Frame(parent, bg=color, relief='solid', borderwidth=1, height=80)
        card.pack_propagate(False)
        card.pack(side='left', fill='x', expand=True, padx=5 if column > 0 else 0)
        
        content = tk.Frame(card, bg=color)
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        title_label = tk.Label(
            content,
            text=title,
            font=('Segoe UI', 10),
            fg='white',
            bg=color
        )
        title_label.pack(anchor='w')
        
        value_label = tk.Label(
            content,
            text=value,
            font=('Segoe UI', 16, 'bold'),
            fg='white',
            bg=color
        )
        value_label.pack(anchor='w')
        
        return {'title': title_label, 'value': value_label}
    
    def create_movements_detail(self, parent):
        """Crear detalle de movimientos"""
        detail_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        detail_frame.pack(fill='both', expand=True)
        
        detail_content = tk.Frame(detail_frame, bg='white')
        detail_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        detail_title = tk.Label(
            detail_content,
            text="📝 Movimientos del Día",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='white'
        )
        detail_title.pack(anchor='w', pady=(0, 20))
        
        # Tabla de movimientos
        columns = ('Hora', 'Concepto', 'Monto', 'Método')
        
        self.movements_tree = ttk.Treeview(detail_content, columns=columns, show='headings', height=20)
        
        # Configurar columnas
        self.movements_tree.heading('Hora', text='Hora')
        self.movements_tree.heading('Concepto', text='Concepto')
        self.movements_tree.heading('Monto', text='Monto')
        self.movements_tree.heading('Método', text='Método')
        
        self.movements_tree.column('Hora', width=80, anchor='center')
        self.movements_tree.column('Concepto', width=200)
        self.movements_tree.column('Monto', width=100, anchor='center')
        self.movements_tree.column('Método', width=100, anchor='center')
        
        # Scrollbar
        movements_scrollbar = ttk.Scrollbar(detail_content, orient='vertical', command=self.movements_tree.yview)
        self.movements_tree.configure(yscrollcommand=movements_scrollbar.set)
        
        # Pack
        self.movements_tree.pack(side='left', fill='both', expand=True)
        movements_scrollbar.pack(side='right', fill='y')
    
    def load_daily_cash_data(self):
        """Cargar datos de caja del día"""
        try:
            selected_date = self.cash_date.get().strip()
            
            # Query para resumen del día
            summary_query = """
                SELECT 
                    COUNT(*) as total_servicios,
                    SUM(r.costo) as total_ingresos,
                    r.metodo_pago,
                    COUNT(*) as count_metodo
                FROM registros r
                WHERE r.fecha = %s
                GROUP BY r.metodo_pago
                ORDER BY count_metodo DESC
            """
            
            summary_data = db.execute_query(summary_query, (selected_date,))
            
            # Calcular totales
            total_ingresos = 0
            total_servicios = 0
            metodo_popular = "Efectivo"
            
            if summary_data:
                for row in summary_data:
                    total_servicios += row['total_servicios']
                    if row['total_ingresos']:
                        total_ingresos += row['total_ingresos']
                
                # Método más popular (primer resultado por ORDER BY)
                if summary_data[0]['metodo_pago']:
                    metodo_popular = summary_data[0]['metodo_pago'].title()
            
            # Actualizar cards
            self.ingresos_card['value'].config(text=f"${total_ingresos:,.0f}")
            self.servicios_card['value'].config(text=str(total_servicios))
            self.metodo_card['value'].config(text=metodo_popular)
            
            # Cargar movimientos detallados
            self.load_movements_detail(selected_date)
            
        except Exception as e:
            print(f"Error cargando datos de caja: {e}")
            messagebox.showerror("Error", "Error al cargar datos de caja")
    
    def load_movements_detail(self, selected_date):
        """Cargar detalle de movimientos"""
        try:
            # Limpiar tabla
            for item in self.movements_tree.get_children():
                self.movements_tree.delete(item)
            
            # Query para movimientos
            movements_query = """
                SELECT r.hora, r.vehiculo, s.nombre as servicio, r.costo, r.metodo_pago
                FROM registros r
                JOIN servicios s ON r.tipo_lavado_id = s.id
                WHERE r.fecha = %s
                ORDER BY r.hora DESC
            """
            
            movements_data = db.execute_query(movements_query, (selected_date,))
            
            if movements_data:
                for row in movements_data:
                    hora = str(row['hora']) if row['hora'] else ''
                    concepto = f"{row['servicio']} - {row['vehiculo']}"
                    monto = f"${row['costo']:,.0f}"
                    metodo = row['metodo_pago'].title()
                    
                    self.movements_tree.insert('', 'end', values=(
                        hora, concepto, monto, metodo
                    ))
            else:
                self.movements_tree.insert('', 'end', values=(
                    '', 'No hay movimientos para esta fecha', '', ''
                ))
                
        except Exception as e:
            print(f"Error cargando movimientos: {e}")
    
    def close_daily_cash(self):
        """Cerrar caja del día"""
        result = messagebox.askyesno(
            "Cerrar Caja",
            "¿Está seguro que desea cerrar la caja del día?\n\nEsta acción no se puede deshacer."
        )
        
        if result:
            messagebox.showinfo("Éxito", "Caja cerrada correctamente")
    
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
    
    def clear_content(self):
        """Limpiar contenido actual"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()