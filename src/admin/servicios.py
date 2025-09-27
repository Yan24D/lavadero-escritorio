"""
Módulo de Gestión de Servicios y Precios
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .base_module import BaseModule

class ServiciosModule(BaseModule):
    """Módulo para gestión completa de servicios y precios"""
    
    def setup_module(self):
        """Configurar módulo de servicios"""
        # Datos de tipos de vehículo
        self.vehicle_types = {
            'motorcycle': 'Motocicleta',
            'car': 'Automóvil', 
            'pickup': 'Camioneta',
            'suv': 'SUV',
            'truck': 'Camión'
        }
        
        # Crear interfaz
        self.create_header()
        self.create_tabs_section()
        
        # Cargar datos iniciales
        self.load_services_data()
    
    def create_header(self):
        """Crear header del módulo"""
        header_frame = tk.Frame(self.parent, bg='#f8fafc')
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="⚙️ Gestión de Servicios y Precios",
            font=('Segoe UI', 24, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(side='left')
        
        # Botón Nuevo Servicio
        add_service_btn = tk.Button(
            header_frame,
            text="➕ Nuevo Servicio",
            font=('Segoe UI', 12, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_add_service_form
        )
        add_service_btn.pack(side='right')
    
    def create_tabs_section(self):
        """Crear sección con pestañas"""
        # Notebook para pestañas
        self.notebook = ttk.Notebook(self.parent)
        self.notebook.pack(fill='both', expand=True)
        
        # Pestaña 1: Lista de Servicios
        self.services_frame = tk.Frame(self.notebook, bg='#f8fafc')
        self.notebook.add(self.services_frame, text='📋 Lista de Servicios')
        
        # Pestaña 2: Matriz de Precios
        self.prices_frame = tk.Frame(self.notebook, bg='#f8fafc')
        self.notebook.add(self.prices_frame, text='💰 Matriz de Precios')
        
        # Configurar cada pestaña
        self.setup_services_tab()
        self.setup_prices_tab()
    
    def setup_services_tab(self):
        """Configurar pestaña de servicios"""
        # Filtros
        self.create_services_filters()
        
        # Tabla de servicios
        self.create_services_table()
    
    def create_services_filters(self):
        """Crear filtros para servicios"""
        filters_frame = tk.Frame(self.services_frame, bg='white', relief='solid', borderwidth=1)
        filters_frame.pack(fill='x', pady=(20, 20), padx=20)
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=15)
        
        # Título
        tk.Label(
            filters_content,
            text="🔍 Filtros de Búsqueda",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='white'
        ).pack(side='left')
        
        # Campo de búsqueda
        search_frame = tk.Frame(filters_content, bg='white')
        search_frame.pack(side='right')
        
        tk.Label(
            search_frame,
            text="Buscar servicio:",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        self.service_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.service_search_var,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            width=25
        )
        search_entry.pack(side='left', ipady=5, padx=(0, 10))
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Buscar",
            font=('Segoe UI', 10, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.search_services
        )
        search_btn.pack(side='left')
        
        search_entry.bind('<KeyRelease>', lambda e: self.search_services())
    
    def create_services_table(self):
        """Crear tabla de servicios"""
        table_frame = tk.Frame(self.services_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Header de tabla
        table_header = tk.Frame(table_frame, bg='#f8fafc')
        table_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            table_header,
            text="📝 Lista de Servicios Disponibles",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(side='left', padx=20, pady=15)
        
        # Treeview para servicios
        columns = ('ID', 'Nombre', 'Descripción', 'Precios Config.', 'Fecha Creación', 'Acciones')
        
        self.services_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        # Configurar columnas
        self.services_tree.heading('ID', text='ID')
        self.services_tree.heading('Nombre', text='Nombre del Servicio')
        self.services_tree.heading('Descripción', text='Descripción')
        self.services_tree.heading('Precios Config.', text='Precios Config.')
        self.services_tree.heading('Fecha Creación', text='Fecha Creación')
        self.services_tree.heading('Acciones', text='Acciones')
        
        # Ancho de columnas
        self.services_tree.column('ID', width=50, anchor='center')
        self.services_tree.column('Nombre', width=200)
        self.services_tree.column('Descripción', width=300)
        self.services_tree.column('Precios Config.', width=120, anchor='center')
        self.services_tree.column('Fecha Creación', width=120, anchor='center')
        self.services_tree.column('Acciones', width=100, anchor='center')
        
        # Menú contextual
        self.services_context_menu = tk.Menu(self.services_tree, tearoff=0)
        self.services_context_menu.add_command(label="✏️ Editar Servicio", command=self.edit_service)
        self.services_context_menu.add_command(label="💰 Configurar Precios", command=self.configure_prices)
        self.services_context_menu.add_separator()
        self.services_context_menu.add_command(label="🗑️ Eliminar Servicio", command=self.delete_service)
        
        self.services_tree.bind("<Button-3>", self.show_services_context_menu)
        self.services_tree.bind("<Double-1>", lambda e: self.edit_service())
        
        # Scrollbar
        services_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.services_tree.yview)
        self.services_tree.configure(yscrollcommand=services_scrollbar.set)
        
        # Pack
        self.services_tree.pack(side='left', fill='both', expand=True, padx=20, pady=(0, 20))
        services_scrollbar.pack(side='right', fill='y', pady=(0, 20), padx=(0, 20))
    
    def setup_prices_tab(self):
        """Configurar pestaña de matriz de precios"""
        # Header de matriz
        matrix_header = tk.Frame(self.prices_frame, bg='#f8fafc')
        matrix_header.pack(fill='x', pady=20, padx=20)
        
        tk.Label(
            matrix_header,
            text="💰 Matriz de Precios por Tipo de Vehículo",
            font=('Segoe UI', 18, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(side='left')
        
        # Botón actualizar matriz
        refresh_matrix_btn = tk.Button(
            matrix_header,
            text="🔄 Actualizar Matriz",
            font=('Segoe UI', 11, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.load_price_matrix
        )
        refresh_matrix_btn.pack(side='right')
        
        # Container para matriz
        self.matrix_container = tk.Frame(self.prices_frame, bg='#f8fafc')
        self.matrix_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Cargar matriz
        self.load_price_matrix()
    
    def load_services_data(self):
        """Cargar datos de servicios"""
        try:
            # Limpiar tabla
            for item in self.services_tree.get_children():
                self.services_tree.delete(item)
            
            # Query para servicios con conteo de precios
            services_query = """
                SELECT 
                    s.id,
                    s.nombre,
                    s.descripcion,
                    COUNT(sp.id) as precios_configurados,
                    DATE_FORMAT(s.creado_en, '%d/%m/%Y') as fecha_creacion
                FROM servicios s
                LEFT JOIN servicio_precios sp ON s.id = sp.id_servicio AND sp.activo = 1
                GROUP BY s.id, s.nombre, s.descripcion, s.creado_en
                ORDER BY s.id DESC
            """
            
            search_term = self.service_search_var.get().strip() if hasattr(self, 'service_search_var') else ""
            params = None
            
            if search_term:
                services_query = services_query.replace(
                    "ORDER BY s.id DESC",
                    "HAVING s.nombre LIKE %s OR s.descripcion LIKE %s ORDER BY s.id DESC"
                )
                search_pattern = f"%{search_term}%"
                params = (search_pattern, search_pattern)
            
            results = self.db.execute_query(services_query, params)
            
            if results:
                for row in results:
                    precios_status = f"{row['precios_configurados']}/5 tipos"
                    
                    self.services_tree.insert('', 'end', values=(
                        row['id'],
                        row['nombre'],
                        row['descripcion'][:50] + "..." if len(row['descripcion']) > 50 else row['descripcion'],
                        precios_status,
                        row['fecha_creacion'],
                        '🔧 Acciones'
                    ))
                    
        except Exception as e:
            print(f"Error cargando servicios: {e}")
            messagebox.showerror("Error", "Error al cargar la lista de servicios")
    
    def search_services(self):
        """Buscar servicios"""
        self.load_services_data()
    
    def show_services_context_menu(self, event):
        """Mostrar menú contextual de servicios"""
        item = self.services_tree.identify_row(event.y)
        if item:
            self.services_tree.selection_set(item)
            self.services_context_menu.post(event.x_root, event.y_root)
    
    def show_add_service_form(self):
        """Mostrar formulario para agregar servicio"""
        self.show_service_form("Nuevo Servicio", "add")
    
    def edit_service(self):
        """Editar servicio seleccionado"""
        selected = self.services_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un servicio para editar")
            return
        
        item = selected[0]
        values = self.services_tree.item(item, 'values')
        service_id = values[0]
        
        self.show_service_form("Editar Servicio", "edit", service_id)
    
    def show_service_form(self, title, mode, service_id=None):
        """Mostrar formulario para servicio"""
        # Crear ventana modal
        form_window = tk.Toplevel(self.parent)
        form_window.title(title)
        form_window.geometry("600x450")
        form_window.configure(bg='white')
        form_window.grab_set()
        form_window.resizable(False, False)
        
        # Centrar ventana
        form_window.transient(self.parent)
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (form_window.winfo_screenheight() // 2) - (450 // 2)
        form_window.geometry(f"600x450+{x}+{y}")
        
        # Título del formulario
        title_label = tk.Label(
            form_window,
            text=title,
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#1e293b'
        )
        title_label.pack(pady=(30, 40))
        
        # Frame para campos
        fields_frame = tk.Frame(form_window, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=50)
        
        # Campo Nombre
        tk.Label(
            fields_frame,
            text="Nombre del Servicio:",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w', pady=(0, 5))
        
        nombre_var = tk.StringVar()
        nombre_entry = tk.Entry(
            fields_frame,
            textvariable=nombre_var,
            font=('Segoe UI', 12),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        nombre_entry.pack(fill='x', pady=(0, 20), ipady=10)
        
        # Campo Descripción
        tk.Label(
            fields_frame,
            text="Descripción:",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w', pady=(0, 5))
        
        # Text widget para descripción
        desc_frame = tk.Frame(fields_frame, bg='white')
        desc_frame.pack(fill='x', pady=(0, 20))
        
        descripcion_text = tk.Text(
            desc_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb',
            height=5,
            wrap=tk.WORD
        )
        descripcion_text.pack(side='left', fill='both', expand=True)
        
        # Scrollbar para descripción
        desc_scrollbar = ttk.Scrollbar(desc_frame, orient='vertical', command=descripcion_text.yview)
        descripcion_text.configure(yscrollcommand=desc_scrollbar.set)
        desc_scrollbar.pack(side='right', fill='y')
        
        # Cargar datos si es edición
        if mode == "edit" and service_id:
            try:
                query = "SELECT nombre, descripcion FROM servicios WHERE id = %s"
                result = self.db.execute_query(query, (service_id,))
                if result:
                    data = result[0]
                    nombre_var.set(data['nombre'])
                    descripcion_text.insert('1.0', data['descripcion'] or "")
            except Exception as e:
                print(f"Error cargando datos del servicio: {e}")
        
        # Frame para botones
        buttons_frame = tk.Frame(fields_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(30, 0))
        
        # Botón Cancelar
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancelar",
            font=('Segoe UI', 12),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            command=form_window.destroy
        )
        cancel_btn.pack(side='left')
        
        # Botón Guardar
        def save_service():
            nombre = nombre_var.get().strip()
            descripcion = descripcion_text.get('1.0', tk.END).strip()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre del servicio es obligatorio")
                return
            
            try:
                if mode == "add":
                    query = "INSERT INTO servicios (nombre, descripcion) VALUES (%s, %s)"
                    params = (nombre, descripcion)
                    success_msg = "Servicio agregado correctamente"
                else:  # edit
                    query = "UPDATE servicios SET nombre = %s, descripcion = %s WHERE id = %s"
                    params = (nombre, descripcion, service_id)
                    success_msg = "Servicio actualizado correctamente"
                
                result = self.db.execute_insert(query, params) if mode == "add" else self.db.execute_update(query, params)
                
                if result is not None:
                    messagebox.showinfo("Éxito", success_msg)
                    form_window.destroy()
                    self.load_services_data()
                    self.load_price_matrix()  # Actualizar matriz también
                else:
                    messagebox.showerror("Error", "No se pudo guardar el servicio")
                    
            except Exception as e:
                print(f"Error guardando servicio: {e}")
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        save_btn = tk.Button(
            buttons_frame,
            text="Guardar" if mode == "add" else "Actualizar",
            font=('Segoe UI', 12, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2',
            command=save_service
        )
        save_btn.pack(side='right')
        
        # Foco inicial
        nombre_entry.focus()
    
    def configure_prices(self):
        """Configurar precios del servicio seleccionado"""
        selected = self.services_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un servicio para configurar precios")
            return
        
        item = selected[0]
        values = self.services_tree.item(item, 'values')
        service_id = values[0]
        service_name = values[1]
        
        self.show_price_config_window(service_id, service_name)
    
    def show_price_config_window(self, service_id, service_name):
        """Mostrar ventana de configuración de precios"""
        # Crear ventana modal
        price_window = tk.Toplevel(self.parent)
        price_window.title(f"Configurar Precios - {service_name}")
        price_window.geometry("700x700")  # Altura mayor
        price_window.configure(bg='white')
        price_window.grab_set()
        price_window.resizable(True, True)  # Permitir redimensionar
        
        # Centrar ventana
        price_window.transient(self.parent)
        price_window.update_idletasks()
        x = (price_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (price_window.winfo_screenheight() // 2) - (700 // 2)
        price_window.geometry(f"700x700+{x}+{y}")
        
        # Canvas con scrollbar para todo el contenido
        main_canvas = tk.Canvas(price_window, bg='white')
        main_scrollbar = ttk.Scrollbar(price_window, orient="vertical", command=main_canvas.yview)
        scrollable_main = tk.Frame(main_canvas, bg='white')
        
        scrollable_main.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        main_canvas.create_window((0, 0), window=scrollable_main, anchor="nw")
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Pack canvas principal
        main_canvas.pack(side="left", fill="both", expand=True)
        main_scrollbar.pack(side="right", fill="y")
        
        # Scroll con mouse wheel
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        main_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Título
        title_label = tk.Label(
            scrollable_main,
            text=f"💰 Configurar Precios\n{service_name}",
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#1e293b',
            justify='center'
        )
        title_label.pack(pady=(30, 40))
        
        # Frame para precios
        prices_frame = tk.Frame(scrollable_main, bg='white')
        prices_frame.pack(fill='x', padx=50)
        
        # Cargar precios actuales
        current_prices = self.get_current_prices(service_id)
        price_vars = {}
        
        # Crear campos para cada tipo de vehículo
        for vehicle_type, vehicle_name in self.vehicle_types.items():
            # Frame para cada precio
            price_row = tk.Frame(prices_frame, bg='white')
            price_row.pack(fill='x', pady=15)
            
            # Label del tipo de vehículo
            vehicle_label = tk.Label(
                price_row,
                text=f"{vehicle_name}:",
                font=('Segoe UI', 14, 'bold'),
                bg='white',
                fg='#374151',
                width=12,
                anchor='w'
            )
            vehicle_label.pack(side='left')
            
            # Frame para entry y COP
            entry_container = tk.Frame(price_row, bg='white')
            entry_container.pack(side='left', padx=(20, 0))
            
            # Entry para precio
            price_var = tk.StringVar()
            price_vars[vehicle_type] = price_var
            
            # Cargar precio actual si existe
            if vehicle_type in current_prices:
                price_var.set(str(int(current_prices[vehicle_type])))
            
            price_entry = tk.Entry(
                entry_container,
                textvariable=price_var,
                font=('Segoe UI', 14),
                relief='solid',
                borderwidth=2,
                bg='#f9fafb',
                width=15
            )
            price_entry.pack(side='left', ipady=10)
            
            tk.Label(
                entry_container,
                text=" COP",
                font=('Segoe UI', 12, 'bold'),
                bg='white',
                fg='#6b7280'
            ).pack(side='left', padx=(10, 0))
        
        # Información adicional
        info_frame = tk.Frame(scrollable_main, bg='#e0f2fe', relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(40, 30), padx=50)
        
        info_content = tk.Frame(info_frame, bg='#e0f2fe')
        info_content.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            info_content,
            text="ℹ️ Información Importante:",
            font=('Segoe UI', 12, 'bold'),
            bg='#e0f2fe',
            fg='#0277bd'
        ).pack(anchor='w')
        
        tk.Label(
            info_content,
            text="• Los precios se actualizarán automáticamente en el sistema\n• Puede modificar estos precios cuando lo necesite\n• Deje en blanco los campos que no apliquen para su negocio",
            font=('Segoe UI', 11),
            bg='#e0f2fe',
            fg='#0277bd',
            justify='left'
        ).pack(anchor='w', pady=(10, 0))
        
        # BOTONES - Frame fijo y visible
        buttons_frame = tk.Frame(scrollable_main, bg='#f8fafc', relief='solid', borderwidth=1)
        buttons_frame.pack(fill='x', pady=30, padx=50)
        
        button_content = tk.Frame(buttons_frame, bg='#f8fafc')
        button_content.pack(fill='x', padx=20, pady=20)
        
        # Función para guardar precios
        def save_prices():
            try:
                saved_count = 0
                errors = []
                
                for vehicle_type, price_var in price_vars.items():
                    price_text = price_var.get().strip()
                    
                    if price_text:  # Si hay precio ingresado
                        try:
                            precio = float(price_text)
                            if precio <= 0:
                                errors.append(f"{self.vehicle_types[vehicle_type]}: El precio debe ser mayor a 0")
                                continue
                            
                            # Verificar si ya existe precio
                            check_query = "SELECT id FROM servicio_precios WHERE id_servicio = %s AND tipo_vehiculo = %s"
                            existing = self.db.execute_query(check_query, (service_id, vehicle_type))
                            
                            if existing:
                                # Actualizar precio existente
                                update_query = """
                                    UPDATE servicio_precios 
                                    SET precio = %s, activo = 1, actualizado_en = NOW()
                                    WHERE id_servicio = %s AND tipo_vehiculo = %s
                                """
                                self.db.execute_update(update_query, (precio, service_id, vehicle_type))
                            else:
                                # Insertar nuevo precio
                                insert_query = """
                                    INSERT INTO servicio_precios (id_servicio, tipo_vehiculo, precio, activo)
                                    VALUES (%s, %s, %s, 1)
                                """
                                self.db.execute_insert(insert_query, (service_id, vehicle_type, precio))
                            
                            saved_count += 1
                            
                        except ValueError:
                            errors.append(f"{self.vehicle_types[vehicle_type]}: Ingrese solo números")
                    else:
                        # Desactivar precio si no hay valor
                        deactivate_query = """
                            UPDATE servicio_precios 
                            SET activo = 0 
                            WHERE id_servicio = %s AND tipo_vehiculo = %s
                        """
                        self.db.execute_update(deactivate_query, (service_id, vehicle_type))
                
                if errors:
                    messagebox.showerror("Errores en los precios", "\n".join(errors))
                    return
                
                if saved_count > 0:
                    messagebox.showinfo("Precios Guardados", f"Se configuraron {saved_count} precios correctamente")
                else:
                    messagebox.showinfo("Precios Actualizados", "Se actualizaron las configuraciones de precios")
                
                price_window.destroy()
                self.load_services_data()
                self.load_price_matrix()
                            
            except Exception as e:
                print(f"Error guardando precios: {e}")
                messagebox.showerror("Error", f"Error al guardar precios:\n{str(e)}")
        
        # Botón Cancelar
        cancel_btn = tk.Button(
            button_content,
            text="❌ Cancelar",
            font=('Segoe UI', 14, 'bold'),
            bg='#dc2626',
            fg='white',
            relief='flat',
            padx=40,
            pady=15,
            cursor='hand2',
            command=price_window.destroy
        )
        cancel_btn.pack(side='left')
        
        # Botón Guardar Precios
        save_btn = tk.Button(
            button_content,
            text="💾 GUARDAR PRECIOS",
            font=('Segoe UI', 14, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=40,
            pady=15,
            cursor='hand2',
            command=save_prices
        )
        save_btn.pack(side='right')
        
        # Asegurar que el contenido sea visible
        scrollable_main.update_idletasks()
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        
        # Espaciado final para asegurar visibilidad
        tk.Frame(scrollable_main, bg='white', height=50).pack()
    
    def get_current_prices(self, service_id):
        """Obtener precios actuales de un servicio"""
        try:
            query = """
                SELECT tipo_vehiculo, precio
                FROM servicio_precios
                WHERE id_servicio = %s AND activo = 1
            """
            results = self.db.execute_query(query, (service_id,))
            
            prices = {}
            if results:
                for row in results:
                    prices[row['tipo_vehiculo']] = row['precio']
            
            return prices
        except Exception as e:
            print(f"Error obteniendo precios actuales: {e}")
            return {}
    
    def delete_service(self):
        """Eliminar servicio seleccionado"""
        selected = self.services_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un servicio para eliminar")
            return
        
        item = selected[0]
        values = self.services_tree.item(item, 'values')
        service_id = values[0]
        service_name = values[1]
        
                    # Verificar si el servicio tiene registros asociados
        try:
            check_query = "SELECT COUNT(*) as count FROM registros WHERE id_servicio = %s"
            check_result = self.db.execute_query(check_query, (service_id,))
            
            if check_result and check_result[0]['count'] > 0:
                messagebox.showwarning(
                    "No se puede eliminar",
                    f"El servicio '{service_name}' tiene registros asociados y no puede ser eliminado.\n\n"
                    "Considere desactivar los precios en lugar de eliminar el servicio."
                )
                return
            
            # Confirmar eliminación
            confirm = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Está seguro que desea eliminar el servicio '{service_name}'?\n\n"
                "Esta acción eliminará:\n"
                "• El servicio\n"
                "• Todos los precios configurados\n\n"
                "Esta acción no se puede deshacer."
            )
            
            if confirm:
                # Primero eliminar precios asociados
                delete_prices_query = "DELETE FROM servicio_precios WHERE id_servicio = %s"
                self.db.execute_update(delete_prices_query, (service_id,))
                
                # Luego eliminar servicio
                delete_service_query = "DELETE FROM servicios WHERE id = %s"
                result = self.db.execute_update(delete_service_query, (service_id,))
                
                if result:
                    messagebox.showinfo("Éxito", f"Servicio '{service_name}' eliminado correctamente")
                    self.load_services_data()
                    self.load_price_matrix()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el servicio")
                    
        except Exception as e:
            print(f"Error eliminando servicio: {e}")
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def load_price_matrix(self):
        """Cargar matriz completa de precios"""
        try:
            # Limpiar matriz anterior
            for widget in self.matrix_container.winfo_children():
                widget.destroy()
            
            # Obtener datos de la vista de precios
            matrix_query = """
                SELECT * FROM vista_lista_precios
                ORDER BY servicio_id, 
                CASE tipo_vehiculo 
                    WHEN 'motorcycle' THEN 1 
                    WHEN 'car' THEN 2 
                    WHEN 'pickup' THEN 3 
                    WHEN 'suv' THEN 4 
                    WHEN 'truck' THEN 5 
                END
            """
            
            results = self.db.execute_query(matrix_query)
            
            if not results:
                no_data_label = tk.Label(
                    self.matrix_container,
                    text="No hay precios configurados\n\nAgregue servicios y configure sus precios",
                    font=('Segoe UI', 14),
                    fg='#6b7280',
                    bg='#f8fafc',
                    justify='center'
                )
                no_data_label.pack(expand=True)
                return
            
            # Agrupar datos por servicio
            services_data = {}
            for row in results:
                service_id = row['servicio_id']
                if service_id not in services_data:
                    services_data[service_id] = {
                        'nombre': row['servicio_nombre'],
                        'descripcion': row['descripcion'],
                        'precios': {}
                    }
                services_data[service_id]['precios'][row['tipo_vehiculo']] = row['precio']
            
            # Crear tabla de matriz
            matrix_frame = tk.Frame(self.matrix_container, bg='white', relief='solid', borderwidth=1)
            matrix_frame.pack(fill='both', expand=True)
            
            # Headers de la tabla
            headers_frame = tk.Frame(matrix_frame, bg='#1e293b')
            headers_frame.pack(fill='x')
            
            # Crear headers
            headers = ['Servicio', 'Motocicleta', 'Automóvil', 'Camioneta', 'SUV', 'Camión', 'Acciones']
            header_widths = [200, 100, 100, 100, 80, 80, 100]
            
            for i, (header, width) in enumerate(zip(headers, header_widths)):
                header_label = tk.Label(
                    headers_frame,
                    text=header,
                    font=('Segoe UI', 11, 'bold'),
                    fg='white',
                    bg='#1e293b',
                    width=width//8,  # Aproximación para ancho
                    relief='solid',
                    borderwidth=1
                )
                header_label.pack(side='left', fill='y')
            
            # Canvas y scrollbar para filas de datos
            canvas = tk.Canvas(matrix_frame, bg='white', highlightthickness=0)
            scrollbar = ttk.Scrollbar(matrix_frame, orient='vertical', command=canvas.yview)
            scrollable_frame = tk.Frame(canvas, bg='white')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Crear filas de datos
            row_colors = ['#ffffff', '#f8fafc']
            
            for i, (service_id, service_data) in enumerate(services_data.items()):
                row_color = row_colors[i % 2]
                row_frame = tk.Frame(scrollable_frame, bg=row_color, relief='solid', borderwidth=1)
                row_frame.pack(fill='x')
                
                # Nombre del servicio
                service_label = tk.Label(
                    row_frame,
                    text=service_data['nombre'][:25] + ("..." if len(service_data['nombre']) > 25 else ""),
                    font=('Segoe UI', 10, 'bold'),
                    bg=row_color,
                    fg='#1e293b',
                    width=25,
                    anchor='w',
                    relief='solid',
                    borderwidth=1
                )
                service_label.pack(side='left', fill='y')
                
                # Precios por tipo de vehículo
                vehicle_order = ['motorcycle', 'car', 'pickup', 'suv', 'truck']
                
                for vehicle_type in vehicle_order:
                    precio = service_data['precios'].get(vehicle_type, 0)
                    precio_text = f"${precio:,.0f}" if precio > 0 else "N/A"
                    color_texto = '#059669' if precio > 0 else '#dc2626'
                    
                    price_label = tk.Label(
                        row_frame,
                        text=precio_text,
                        font=('Segoe UI', 10, 'bold' if precio > 0 else 'normal'),
                        bg=row_color,
                        fg=color_texto,
                        width=12,
                        relief='solid',
                        borderwidth=1
                    )
                    price_label.pack(side='left', fill='y')
                
                # Botón de acciones
                action_btn = tk.Button(
                    row_frame,
                    text="⚙️ Config.",
                    font=('Segoe UI', 9),
                    bg='#2563eb',
                    fg='white',
                    relief='flat',
                    cursor='hand2',
                    command=lambda sid=service_id, sname=service_data['nombre']: self.show_price_config_window(sid, sname)
                )
                action_btn.pack(side='right', padx=5, pady=2)
            
            # Pack canvas y scrollbar
            canvas.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            # Habilitar scroll con rueda del mouse
            def _on_matrix_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind("<MouseWheel>", _on_matrix_mousewheel)
            
            # Resumen al final
            self.create_price_summary(services_data)
            
        except Exception as e:
            print(f"Error cargando matriz de precios: {e}")
            error_label = tk.Label(
                self.matrix_container,
                text="Error al cargar la matriz de precios",
                font=('Segoe UI', 14),
                fg='#dc2626',
                bg='#f8fafc'
            )
            error_label.pack(expand=True)
    
    def create_price_summary(self, services_data):
        """Crear resumen de precios al final de la matriz"""
        summary_frame = tk.Frame(self.matrix_container, bg='#f0f9ff', relief='solid', borderwidth=1)
        summary_frame.pack(fill='x', pady=(20, 0))
        
        summary_content = tk.Frame(summary_frame, bg='#f0f9ff')
        summary_content.pack(fill='x', padx=20, pady=15)
        
        # Título del resumen
        tk.Label(
            summary_content,
            text="📊 Resumen de Precios",
            font=('Segoe UI', 14, 'bold'),
            bg='#f0f9ff',
            fg='#1e40af'
        ).pack(anchor='w')
        
        # Calcular estadísticas
        total_services = len(services_data)
        total_prices = 0
        price_ranges = {'motorcycle': [], 'car': [], 'pickup': [], 'suv': [], 'truck': []}
        
        for service_data in services_data.values():
            for vehicle_type, precio in service_data['precios'].items():
                if precio > 0:
                    total_prices += 1
                    price_ranges[vehicle_type].append(precio)
        
        # Mostrar estadísticas
        stats_text = f"• Total de servicios: {total_services}\n"
        stats_text += f"• Total de precios configurados: {total_prices}\n\n"
        
        # Rangos de precios por tipo de vehículo
        for vehicle_type, vehicle_name in self.vehicle_types.items():
            prices = price_ranges[vehicle_type]
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                avg_price = sum(prices) / len(prices)
                stats_text += f"• {vehicle_name}: ${min_price:,.0f} - ${max_price:,.0f} (Promedio: ${avg_price:,.0f})\n"
        
        tk.Label(
            summary_content,
            text=stats_text,
            font=('Segoe UI', 11),
            bg='#f0f9ff',
            fg='#1e40af',
            justify='left'
        ).pack(anchor='w', pady=(10, 0))
    
    def refresh(self):
        """Refrescar datos del módulo"""
        self.load_services_data()
        self.load_price_matrix()
    
    def cleanup(self):
        """Limpiar recursos del módulo"""
        pass