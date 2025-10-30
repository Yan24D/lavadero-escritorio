"""
Panel Principal del Secretario - Refactorizado
Módulo coordinador que gestiona la navegación entre submódulos
"""

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from secretary.register import RegisterModule
from secretary.history import HistoryModule
from secretary.cash import CashModule


class SecretaryPanel:
    """Panel principal para el secretario con navegación lateral"""
    
    def __init__(self, parent, user_data, on_logout_callback):
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout_callback
        self.current_module = None
        self.modules = {}
        
        self.setup_ui()
        self.load_modules()
    
    def setup_ui(self):
        """Configurar interfaz principal"""
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        self.parent.configure(bg='#f8fafc')
        self.parent.geometry("1400x900")
        self.parent.title("Clean Car - Panel Secretario")
        
        # Header
        self.create_header()
        
        # Contenedor principal con sidebar
        main_container = tk.Frame(self.parent, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        # Sidebar izquierdo
        self.create_sidebar(main_container)
        
        # Contenido dinámico
        self.content_frame = tk.Frame(main_container, bg='#f8fafc')
        self.content_frame.pack(side='right', fill='both', expand=True, padx=20, pady=20)

        self.load_modules()
        self.show_module('register')
    
    def create_header(self):
        """Crear header de la aplicación"""
        header_frame = tk.Frame(self.parent, bg='#2563eb', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#2563eb')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Lado izquierdo
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
        
        # Lado derecho
        right_frame = tk.Frame(header_content, bg='#2563eb')
        right_frame.pack(side='right', fill='y')
        
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
        
        user_label = tk.Label(
            right_frame,
            text=f"👤 {self.user_data['nombre']}",
            font=('Segoe UI', 10, 'bold'),
            fg='white',
            bg='#2563eb'
        )
        user_label.pack(side='right', padx=(0, 20))
        
        today = datetime.now()
        date_label = tk.Label(
            right_frame,
            text=f"📅 {today.strftime('%A, %d de %B de %Y')}",
            font=('Segoe UI', 10),
            fg='white',
            bg='#2563eb'
        )
        date_label.pack(side='right', padx=(0, 20))
    
    def create_sidebar(self, parent):
        """Crear sidebar con menú de navegación"""
        sidebar = tk.Frame(parent, bg='#1e293b', width=250)
        sidebar.pack(side='left', fill='y')
        sidebar.pack_propagate(False)
        
        # Logo/Título del panel
        title_frame = tk.Frame(sidebar, bg='#0f172a', height=70)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="📋 Menú",
            font=('Segoe UI', 14, 'bold'),
            fg='white',
            bg='#0f172a'
        )
        title_label.pack(pady=20)
        
        # Botones de navegación
        nav_buttons_frame = tk.Frame(sidebar, bg='#1e293b')
        nav_buttons_frame.pack(fill='both', expand=True, padx=10, pady=20)
        
        btn_style = {
            'font': ('Segoe UI', 11),
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 15,
            'pady': 15,
            'anchor': 'w',
            'justify': 'left'
        }
        
        # Botón Registrar
        self.btn_register = tk.Button(
            nav_buttons_frame,
            text="➕ Registrar Vehículo",
            bg='#2563eb',
            fg='white',
            command=lambda: self.show_module('register'),
            **btn_style
        )
        self.btn_register.pack(fill='x', pady=5)
        
        # Botón Historial
        self.btn_history = tk.Button(
            nav_buttons_frame,
            text="📋 Consultar Historial",
            bg='#64748b',
            fg='white',
            command=lambda: self.show_module('history'),
            **btn_style
        )
        self.btn_history.pack(fill='x', pady=5)
        
        # Botón Cierre de Caja
        self.btn_cash = tk.Button(
            nav_buttons_frame,
            text="💰 Cierre de Caja",
            bg='#64748b',
            fg='white',
            command=lambda: self.show_module('cash'),
            **btn_style
        )
        self.btn_cash.pack(fill='x', pady=5)
        
        # Footer
        footer_frame = tk.Frame(sidebar, bg='#0f172a', height=80)
        footer_frame.pack(fill='x', side='bottom')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Clean Car Sistema\nv1.0 - 2025",
            font=('Segoe UI', 9),
            fg='#94a3b8',
            bg='#0f172a',
            justify='center'
        )
        footer_label.pack(pady=15)
    
    def load_modules(self):
        """Cargar módulos del secretario"""
        try:
            self.modules = {
                'register': RegisterModule(self.user_data),
                'history': HistoryModule(self.user_data),
                'cash': CashModule(self.user_data)
            }
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando módulos: {str(e)}")
    
    def show_module(self, module_name):
        """Mostrar módulo específico"""
        if module_name not in self.modules:
            messagebox.showerror("Error", "Módulo no encontrado")
            return
        
        # Limpiar contenido anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Actualizar botones del sidebar
        self.update_sidebar_buttons(module_name)
        
        # Mostrar módulo
        module = self.modules[module_name]
        module.render(self.content_frame)
        self.current_module = module
    
    def update_sidebar_buttons(self, active_module):
        """Actualizar estilos de botones activos"""
        buttons = {
            'register': self.btn_register,
            'history': self.btn_history,
            'cash': self.btn_cash
        }
        
        for name, btn in buttons.items():
            btn.config(bg='#2563eb' if name == active_module else '#64748b')


def run_secretary_panel(parent, user_data, on_logout):
    """Función para iniciar el panel del secretario"""
    SecretaryPanel(parent, user_data, on_logout)