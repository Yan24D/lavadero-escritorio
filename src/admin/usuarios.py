"""
Módulo de Gestión de Usuarios y Lavadores
"""
import bcrypt
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from src.admin.base_module import BaseModule

class UsuariosModule(BaseModule):
    """Módulo para gestión de usuarios del sistema y lavadores"""
    
    def setup_module(self):
        """Configurar módulo de usuarios"""
        # Título del módulo
        self.create_header()
        
        # Pestañas para Usuarios y Lavadores
        self.create_tabs()
        
        # Cargar contenido de la pestaña activa
        self.show_usuarios_tab()
    
    def create_header(self):
        """Crear header del módulo"""
        header_frame = tk.Frame(self.parent, bg='#f8fafc')
        header_frame.pack(fill='x', pady=(0, 20))
        
    
    def create_tabs(self):
        """Crear navegación por pestañas"""
        tabs_frame = tk.Frame(self.parent, bg='#f8fafc')
        tabs_frame.pack(fill='x', pady=(0, 10))
        
        btn_style = {
            'font': ('Segoe UI', 12, 'bold'),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 25,
            'pady': 12
        }
        
        # Pestaña Usuarios del Sistema
        self.btn_usuarios = tk.Button(
            tabs_frame,
            text="👤 Usuarios del Sistema",
            bg='#2563eb',
            fg='white',
            command=self.show_usuarios_tab,
            **btn_style
        )
        self.btn_usuarios.pack(side='left', padx=(0, 2))
        
        # Pestaña Lavadores
        self.btn_lavadores = tk.Button(
            tabs_frame,
            text="🧑‍💼 Lavadores",
            bg='#64748b',
            fg='white',
            command=self.show_lavadores_tab,
            **btn_style
        )
        self.btn_lavadores.pack(side='left', padx=2)
        
        # Contenedor para el contenido de las pestañas
        self.tab_content = tk.Frame(self.parent, bg='#f8fafc')
        self.tab_content.pack(fill='both', expand=True)
    
    def show_usuarios_tab(self):
        """Mostrar pestaña de usuarios del sistema"""
        # Actualizar botones
        self.btn_usuarios.config(bg='#2563eb')
        self.btn_lavadores.config(bg='#64748b')
        
        # Limpiar contenido
        for widget in self.tab_content.winfo_children():
            widget.destroy()
        
        # Crear contenido de usuarios
        self.create_usuarios_content()
    
    def show_lavadores_tab(self):
        """Mostrar pestaña de lavadores"""
        # Actualizar botones
        self.btn_usuarios.config(bg='#64748b')
        self.btn_lavadores.config(bg='#2563eb')
        
        # Limpiar contenido
        for widget in self.tab_content.winfo_children():
            widget.destroy()
        
        # Crear contenido de lavadores (reutilizar código de lavadores.py)
        self.create_lavadores_content()
    
    # ==================== CONTENIDO DE USUARIOS ====================
    
    def create_usuarios_content(self):
        """Crear contenido para gestión de usuarios del sistema"""
        # Botón agregar usuario
        btn_frame = tk.Frame(self.tab_content, bg='#f8fafc')
        btn_frame.pack(fill='x', pady=(0, 20))
        
        add_btn = tk.Button(
            btn_frame,
            text="➕ Agregar Usuario",
            font=('Segoe UI', 12, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.show_add_usuario_form
        )
        add_btn.pack(side='right')
        
        # Container con scroll
        self.usuarios_canvas = tk.Canvas(self.tab_content, bg='#f8fafc')
        self.usuarios_scrollbar = ttk.Scrollbar(self.tab_content, orient="vertical", command=self.usuarios_canvas.yview)
        self.usuarios_scrollable = tk.Frame(self.usuarios_canvas, bg='#f8fafc')
        
        self.usuarios_scrollable.bind(
            "<Configure>",
            lambda e: self.usuarios_canvas.configure(scrollregion=self.usuarios_canvas.bbox("all"))
        )
        
        self.usuarios_canvas.create_window((0, 0), window=self.usuarios_scrollable, anchor="nw")
        self.usuarios_canvas.configure(yscrollcommand=self.usuarios_scrollbar.set)
        
        self.usuarios_canvas.pack(side="left", fill="both", expand=True)
        self.usuarios_scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con mouse
        def _on_mousewheel(event):
            self.usuarios_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.usuarios_canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Filtros
        self.create_usuarios_filters()
        
        # Tabla
        self.create_usuarios_table()
        
        # Cargar datos
        self.load_usuarios_data()
    
    def create_usuarios_filters(self):
        """Crear filtros para usuarios"""
        filters_frame = tk.Frame(self.usuarios_scrollable, bg='white', relief='solid', borderwidth=1)
        filters_frame.pack(fill='x', pady=(0, 20))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=15)
        

        
        # Filtro por rol
        rol_frame = tk.Frame(filters_content, bg='white')
        rol_frame.pack(side='left', padx=(0, 20))
        
        tk.Label(rol_frame, text="Rol:", font=('Segoe UI', 10, 'bold'), bg='white').pack(side='left', padx=(0, 10))
        
        self.filter_rol_var = tk.StringVar(value="todos")
        roles = [("Todos", "todos"), ("Admin", "admin"), ("Secretario", "secretario")]
        
        for text, value in roles:
            rb = tk.Radiobutton(
                rol_frame,
                text=text,
                variable=self.filter_rol_var,
                value=value,
                font=('Segoe UI', 10),
                bg='white',
                command=self.search_usuarios
            )
            rb.pack(side='left', padx=5)
        
        # Búsqueda por texto
        search_frame = tk.Frame(filters_content, bg='white')
        search_frame.pack(side='left')
        
        tk.Label(search_frame, text="Buscar:", font=('Segoe UI', 10, 'bold'), bg='white').pack(side='left', padx=(0, 10))
        
        self.usuario_search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            textvariable=self.usuario_search_var,
            font=('Segoe UI', 10),
            relief='solid',
            borderwidth=1,
            width=25
        )
        search_entry.pack(side='left', ipady=5, padx=(0, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.search_usuarios())
        
        search_btn = tk.Button(
            search_frame,
            text="🔍",
            font=('Segoe UI', 10),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=10,
            pady=5,
            cursor='hand2',
            command=self.search_usuarios
        )
        search_btn.pack(side='left')
    
    def create_usuarios_table(self):
        """Crear tabla de usuarios"""
        table_frame = tk.Frame(self.usuarios_scrollable, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        table_header = tk.Frame(table_frame, bg='#f8fafc')
        table_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            table_header,
            text="👥 Lista de Usuarios del Sistema",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(side='left', padx=20, pady=15)
        
        columns = ('ID', 'Nombre', 'Email', 'Rol', 'Provider', 'Fecha Registro', 'Acciones')
        
        self.usuarios_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=12)
        
        self.usuarios_tree.heading('ID', text='ID')
        self.usuarios_tree.heading('Nombre', text='Nombre')
        self.usuarios_tree.heading('Email', text='Email')
        self.usuarios_tree.heading('Rol', text='Rol')
        self.usuarios_tree.heading('Provider', text='Provider')
        self.usuarios_tree.heading('Fecha Registro', text='Fecha Registro')
        self.usuarios_tree.heading('Acciones', text='Acciones')
        
        self.usuarios_tree.column('ID', width=50, anchor='center')
        self.usuarios_tree.column('Nombre', width=180)
        self.usuarios_tree.column('Email', width=200)
        self.usuarios_tree.column('Rol', width=100, anchor='center')
        self.usuarios_tree.column('Provider', width=100, anchor='center')
        self.usuarios_tree.column('Fecha Registro', width=140, anchor='center')
        self.usuarios_tree.column('Acciones', width=120, anchor='center')
        
        # Menú contextual
        self.usuarios_context_menu = tk.Menu(self.usuarios_tree, tearoff=0)
        self.usuarios_context_menu.add_command(label="✏️ Editar", command=self.edit_usuario)
        self.usuarios_context_menu.add_command(label="🗑️ Eliminar", command=self.delete_usuario)
        
        self.usuarios_tree.bind("<Button-3>", self.show_usuario_context_menu)
        
        table_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=table_scrollbar.set)
        
        self.usuarios_tree.pack(side='left', fill='both', expand=True, padx=20, pady=(0, 20))
        table_scrollbar.pack(side='right', fill='y', pady=(0, 20), padx=(0, 20))
    
    def load_usuarios_data(self, search_term="", rol_filter="todos"):
        """Cargar datos de usuarios"""
        try:
            for item in self.usuarios_tree.get_children():
                self.usuarios_tree.delete(item)
            
            base_query = """
                SELECT id, nombre, email, rol, provider,
                       DATE_FORMAT(creado_en, '%d/%m/%Y') as fecha_registro
                FROM usuarios
                WHERE 1=1
            """
            
            params = []
            
            if search_term:
                base_query += " AND (nombre LIKE %s OR email LIKE %s)"
                search_pattern = f"%{search_term}%"
                params.extend([search_pattern, search_pattern])
            
            if rol_filter != "todos":
                base_query += " AND rol = %s"
                params.append(rol_filter)
            
            base_query += " ORDER BY nombre"
            
            results = self.db.execute_query(base_query, params if params else None)
            
            if results:
                for row in results:
                    tags = ('admin',) if row['rol'] == 'admin' else ('secretario',)
                    
                    self.usuarios_tree.insert('', 'end', values=(
                        row['id'],
                        row['nombre'],
                        row['email'],
                        row['rol'].title(),
                        row['provider'].title(),
                        row['fecha_registro'],
                        '🔧 Acciones'
                    ), tags=tags)
            
            self.usuarios_tree.tag_configure('admin', background='#fef3c7')  # Amarillo claro
            self.usuarios_tree.tag_configure('secretario', background='#dbeafe')  # Azul claro
            
        except Exception as e:
            print(f"Error cargando usuarios: {e}")
            messagebox.showerror("Error", "Error al cargar la lista de usuarios")
    
    def search_usuarios(self):
        """Buscar usuarios"""
        search_term = self.usuario_search_var.get().strip()
        rol_filter = self.filter_rol_var.get()
        self.load_usuarios_data(search_term, rol_filter)
    
    def show_usuario_context_menu(self, event):
        """Mostrar menú contextual"""
        item = self.usuarios_tree.identify_row(event.y)
        if item:
            self.usuarios_tree.selection_set(item)
            self.usuarios_context_menu.post(event.x_root, event.y_root)
    
    def show_add_usuario_form(self):
        """Mostrar formulario para agregar usuario"""
        self.show_usuario_form("Agregar Usuario", "add")
    
    def edit_usuario(self):
        """Editar usuario seleccionado"""
        selected = self.usuarios_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para editar")
            return
        
        values = self.usuarios_tree.item(selected[0], 'values')
        usuario_id = values[0]
        
        if not usuario_id:
            messagebox.showwarning("Advertencia", "No se puede editar este usuario")
            return
        
        self.show_usuario_form("Editar Usuario", "edit", usuario_id)
    
    def show_usuario_form(self, title, mode, usuario_id=None):
        """Mostrar formulario para agregar/editar usuario"""
        form_window = tk.Toplevel(self.parent)
        form_window.title(title)
        form_window.geometry("550x600")
        form_window.configure(bg='white')
        form_window.grab_set()
        form_window.resizable(False, False)
        
        form_window.transient(self.parent)
        form_window.update_idletasks()
        x = (form_window.winfo_screenwidth() // 2) - (550 // 2)
        y = (form_window.winfo_screenheight() // 2) - (600 // 2)
        form_window.geometry(f"550x600+{x}+{y}")
        
        # Título
        tk.Label(
            form_window,
            text=title,
            font=('Segoe UI', 18, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(pady=(30, 40))
        
        # Frame para campos con scroll
        canvas = tk.Canvas(form_window, bg='white', height=380)
        scrollbar = ttk.Scrollbar(form_window, orient="vertical", command=canvas.yview)
        fields_frame = tk.Frame(canvas, bg='white')
        
        fields_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=fields_frame, anchor="nw", width=500)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side='left', fill='both', expand=True, padx=(50, 0))
        scrollbar.pack(side='right', fill='y', padx=(0, 50))
        
        # Campo Nombre
        tk.Label(fields_frame, text="Nombre Completo:", font=('Segoe UI', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        nombre_var = tk.StringVar()
        nombre_entry = tk.Entry(fields_frame, textvariable=nombre_var, font=('Segoe UI', 11), relief='solid', borderwidth=1, bg='#f9fafb')
        nombre_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Campo Email
        tk.Label(fields_frame, text="Email:", font=('Segoe UI', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        email_var = tk.StringVar()
        email_entry = tk.Entry(fields_frame, textvariable=email_var, font=('Segoe UI', 11), relief='solid', borderwidth=1, bg='#f9fafb')
        email_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Campo Contraseña (solo para agregar)
        password_var = tk.StringVar()
        if mode == "add":
            tk.Label(fields_frame, text="Contraseña:", font=('Segoe UI', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
            password_entry = tk.Entry(fields_frame, textvariable=password_var, font=('Segoe UI', 11), show='*', relief='solid', borderwidth=1, bg='#f9fafb')
            password_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Campo Rol
        tk.Label(fields_frame, text="Rol:", font=('Segoe UI', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        rol_var = tk.StringVar(value="secretario")
        rol_frame = tk.Frame(fields_frame, bg='white')
        rol_frame.pack(fill='x', pady=(0, 15))
        
        tk.Radiobutton(rol_frame, text="Administrador", variable=rol_var, value="admin", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 20))
        tk.Radiobutton(rol_frame, text="Secretario", variable=rol_var, value="secretario", font=('Segoe UI', 10), bg='white').pack(side='left')
        
        # Campo Provider
        tk.Label(fields_frame, text="Provider:", font=('Segoe UI', 11, 'bold'), bg='white').pack(anchor='w', pady=(0, 5))
        provider_var = tk.StringVar(value="local")
        provider_frame = tk.Frame(fields_frame, bg='white')
        provider_frame.pack(fill='x', pady=(0, 20))
        
        tk.Radiobutton(provider_frame, text="Local", variable=provider_var, value="local", font=('Segoe UI', 10), bg='white').pack(side='left', padx=(0, 20))
        tk.Radiobutton(provider_frame, text="Google", variable=provider_var, value="google", font=('Segoe UI', 10), bg='white').pack(side='left')
        
        # Cargar datos si es edición
        if mode == "edit" and usuario_id:
            try:
                query = "SELECT nombre, email, rol, provider FROM usuarios WHERE id = %s"
                result = self.db.execute_query(query, (usuario_id,))
                if result:
                    data = result[0]
                    nombre_var.set(data['nombre'])
                    email_var.set(data['email'])
                    rol_var.set(data['rol'])
                    provider_var.set(data['provider'])
                    email_entry.config(state='readonly')  # No permitir cambiar email en edición
            except Exception as e:
                print(f"Error cargando datos del usuario: {e}")
        
        # Botones
        buttons_frame = tk.Frame(form_window, bg='white')
        buttons_frame.pack(fill='x', padx=50, pady=20)
        
        tk.Button(
            buttons_frame,
            text="Cancelar",
            font=('Segoe UI', 11),
            bg='#6b7280',
            fg='white',
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2',
            command=form_window.destroy
        ).pack(side='left')
        
        def save_usuario():
            nombre = nombre_var.get().strip()
            email = email_var.get().strip()
            password = password_var.get().strip() if mode == "add" else None
            rol = rol_var.get()
            provider = provider_var.get()
            
            if not nombre or not email:
                messagebox.showerror("Error", "Nombre y Email son obligatorios")
                return
            
            if mode == "add" and not password:
                messagebox.showerror("Error", "La contraseña es obligatoria")
                return
            
            # Validar email único
            try:
                check_query = "SELECT id FROM usuarios WHERE email = %s"
                check_params = [email]
                if mode == "edit":
                    check_query += " AND id != %s"
                    check_params.append(usuario_id)
                
                existing = self.db.execute_query(check_query, tuple(check_params))
                if existing:
                    messagebox.showerror("Error", "El email ya está registrado")
                    return
                
                if mode == "add":
                    # Hashear contraseña con bcrypt
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    
                    query = "INSERT INTO usuarios (nombre, email, password, rol, provider) VALUES (%s, %s, %s, %s, %s)"
                    params = (nombre, email, password_hash, rol, provider)  # ✅ Contraseña hasheada
                    success_msg = "Usuario agregado correctamente"
                else:
                    query = "UPDATE usuarios SET nombre = %s, rol = %s, provider = %s WHERE id = %s"
                    params = (nombre, rol, provider, usuario_id)
                    success_msg = "Usuario actualizado correctamente"
                
                result = self.db.execute_insert(query, params) if mode == "add" else self.db.execute_update(query, params)
                
                if result is not None:
                    messagebox.showinfo("Éxito", success_msg)
                    form_window.destroy()
                    self.load_usuarios_data()
                else:
                    messagebox.showerror("Error", "No se pudo guardar el usuario")
                    
            except Exception as e:
                print(f"Error guardando usuario: {e}")
                messagebox.showerror("Error", f"Error al guardar: {str(e)}")
        
        tk.Button(
            buttons_frame,
            text="Guardar" if mode == "add" else "Actualizar",
            font=('Segoe UI', 11, 'bold'),
            bg='#059669',
            fg='white',
            relief='flat',
            padx=25,
            pady=10,
            cursor='hand2',
            command=save_usuario
        ).pack(side='right')
        
        nombre_entry.focus()
    
    def delete_usuario(self):
        """Eliminar usuario seleccionado"""
        selected = self.usuarios_tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un usuario para eliminar")
            return
        
        values = self.usuarios_tree.item(selected[0], 'values')
        usuario_id = values[0]
        nombre = values[1]
        email = values[2]
        
        if not usuario_id:
            messagebox.showwarning("Advertencia", "No se puede eliminar este usuario")
            return
        
        # Verificar si tiene registros asociados
        try:
            check_query = "SELECT COUNT(*) as count FROM registros WHERE id_usuario = %s"
            check_result = self.db.execute_query(check_query, (usuario_id,))
            
            if check_result and check_result[0]['count'] > 0:
                messagebox.showwarning(
                    "Usuario con registros",
                    f"El usuario '{nombre}' tiene registros asociados y no puede ser eliminado.\n\n"
                    "Los usuarios con historial deben permanecer en el sistema."
                )
            else:
                confirm = messagebox.askyesno(
                    "Confirmar Eliminación",
                    f"¿Está seguro que desea eliminar al usuario '{nombre}'?\n\n"
                    "Email: {email}\n\n"
                    "Esta acción no se puede deshacer."
                )
                
                if confirm:
                    delete_query = "DELETE FROM usuarios WHERE id = %s"
                    result = self.db.execute_update(delete_query, (usuario_id,))
                    
                    if result:
                        messagebox.showinfo("Éxito", f"Usuario '{nombre}' eliminado correctamente")
                        self.load_usuarios_data()
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el usuario")
                        
        except Exception as e:
            print(f"Error eliminando usuario: {e}")
            messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    # ==================== CONTENIDO DE LAVADORES ====================
    
    def create_lavadores_content(self):
        """Crear contenido para gestión de lavadores (reutilizando código)"""
        # Importar y usar el módulo de lavadores
        from src.admin.lavadores import LavadoresModule
        
        # Crear instancia del módulo de lavadores en el tab_content
        self.lavadores_instance = LavadoresModule(self.tab_content, self.user_data, self.db)
    
    def refresh(self):
        """Refrescar datos del módulo"""
        if self.btn_usuarios.cget('bg') == '#2563eb':
            self.load_usuarios_data()
        else:
            if hasattr(self, 'lavadores_instance'):
                self.lavadores_instance.refresh()
    
    def cleanup(self):
        """Limpiar recursos del módulo"""
        if hasattr(self, 'lavadores_instance'):
            self.lavadores_instance.cleanup()