"""
Sistema de Login y Autenticación con Registro
"""

import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
from database.db_config import db

class LoginWindow:
    """Ventana de inicio de sesión y registro"""
    
    def __init__(self, parent, on_success_callback):
        self.parent = parent
        self.on_success = on_success_callback
        self.remember_me = tk.BooleanVar(value=False)
        self.current_tab = "login"  # 'login' o 'register'
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        # Limpiar ventana
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Configurar ventana principal
        self.parent.configure(bg='#f8f9fa')
        self.parent.geometry("500x700")
        self.parent.resizable(True, True)
        self.parent.minsize(450, 600)
        
        # Canvas con scroll
        canvas = tk.Canvas(self.parent, bg='#f8f9fa', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.parent, orient="vertical", command=canvas.yview)
        
        # Frame scrollable
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

        # Agregar función para centrar al redimensionar
        def center_window(event):
            canvas_width = event.width
            canvas.coords(window_id, canvas_width // 2, 0)

        canvas.bind("<Configure>", center_window)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Habilitar scroll con mouse 
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Contenedor centrado con padding
        center_container = tk.Frame(scrollable_frame, bg='#f8f9fa')
        center_container.pack(expand=True, pady=40)
        
        # Card principal con sombra simulada
        card_shadow = tk.Frame(center_container, bg='#dee2e6', relief='flat')
        card_shadow.pack(padx=3, pady=3, anchor='center')
        
        card_frame = tk.Frame(card_shadow, bg='white', relief='flat', width=400, height=750)
        card_frame.pack_propagate(False)
        card_frame.pack(padx=5, pady=5) 
        
        # Header azul
        header_frame = tk.Frame(card_frame, bg='#0d6efd')
        header_frame.pack(fill='x', pady=(0, 0))
        
        tk.Label(
            header_frame,
            text="Clean Car ",
            font=('Segoe UI', 22, 'bold'),
            fg='white',
            bg='#0d6efd'
        ).pack(pady=(35, 5))
        
        tk.Label(
            header_frame,
            text="Sistema de Gestión para Lavadero",
            font=('Segoe UI', 11),
            fg='#e3f2fd',
            bg='#0d6efd'
        ).pack(pady=(0, 25))
        
        # Tabs container
        tabs_frame = tk.Frame(card_frame, bg='white')
        tabs_frame.pack(fill='x', pady=(0, 0))
        
        self.tab_login = tk.Button(
            tabs_frame,
            text="Iniciar Sesión",
            font=('Segoe UI', 11, 'bold'),
            bg='#0d6efd',
            fg='white',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=12,
            command=lambda: self.switch_tab('login')
        )
        self.tab_login.pack(side='left', fill='x', expand=True)
        
        self.tab_register = tk.Button(
            tabs_frame,
            text="Registrarse",
            font=('Segoe UI', 11),
            bg='#e9ecef',
            fg='#6c757d',
            relief='flat',
            cursor='hand2',
            padx=40,
            pady=12,
            command=lambda: self.switch_tab('register')
        )
        self.tab_register.pack(side='left', fill='x', expand=True)
        
        # Contenedor de contenido
        self.content_frame = tk.Frame(card_frame, bg='white')
        self.content_frame.pack(fill='both', padx=40, pady=25)
        
        # Mostrar login por defecto
        self.show_login_form()
        
        # Footer
        footer_frame = tk.Frame(card_frame, bg='white')
        footer_frame.pack(fill='x', pady=(15, 25))
        
        tk.Label(
            footer_frame,
            text="Clean Car © 2025 | Desarrollado por Victorius",
            font=('Segoe UI', 9),
            fg='#6c757d',
            bg='white'
        ).pack()
        
        # Actualizar canvas después de crear todo
        self.parent.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
        # Mostrar ventana
        self.parent.deiconify()
    
    def switch_tab(self, tab):
        """Cambiar entre tabs de login y registro"""
        self.current_tab = tab
        
        if tab == 'login':
            self.tab_login.config(bg='#0d6efd', fg='white', font=('Segoe UI', 11, 'bold'))
            self.tab_register.config(bg='#e9ecef', fg='#6c757d', font=('Segoe UI', 11))
            self.show_login_form()
        else:
            self.tab_register.config(bg='#0d6efd', fg='white', font=('Segoe UI', 11, 'bold'))
            self.tab_login.config(bg='#e9ecef', fg='#6c757d', font=('Segoe UI', 11))
            self.show_register_form()
    
    def show_login_form(self):
        """Mostrar formulario de login"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Frame interno con scroll propio
        inner_frame = tk.Frame(self.content_frame, bg='white')
        inner_frame.pack(fill='both', expand=True)
        
        # Campo Email
        tk.Label(
            inner_frame,
            text="Email",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529'
        ).pack(anchor='w', pady=(10, 5))
        
        self.login_email_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.login_email_entry.pack(fill='x', pady=(0, 18), ipady=8)
        self.login_email_entry.insert(0, "Ingrese su email")
        self.login_email_entry.config(fg='#adb5bd')
        self.login_email_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(e, "Ingrese su email"))
        self.login_email_entry.bind('<FocusOut>', lambda e: self.restore_placeholder(e, "Ingrese su email"))
        
        # Campo Contraseña
        tk.Label(
            inner_frame,
            text="Contraseña",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529'
        ).pack(anchor='w', pady=(0, 5))
        
        self.login_password_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            show='*',
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.login_password_entry.pack(fill='x', pady=(0, 18), ipady=8)
        self.login_password_entry.insert(0, "Ingrese su contraseña")
        self.login_password_entry.config(show='', fg='#adb5bd')
        self.login_password_entry.bind('<FocusIn>', lambda e: self.clear_password_placeholder(e))
        self.login_password_entry.bind('<FocusOut>', lambda e: self.restore_password_placeholder(e))
        
        # Checkbox Recordar sesión
        remember_frame = tk.Frame(inner_frame, bg='white')
        remember_frame.pack(fill='x', pady=(0, 18))
        
        tk.Checkbutton(
            remember_frame,
            text="Recordar sesión",
            variable=self.remember_me,
            font=('Segoe UI', 9),
            bg='white',
            fg='#6c757d',
            activebackground='white',
            selectcolor='white'
        ).pack(side='left')
        
        # Botón Iniciar Sesión
        login_btn = tk.Button(
            inner_frame,
            text="Iniciar Sesión",
            font=('Segoe UI', 12, 'bold'),
            bg='#0d6efd',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.authenticate
        )
        login_btn.pack(fill='x', pady=(0, 12), ipady=10)
        
        # Link "¿Olvidaste tu contraseña?"
        forgot_link = tk.Label(
            inner_frame,
            text="¿Olvidaste tu contraseña?",
            font=('Segoe UI', 9),
            fg='#0d6efd',
            bg='white',
            cursor='hand2'
        )
        forgot_link.pack(pady=(0, 12))
        # forgot_link.bind('<Button-1>', lambda e: self.forgot_password())  # Deshabilitado por ahora
        
        # Separador
        separator_frame = tk.Frame(inner_frame, bg='white')
        separator_frame.pack(fill='x', pady=12)
        
        tk.Frame(separator_frame, bg='#dee2e6', height=1).pack(side='left', fill='x', expand=True, padx=(0, 10))
        tk.Label(separator_frame, text="o continúa con", font=('Segoe UI', 9), fg='#6c757d', bg='white').pack(side='left')
        tk.Frame(separator_frame, bg='#dee2e6', height=1).pack(side='left', fill='x', expand=True, padx=(10, 0))
        
        # Botón Google (deshabilitado)
        google_btn = tk.Button(
            inner_frame,
            text="Google",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529',
            relief='solid',
            borderwidth=1,
            cursor='hand2',
            state='disabled'  # Deshabilitado
        )
        google_btn.pack(fill='x', pady=(12, 0), ipady=8)
        
        # Eventos de teclado
        self.login_email_entry.bind('<Return>', lambda e: self.login_password_entry.focus())
        self.login_password_entry.bind('<Return>', lambda e: self.authenticate())
        
        # Foco inicial
        self.login_email_entry.focus()
    
    def show_register_form(self):
        """Mostrar formulario de registro"""
        # Limpiar contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Frame interno
        inner_frame = tk.Frame(self.content_frame, bg='white')
        inner_frame.pack(fill='both', expand=True)
        
        # Campo Nombre
        tk.Label(
            inner_frame,
            text="Nombre completo",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529'
        ).pack(anchor='w', pady=(10, 5))
        
        self.register_name_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.register_name_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Campo Email
        tk.Label(
            inner_frame,
            text="Email",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529'
        ).pack(anchor='w', pady=(0, 5))
        
        self.register_email_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.register_email_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Campo Contraseña
        tk.Label(
            inner_frame,
            text="Contraseña",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529'
        ).pack(anchor='w', pady=(0, 5))
        
        self.register_password_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            show='*',
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.register_password_entry.pack(fill='x', pady=(0, 15), ipady=8)
        
        # Campo Confirmar Contraseña
        tk.Label(
            inner_frame,
            text="Confirmar contraseña",
            font=('Segoe UI', 10, 'bold'),
            bg='white',
            fg='#212529'
        ).pack(anchor='w', pady=(0, 5))
        
        self.register_confirm_password_entry = tk.Entry(
            inner_frame,
            font=('Segoe UI', 11),
            show='*',
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.register_confirm_password_entry.pack(fill='x', pady=(0, 18), ipady=8)
        
        # Botón Registrarse
        register_btn = tk.Button(
            inner_frame,
            text="Registrarse",
            font=('Segoe UI', 12, 'bold'),
            bg='#0d6efd',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.register_user
        )
        register_btn.pack(fill='x', pady=(0, 15), ipady=10)
        
        # Nota informativa
        tk.Label(
            inner_frame,
            text="Se creará una cuenta con rol de Secretario.\nEl administrador podrá cambiar el rol posteriormente.",
            font=('Segoe UI', 8),
            fg='#6c757d',
            bg='white',
            justify='center'
        ).pack()
        
        # Eventos de teclado
        self.register_name_entry.bind('<Return>', lambda e: self.register_email_entry.focus())
        self.register_email_entry.bind('<Return>', lambda e: self.register_password_entry.focus())
        self.register_password_entry.bind('<Return>', lambda e: self.register_confirm_password_entry.focus())
        self.register_confirm_password_entry.bind('<Return>', lambda e: self.register_user())
        
        # Foco inicial
        self.register_name_entry.focus()
    
    def clear_placeholder(self, event, placeholder):
        """Limpiar placeholder del campo"""
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, tk.END)
            widget.config(fg='#212529')
    
    def restore_placeholder(self, event, placeholder):
        """Restaurar placeholder si está vacío"""
        widget = event.widget
        if not widget.get():
            widget.insert(0, placeholder)
            widget.config(fg='#adb5bd')
    
    def clear_password_placeholder(self, event):
        """Limpiar placeholder del campo contraseña"""
        widget = event.widget
        if widget.get() == "Ingrese su contraseña":
            widget.delete(0, tk.END)
            widget.config(show='*', fg='#212529')
    
    def restore_password_placeholder(self, event):
        """Restaurar placeholder del campo contraseña"""
        widget = event.widget
        if not widget.get():
            widget.config(show='')
            widget.insert(0, "Ingrese su contraseña")
            widget.config(fg='#adb5bd')
    
    def authenticate(self):
        """Autenticar usuario"""
        email = self.login_email_entry.get().strip()
        password = self.login_password_entry.get().strip()
        
        # Validar que no sean placeholders
        if email == "Ingrese su email" or not email:
            messagebox.showerror("Error", "Por favor ingrese su email")
            return
        
        if password == "Ingrese su contraseña" or not password:
            messagebox.showerror("Error", "Por favor ingrese su contraseña")
            return
        
        try:
            # Consultar usuario
            query = """
                SELECT id, nombre, email, password, rol, activo
                FROM usuarios 
                WHERE email = %s
            """
            
            result = db.execute_query(query, (email,))
            
            if not result:
                messagebox.showerror("Error", "Usuario no encontrado")
                return
            
            user_data = result[0]
            
            # Verificar si está activo
            if not user_data['activo']:
                messagebox.showerror("Error", "Usuario desactivado. Contacte al administrador.")
                return
            
            stored_password = user_data['password']
            password_valid = False
            
            # Verificar contraseña
            if stored_password.startswith('$2b$') or stored_password.startswith('$2a$'):
                try:
                    password_valid = bcrypt.checkpw(
                        password.encode('utf-8'), 
                        stored_password.encode('utf-8')
                    )
                except Exception as e:
                    print(f"Error verificando hash bcrypt: {e}")
                    password_valid = False
            else:
                # Contraseña en texto plano (legacy)
                password_valid = (stored_password == password)
                
                # Migrar a bcrypt
                if password_valid:
                    try:
                        new_hash = bcrypt.hashpw(
                            password.encode('utf-8'), 
                            bcrypt.gensalt()
                        ).decode('utf-8')
                        
                        update_query = "UPDATE usuarios SET password = %s WHERE id = %s"
                        db.execute_update(update_query, (new_hash, user_data['id']))
                        print(f"Contraseña migrada a bcrypt para: {user_data['email']}")
                    except Exception as e:
                        print(f"Error migrando contraseña: {e}")
            
            if password_valid:
                # Guardar preferencia de "recordar sesión" si es necesario
                if self.remember_me.get():
                    self.save_remember_me(email)
                
                messagebox.showinfo("Login Exitoso", f"Bienvenido {user_data['nombre']}")
                self.on_success(user_data)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
                self.login_password_entry.delete(0, tk.END)
                self.login_password_entry.config(show='')
                self.login_password_entry.insert(0, "Ingrese su contraseña")
                self.login_password_entry.config(fg='#adb5bd')
                
        except Exception as e:
            messagebox.showerror("Error", f"Error de autenticación: {str(e)}")
            print(f"Error en login: {e}")
    
    def register_user(self):
        """Registrar nuevo usuario"""
        nombre = self.register_name_entry.get().strip()
        email = self.register_email_entry.get().strip()
        password = self.register_password_entry.get().strip()
        confirm_password = self.register_confirm_password_entry.get().strip()
        
        # Validaciones
        if not nombre or not email or not password or not confirm_password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        if password != confirm_password:
            messagebox.showerror("Error", "Las contraseñas no coinciden")
            return
        
        if '@' not in email:
            messagebox.showerror("Error", "Email inválido")
            return
        
        try:
            # Verificar si el email ya existe
            check_query = "SELECT id FROM usuarios WHERE email = %s"
            existing = db.execute_query(check_query, (email,))
            
            if existing:
                messagebox.showerror("Error", "El email ya está registrado")
                return
            
            # Hashear contraseña
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # Insertar usuario con rol secretario
            insert_query = """
                INSERT INTO usuarios (nombre, email, password, rol, provider, activo)
                VALUES (%s, %s, %s, 'secretario', 'local', 1)
            """
            
            result = db.execute_insert(insert_query, (nombre, email, password_hash))
            
            if result:
                messagebox.showinfo(
                    "Registro Exitoso",
                    f"Usuario {nombre} registrado correctamente.\n\nPuedes iniciar sesión ahora."
                )
                self.switch_tab('login')
                self.login_email_entry.delete(0, tk.END)
                self.login_email_entry.insert(0, email)
                self.login_email_entry.config(fg='#212529')
            else:
                messagebox.showerror("Error", "No se pudo registrar el usuario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error en el registro: {str(e)}")
            print(f"Error en registro: {e}")
    
    def save_remember_me(self, email):
        """Guardar preferencia de recordar sesión (implementación básica)"""
        # Aquí podrías guardar en un archivo local o en la BD
        # Por ahora solo imprime en consola
        print(f"Recordar sesión para: {email}")
        # TODO: Implementar guardado persistente
    
    def forgot_password(self):
        """Funcionalidad de recuperar contraseña (placeholder)"""
        messagebox.showinfo(
            "Recuperar Contraseña",
            "Contacte al administrador del sistema para restablecer su contraseña."
        )