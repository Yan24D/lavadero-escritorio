import tkinter as tk
from tkinter import ttk, messagebox
from database.db_config import db

class AdminLavadores:
    
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        """Configurar la interfaz del módulo de lavadores"""
        # Título del módulo
        title_frame = tk.Frame(self.parent_frame, bg='#f8fafc')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🧑‍💼 Gestión de Lavadores",
            font=('Segoe UI', 24, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(side='left')
        
    def show_lavadores(self):
        """Mostrar módulo de gestión de lavadores"""
        # Título del módulo
        title_frame = tk.Frame(self.content_area, bg='#f8fafc')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="🧑‍💼 Gestión de Lavadores",
            font=('Segoe UI', 24, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(side='left')
        
        # Botón Agregar Lavador
        add_btn = tk.Button(
            title_frame,
            text="➕ Agregar Lavador",
            font=('Segoe UI', 12, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_add_lavador_form
        )
        add_btn.pack(side='right')
        
        # Container con scroll para el contenido
        self.create_scrollable_container()
        
        # Filtros de búsqueda
        self.create_lavadores_filters()
        
        # Tabla de lavadores
        self.create_lavadores_table()
        
        # Cargar datos iniciales
        self.load_lavadores_data()

    def create_scrollable_container(self):
        """Crear container con scroll para lavadores"""
        # Canvas y scrollbar para scroll vertical
        self.lavadores_canvas = tk.Canvas(self.content_area, bg='#f8fafc')
        self.lavadores_scrollbar = ttk.Scrollbar(self.content_area, orient="vertical", command=self.lavadores_canvas.yview)
        self.lavadores_scrollable_frame = tk.Frame(self.lavadores_canvas, bg='#f8fafc')
        
        # Configurar scroll
        self.lavadores_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.lavadores_canvas.configure(scrollregion=self.lavadores_canvas.bbox("all"))
        )
        
        self.lavadores_canvas.create_window((0, 0), window=self.lavadores_scrollable_frame, anchor="nw")
        self.lavadores_canvas.configure(yscrollcommand=self.lavadores_scrollbar.set)
        
        # Pack canvas y scrollbar
        self.lavadores_canvas.pack(side="left", fill="both", expand=True)
        self.lavadores_scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con rueda del mouse
        def _on_mousewheel(event):
            self.lavadores_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.lavadores_canvas.bind("<MouseWheel>", _on_mousewheel)

    def create_lavadores_filters(self):
        """Crear filtros de búsqueda para lavadores"""
        filters_frame = tk.Frame(self.lavadores_scrollable_frame, bg='white', relief='solid', borderwidth=1)
        filters_frame.pack(fill='x', pady=(0, 20))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=15)
        
        # Título de filtros
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
            text="Buscar:",
            font=('Segoe UI', 10, 'bold'),
            bg='white'
        ).pack(side='left', padx=(0, 10))
        
        self.lavador_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.lavador_search_var,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            width=25
        )
        search_entry.pack(side='left', ipady=5, padx=(0, 10))
        
        # Botón buscar
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
            command=self.search_lavadores
        )
        search_btn.pack(side='left')
        
        # Bind para búsqueda en tiempo real
        search_entry.bind('<KeyRelease>', lambda e: self.search_lavadores())

    def create_lavadores_table(self):
        """Crear tabla de lavadores"""
        table_frame = tk.Frame(self.lavadores_scrollable_frame, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        # Título de la tabla
        table_header = tk.Frame(table_frame, bg='#f8fafc')
        table_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            table_header,
            text="👥 Lista de Lavadores",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(side='left', padx=20, pady=15)
        
        # Crear Treeview
        columns = ('ID', 'Nombre', 'Apellido', 'Nombre Completo', 'Estado', 'Fecha Registro', 'Acciones')
        
        self.lavadores_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Configurar columnas
        self.lavadores_tree.heading('ID', text='ID')
        self.lavadores_tree.heading('Nombre', text='Nombre')
        self.lavadores_tree.heading('Apellido', text='Apellido')
        self.lavadores_tree.heading('Nombre Completo', text='Nombre Completo')
        self.lavadores_tree.heading('Estado', text='Estado')
        self.lavadores_tree.heading('Fecha Registro', text='Fecha Registro')
        self.lavadores_tree.heading('Acciones', text='Acciones')
        
        # Configurar ancho de columnas
        self.lavadores_tree.column('ID', width=60, anchor='center')
        self.lavadores_tree.column('Nombre', width=120)
        self.lavadores_tree.column('Apellido', width=120)
        self.lavadores_tree.column('Nombre Completo', width=180)
        self.lavadores_tree.column('Estado', width=100, anchor='center')
        self.lavadores_tree.column('Fecha Registro', width=140, anchor='center')
        self.lavadores_tree.column('Acciones', width=120, anchor='center')
        
        # Menú contextual para acciones
        self.lavadores_context_menu = tk.Menu(self.lavadores_tree, tearoff=0)
        self.lavadores_context_menu.add_command(label="✏️ Editar", command=self.edit_lavador)
        self.lavadores_context_menu.add_command(label="🗑️ Eliminar", command=self.delete_lavador)
        self.lavadores_context_menu.add_separator()
        self.lavadores_context_menu.add_command(label="📊 Ver Estadísticas", command=self.view_lavador_stats)
        
        # Bind del menú contextual
        self.lavadores_tree.bind("<Button-3>", self.show_lavador_context_menu)
        
        # Scrollbar para la tabla
        table_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.lavadores_tree.yview)
        self.lavadores_tree.configure(yscrollcommand=table_scrollbar.set)
        
        # Pack
        self.lavadores_tree.pack(side='left', fill='both', expand=True, padx=20, pady=(0, 20))
        table_scrollbar.pack(side='right', fill='y', pady=(0, 20), padx=(0, 20))

    def load_lavadores_data(self, search_term=""):
        """Cargar datos de lavadores"""
        try:
            # Limpiar tabla
            for item in self.lavadores_tree.get_children():
                self.lavadores_tree.delete(item)
            
            # Query base
            base_query = """
                SELECT id, nombre, apellido, 
                    CONCAT(nombre, ' ', apellido) as nombre_completo,
                    CASE WHEN activo = 1 THEN 'Activo' ELSE 'Inactivo' END as estado,
                    DATE_FORMAT(creado_en, '%d/%m/%Y') as fecha_registro,
                    activo
                FROM lavadores
                WHERE 1=1
            """
            
            params = []
            
            # Filtro de búsqueda
            if search_term:
                base_query += " AND (nombre LIKE %s OR apellido LIKE %s OR CONCAT(nombre, ' ', apellido) LIKE %s)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern, search_pattern])
            
            base_query += " ORDER BY nombre, apellido"
            
            results = db.execute_query(base_query, params if params else None)
            
            if results:
                for row in results:
                    # Colorear filas según el estado
                    tags = ('active',) if row['activo'] else ('inactive',)
                    
                    self.lavadores_tree.insert('', 'end', values=(
                        row['id'],
                        row['nombre'],
                        row['apellido'],
                        row['nombre_completo'],
                        row['estado'],
                        row['fecha_registro'],
                        '🔧 Acciones'
                    ), tags=tags)
            
            # Configurar tags de colores
            self.lavadores_tree.tag_configure('active', background='#f0fdf4')  # Verde claro
            self.lavadores_tree.tag_configure('inactive', background='#fef2f2')  # Rojo claro
            
        except Exception as e:
            print(f"Error cargando lavadores: {e}")
            messagebox.showerror("Error", "Error al cargar la lista de lavadores")

    def search_lavadores(self):
        """Buscar lavadores"""
        search_term = self.lavador_search_var.get().strip()
        self.load_lavadores_data(search_term)

    def show_lavador_context_menu(self, event):
        """Mostrar menú contextual para lavador"""
        item = self.lavadores_tree.identify_row(event.y)
        if item:
            self.lavadores_tree.selection_set(item)
            self.lavadores_context_menu.post(event.x_root, event.y_root)

    def show_add_lavador_form(self):
        """Mostrar formulario para agregar lavador"""
        self.show_lavador_form("Agregar Lavador", "add")

    def edit_lavador(self):
        """Editar lavador seleccionado"""
        selected = self.lavadores_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un lavador para editar")
            return
        
        item = selected[0]
        values = self.lavadores_tree.item(item, 'values')
        lavador_id = values[0]
        
        if not lavador_id:
            messagebox.showwarning("Advertencia", "No se puede editar este lavador")
            return
        
        self.show_lavador_form("Editar Lavador", "edit", lavador_id)

    def show_lavador_form(self, title, mode, lavador_id=None):
        """Mostrar formulario para agregar/editar lavador"""
        # Crear ventana modal
        form_window = tk.Toplevel(self.parent)
        form_window.title(title)
        form_window.geometry("500x400")
        form_window.configure(bg='white')
        form_window.grab_set()
        form_window.resizable(False, False)
        
        # Centrar ventana
        form_window.transient(self.parent)
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (500 // 2)
        y = (form_window.winfo_screenheight() // 2) - (400 // 2)
        form_window.geometry(f"500x400+{x}+{y}")
        
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
            text="Nombre:",
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
        
        # Campo Apellido
        tk.Label(
            fields_frame,
            text="Apellido:",
            font=('Segoe UI', 12, 'bold'),
            bg='white',
            fg='#374151'
        ).pack(anchor='w', pady=(0, 5))
        
        apellido_var = tk.StringVar()
        apellido_entry = tk.Entry(
            fields_frame,
            textvariable=apellido_var,
            font=('Segoe UI', 12),
            relief='solid',
            borderwidth=1,
            bg='#f9fafb'
        )
        apellido_entry.pack(fill='x', pady=(0, 20), ipady=10)
        
        # Campo Estado (solo para edición)
        estado_var = tk.BooleanVar(value=True)
        if mode == "edit":
            tk.Label(
                fields_frame,
                text="Estado:",
                font=('Segoe UI', 12, 'bold'),
                bg='white',
                fg='#374151'
            ).pack(anchor='w', pady=(0, 5))
            
            estado_check = tk.Checkbutton(
                fields_frame,
                text="Activo",
                variable=estado_var,
                font=('Segoe UI', 12),
                bg='white',
                fg='#374151'
            )
            estado_check.pack(anchor='w', pady=(0, 30))
        
        # Cargar datos si es edición
        if mode == "edit" and lavador_id:
            try:
                query = "SELECT nombre, apellido, activo FROM lavadores WHERE id = %s"
                result = db.execute_query(query, (lavador_id,))
                if result:
                    data = result[0]
                    nombre_var.set(data['nombre'])
                    apellido_var.set(data['apellido'])
                    estado_var.set(bool(data['activo']))
            except Exception as e:
                print(f"Error cargando datos del lavador: {e}")
        
        # Frame para botones
        buttons_frame = tk.Frame(fields_frame, bg='white')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
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
        def save_lavador():
            nombre = nombre_var.get().strip()
            apellido = apellido_var.get().strip()
            
            if not nombre or not apellido:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return
            
            try:
                if mode == "add":
                    query = "INSERT INTO lavadores (nombre, apellido, activo) VALUES (%s, %s, 1)"
                    params = (nombre, apellido)
                    success_msg = "Lavador agregado correctamente"
                else:  # edit
                    query = "UPDATE lavadores SET nombre = %s, apellido = %s, activo = %s WHERE id = %s"
                    params = (nombre, apellido, int(estado_var.get()), lavador_id)
                    success_msg = "Lavador actualizado correctamente"
                
                result = db.execute_insert(query, params) if mode == "add" else db.execute_update(query, params)
                
                if result is not None:
                    messagebox.showinfo("Éxito", success_msg)
                    form_window.destroy()
                    self.load_lavadores_data()  # Recargar datos
                else:
                    messagebox.showerror("Error", "No se pudo guardar el lavador")
                    
            except Exception as e:
                print(f"Error guardando lavador: {e}")
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
            command=save_lavador
        )
        save_btn.pack(side='right')
        
        # Foco inicial
        nombre_entry.focus()

    def delete_lavador(self):
        """Eliminar lavador seleccionado"""
        selected = self.lavadores_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un lavador para eliminar")
            return
        
        item = selected[0]
        values = self.lavadores_tree.item(item, 'values')
        lavador_id = values[0]
        nombre_completo = values[3]
        
        if not lavador_id:
            messagebox.showwarning("Advertencia", "No se puede eliminar este lavador")
            return
        
        # Verificar si el lavador tiene registros asociados
        try:
            check_query = "SELECT COUNT(*) as count FROM registros WHERE lavador LIKE %s"
            check_result = db.execute_query(check_query, (f"%{nombre_completo}%",))
            
            if check_result and check_result[0]['count'] > 0:
                # Confirmar si quiere desactivar en lugar de eliminar
                confirm = messagebox.askyesno(
                    "Lavador con registros",
                    f"El lavador '{nombre_completo}' tiene registros asociados.\n\n"
                    "¿Desea desactivarlo en lugar de eliminarlo?\n\n"
                    "• SÍ: Desactivar lavador (recomendado)\n"
                    "• NO: Cancelar operación"
                )
                
                if confirm:
                    # Desactivar en lugar de eliminar
                    update_query = "UPDATE lavadores SET activo = 0 WHERE id = %s"
                    result = db.execute_update(update_query, (lavador_id,))
                    
                    if result:
                        messagebox.showinfo("Éxito", f"Lavador '{nombre_completo}' desactivado correctamente")
                        self.load_lavadores_data()
                    else:
                        messagebox.showerror("Error", "No se pudo desactivar el lavador")
            else:
                # Confirmar eliminación definitiva
                confirm = messagebox.askyesno(
                    "Confirmar Eliminación",
                    f"¿Está seguro que desea eliminar definitivamente al lavador '{nombre_completo}'?\n\n"
                    "Esta acción no se puede deshacer."
                )
                
                if confirm:
                    delete_query = "DELETE FROM lavadores WHERE id = %s"
                    result = db.execute_update(delete_query, (lavador_id,))
                    
                    if result:
                        messagebox.showinfo("Éxito", f"Lavador '{nombre_completo}' eliminado correctamente")
                        self.load_lavadores_data()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el lavador")
                        
        except Exception as e:
            print(f"Error eliminando lavador: {e}")
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")

    def view_lavador_stats(self):
        """Ver estadísticas del lavador seleccionado"""
        selected = self.lavadores_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un lavador para ver estadísticas")
            return
        
        item = selected[0]
        values = self.lavadores_tree.item(item, 'values')
        nombre_completo = values[3]
        
        # Crear ventana de estadísticas
        stats_window = tk.Toplevel(self.parent)
        stats_window.title(f"Estadísticas - {nombre_completo}")
        stats_window.geometry("600x500")
        stats_window.configure(bg='white')
        stats_window.grab_set()
        
        # Centrar ventana
        stats_window.transient(self.parent)
        stats_window.update_idletasks()
        x = (stats_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (stats_window.winfo_screenheight() // 2) - (500 // 2)
        stats_window.geometry(f"600x500+{x}+{y}")
        
        try:
            # Query para estadísticas
            stats_query = """
                SELECT 
                    COUNT(*) as total_servicios,
                    COALESCE(SUM(costo), 0) as total_ingresos,
                    COALESCE(SUM(comision_calculada), 0) as total_comisiones,
                    MIN(fecha) as primera_fecha,
                    MAX(fecha) as ultima_fecha
                FROM vista_registros_completos
                WHERE lavador = %s
            """
            
            stats_data = db.execute_query(stats_query, (nombre_completo,))
            
            # Título
            title_label = tk.Label(
                stats_window,
                text=f"📊 Estadísticas de {nombre_completo}",
                font=('Segoe UI', 18, 'bold'),
                bg='white',
                fg='#1e293b'
            )
            title_label.pack(pady=(30, 40))
            
            if stats_data and stats_data[0]['total_servicios'] > 0:
                data = stats_data[0]
                
                # Frame para estadísticas
                stats_frame = tk.Frame(stats_window, bg='white')
                stats_frame.pack(fill='both', expand=True, padx=50)
                
                # Cards de estadísticas
                cards = [
                    ("🔧 Total Servicios", str(data['total_servicios']), "#2563eb"),
                    ("💰 Ingresos Generados", f"${data['total_ingresos']:,.0f}", "#059669"),
                    ("💳 Comisiones Ganadas", f"${data['total_comisiones']:,.0f}", "#d97706"),
                    ("📅 Período", f"{data['primera_fecha']} - {data['ultima_fecha']}", "#7c3aed")
                ]
                
                for i, (title, value, color) in enumerate(cards):
                    card_frame = tk.Frame(stats_frame, bg=color, relief='solid', borderwidth=1)
                    card_frame.pack(fill='x', pady=10)
                    
                    card_content = tk.Frame(card_frame, bg=color)
                    card_content.pack(fill='x', padx=20, pady=15)
                    
                    tk.Label(
                        card_content,
                        text=title,
                        font=('Segoe UI', 12, 'bold'),
                        fg='white',
                        bg=color
                    ).pack()
                    
                    tk.Label(
                        card_content,
                        text=value,
                        font=('Segoe UI', 16, 'bold'),
                        fg='white',
                        bg=color
                    ).pack(pady=(5, 0))
            else:
                # Sin datos
                no_data_label = tk.Label(
                    stats_window,
                    text="No hay estadísticas disponibles\npara este lavador",
                    font=('Segoe UI', 14),
                    fg='#6b7280',
                    bg='white',
                    justify='center'
                )
                no_data_label.pack(expand=True)
            
            # Botón cerrar
            close_btn = tk.Button(
                stats_window,
                text="Cerrar",
                font=('Segoe UI', 12),
                bg='#6b7280',
                fg='white',
                relief='flat',
                padx=30,
                pady=12,
                cursor='hand2',
                command=stats_window.destroy
            )
            close_btn.pack(pady=(20, 30))
            
        except Exception as e:
            print(f"Error cargando estadísticas: {e}")
            messagebox.showerror("Error", "Error al cargar estadísticas del lavador")
