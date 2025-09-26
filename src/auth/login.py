"""
Sistema de Login y Autenticación - Versión Corregida
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
from database.db_config import db

class LoginWindow:
    """Ventana de inicio de sesión"""
    
    def __init__(self, parent, on_success_callback):
        self.parent = parent
        self.on_success = on_success_callback
        self.setup_ui()
    
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        # Limpiar ventana
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Configurar ventana principal
        self.parent.configure(bg='#3498db')
        self.parent.geometry("450x500")
        self.parent.resizable(True, True)
        
        # Frame principal
        main_frame = tk.Frame(self.parent, bg='#3498db')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="🚗 SISTEMA LAVADERO", 
            font=('Arial', 18, 'bold'),
            fg='white',
            bg='#3498db'
        )
        title_label.pack(pady=(30, 10))
        
        # Subtítulo
        subtitle_label = tk.Label(
            main_frame,
            text="Iniciar Sesión",
            font=('Arial', 14),
            fg='#ecf0f1',
            bg='#3498db'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame del formulario
        form_frame = tk.Frame(main_frame, bg='white', relief='raised', borderwidth=2)
        form_frame.pack(pady=20, padx=20, fill='x')
        
        # Espaciado interno
        inner_frame = tk.Frame(form_frame, bg='white')
        inner_frame.pack(padx=30, pady=30, fill='both', expand=True)
        
        # Campo Usuario
        user_label = tk.Label(
            inner_frame, 
            text="Correo:", 
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        user_label.pack(anchor='w', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            inner_frame, 
            font=('Arial', 12),
            width=30,
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.username_entry.pack(fill='x', pady=(0, 20), ipady=10)
        
        # Campo Contraseña
        pass_label = tk.Label(
            inner_frame, 
            text="Contraseña:", 
            font=('Arial', 12, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        pass_label.pack(anchor='w', pady=(0, 5))
        
        self.password_entry = tk.Entry(
            inner_frame, 
            font=('Arial', 12),
            width=30,
            show='*',
            relief='solid',
            borderwidth=1,
            bg='#f8f9fa'
        )
        self.password_entry.pack(fill='x', pady=(0, 25), ipady=10)
        
        # Botón Login
        login_button = tk.Button(
            inner_frame,
            text="Iniciar Sesión",
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.authenticate
        )
        login_button.pack(fill='x', pady=(0, 20), ipady=12)
        
        # Información de credenciales
        info_frame = tk.Frame(inner_frame, bg='#ecf0f1', relief='solid', borderwidth=1)
        info_frame.pack(fill='x', pady=(10, 0))
        
        info_title = tk.Label(
            info_frame,
            text="🔑 Credenciales por defecto:",
            font=('Arial', 10, 'bold'),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        info_title.pack(pady=(10, 5))
        
        info_creds = tk.Label(
            info_frame,
            text="Usuario: admin | Contraseña: 123456",
            font=('Arial', 9),
            bg='#ecf0f1',
            fg='#7f8c8d'
        )
        info_creds.pack(pady=(0, 10))
        
        # Eventos de teclado
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.authenticate())
        
        # Establecer foco inicial
        self.username_entry.focus_set()
        
        # Mostrar ventana
        self.parent.deiconify()
    
    def authenticate(self):
        """Autenticar usuario"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validar campos vacíos
        if not username or not password:
            messagebox.showerror("Error", "Por favor completa todos los campos")
            return
        
        try:
            # Consultar usuario en base de datos
            query = """
                SELECT id, nombre, email, password, rol 
                FROM usuarios 
                WHERE email = %s
            """
            
            result = db.execute_query(query, (username,))
            
            if not result:
                messagebox.showerror("Error", "Usuario no encontrado")
                self.clear_fields()
                return
            
            user_data = result[0]
            
            # Verificar contraseña (por ahora sin hash)
            if user_data['password'] == password:
                messagebox.showinfo(
                    "Login Exitoso", 
                    f"¡Bienvenido {user_data['nombre']}!"
                )
                
                # Llamar callback de éxito
                self.on_success(user_data)
            else:
                messagebox.showerror("Error", "Contraseña incorrecta")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus_set()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error de autenticación: {str(e)}")
            print(f"❌ Error en login: {e}")
    
    def clear_fields(self):
        """Limpiar campos del formulario"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.username_entry.focus_set()
    
    def hash_password(self, password):
        """Generar hash de contraseña (para uso futuro)"""
        return hashlib.sha256(password.encode()).hexdigest()