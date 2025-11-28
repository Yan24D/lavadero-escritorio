"""
Panel Principal de Administrador - Controlador Modular con Scroll
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.db_config import db

# Importar módulos específicos
from .dashboard import DashboardModule
from .usuarios import UsuariosModule
from .servicios import ServiciosModule
from .historial import HistorialModule

class AdminPanel:
    """Panel principal de administrador con arquitectura modular"""
    
    def __init__(self, parent, user_data, on_logout_callback):
        self.parent = parent
        self.user_data = user_data
        self.on_logout = on_logout_callback
        self.current_module = None
        self.active_module_instance = None
        
        self.setup_ui()
        
        # Inicializar módulos
        self.modules = {
            'dashboard': DashboardModule,
            'usuarios': UsuariosModule,
            'servicios': ServiciosModule,
            'historial': HistorialModule
        }
        
        # Cargar dashboard por defecto
        self.switch_module('dashboard')
    
    def setup_ui(self):
        """Configurar interfaz principal"""
        # Limpiar ventana
        for widget in self.parent.winfo_children():
            widget.destroy()
        
        # Configurar ventana
        self.parent.configure(bg='#f8fafc')
        self.parent.geometry("1600x1000")
        self.parent.title("Quili Wash - Panel Administrador")
        
        # Header fijo
        self.create_header()
        
        # Container principal con scroll
        self.create_main_container()
    
    def create_header(self):
        """Crear header de la aplicación"""
        header_frame = tk.Frame(self.parent, bg='#2563eb', height=70)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#2563eb')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Título (lado izquierdo)
        title_label = tk.Label(
            header_content,
            text="Clean Car - Panel Administrador",
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
    
    def create_main_container(self):
        """Crear container principal con scroll"""
        # Frame principal sin scroll
        main_frame = tk.Frame(self.parent, bg='#f8fafc')
        main_frame.pack(fill='both', expand=True, pady=10)
        
        # Sidebar fijo (sin scroll)
        self.create_sidebar(main_frame)
        
        # Área de contenido con scroll
        self.create_scrollable_content_area(main_frame)
    
    def create_sidebar(self, parent):
        """Crear menú lateral con scroll interno"""
        # Container del sidebar
        sidebar_container = tk.Frame(parent, bg='white', width=280, relief='solid', borderwidth=1)
        sidebar_container.pack(side='left', fill='y', padx=(20, 0))
        sidebar_container.pack_propagate(False)
        
        # Canvas y scrollbar para el sidebar
        sidebar_canvas = tk.Canvas(sidebar_container, bg='white', highlightthickness=0)
        sidebar_scrollbar = ttk.Scrollbar(sidebar_container, orient="vertical", command=sidebar_canvas.yview)
        self.sidebar_scrollable_frame = tk.Frame(sidebar_canvas, bg='white')
        
        # Configurar scroll del sidebar
        self.sidebar_scrollable_frame.bind(
            "<Configure>",
            lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all"))
        )
        
        sidebar_canvas.create_window((0, 0), window=self.sidebar_scrollable_frame, anchor="nw")
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        # Pack sidebar canvas
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Scroll con rueda del mouse en sidebar
        def _on_sidebar_mousewheel(event):
            sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        sidebar_canvas.bind("<MouseWheel>", _on_sidebar_mousewheel)
        
        # Crear contenido del sidebar
        self.create_sidebar_content()
    
    def create_sidebar_content(self):
        """Crear contenido del menú lateral"""
        # Título del menú
        menu_title = tk.Label(
            self.sidebar_scrollable_frame,
            text="Panel de Control",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='white'
        )
        menu_title.pack(pady=(20, 30), padx=20)
        
        # Botones del menú
        menu_items = [
            ('dashboard', '📈 Dashboard', 'Estadísticas generales del negocio'),
            ('usuarios', '👥 Gestión de Usuarios', 'Administrar usuarios del sistema'),
            ('servicios', '⚙️ Servicios y Precios', 'Configurar servicios y tarifas'),
            ('historial', '📋 Historial Completo', 'Ver todos los registros')
        ]
        
        self.menu_buttons = {}
        
        for module_id, text, description in menu_items:
            # Frame para el botón
            btn_frame = tk.Frame(self.sidebar_scrollable_frame, bg='white')
            btn_frame.pack(fill='x', padx=10, pady=2)
            
            btn = tk.Button(
                btn_frame,
                text=text,
                font=('Segoe UI', 12, 'bold'),
                bg='#f8fafc',
                fg='#374151',
                relief='flat',
                anchor='w',
                padx=20,
                pady=12,
                cursor='hand2',
                command=lambda mid=module_id: self.switch_module(mid)
            )
            btn.pack(fill='x')

        
        # Separador
        separator = tk.Frame(self.sidebar_scrollable_frame, bg='#e5e7eb', height=3)
        separator.pack(fill='x', padx=20, pady=20)
        
        # Información adicional
        info_frame = tk.Frame(self.sidebar_scrollable_frame, bg='white')
        info_frame.pack(fill='x', padx=20, pady=20)
        
        tk.Label(
            info_frame,
            text="Quili Wash Sistema",
            font=('Segoe UI', 10, 'bold'),
            fg='#6b7280',
            bg='white'
        ).pack()
        
        tk.Label(
            info_frame,
            text="v1.0 - 2025",
            font=('Segoe UI', 9),
            fg='#9ca3af',
            bg='white'
        ).pack()
        
        # Espaciado adicional al final
        tk.Frame(self.sidebar_scrollable_frame, bg='white', height=50).pack()
    
    def create_scrollable_content_area(self, parent):
        """Crear área de contenido con scroll"""
        # Container para el área de contenido
        content_container = tk.Frame(parent, bg='#f8fafc')
        content_container.pack(side='right', fill='both', expand=True, padx=(10, 20))
        
        # Canvas y scrollbar para el contenido
        self.content_canvas = tk.Canvas(content_container, bg='#f8fafc', highlightthickness=0)
        self.content_scrollbar = ttk.Scrollbar(content_container, orient="vertical", command=self.content_canvas.yview)
        self.content_area = tk.Frame(self.content_canvas, bg='#f8fafc')
        
        # Configurar scroll del contenido
        self.content_area.bind(
            "<Configure>",
            lambda e: self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
        )
        
        self.content_canvas.create_window((0, 0), window=self.content_area, anchor="nw")
        self.content_canvas.configure(yscrollcommand=self.content_scrollbar.set)
        
        # Pack content canvas
        self.content_canvas.pack(side="left", fill="both", expand=True)
        self.content_scrollbar.pack(side="right", fill="y")
        
        # Scroll con rueda del mouse en área de contenido
        def _on_content_mousewheel(event):
            self.content_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.content_canvas.bind("<MouseWheel>", _on_content_mousewheel)
        
        # Bind para que el área de contenido se ajuste al ancho del canvas
        def _configure_content_width(event):
            canvas_width = event.width
            self.content_canvas.itemconfig(self.content_canvas.find_all()[0], width=canvas_width-20)
        
        self.content_canvas.bind('<Configure>', _configure_content_width)
    
    def switch_module(self, module_id):
        """Cambiar entre módulos"""
        try:
            # Actualizar botones del menú
            for btn_id, button in self.menu_buttons.items():
                if btn_id == module_id:
                    button.config(bg='#2563eb', fg='white')
                else:
                    button.config(bg='#f8fafc', fg='#374151')
            
            # Limpiar módulo anterior si existe
            if self.active_module_instance:
                self.active_module_instance.cleanup()
            
            # Limpiar área de contenido
            for widget in self.content_area.winfo_children():
                widget.destroy()
            
            # Resetear scroll del contenido al inicio
            self.content_canvas.yview_moveto(0)
            
            # Cargar nuevo módulo
            if module_id in self.modules:
                module_class = self.modules[module_id]
                self.active_module_instance = module_class(
                    self.content_area,
                    self.user_data,
                    db
                )
                self.current_module = module_id
                print(f"✅ Módulo {module_id} cargado exitosamente")
                
                # Actualizar scroll region después de cargar el módulo
                self.parent.after(100, self._update_scroll_region)
            else:
                # Módulo no implementado
                self.show_placeholder(module_id)
            
        except Exception as e:
            print(f"❌ Error cargando módulo {module_id}: {e}")
            messagebox.showerror("Error", f"Error al cargar el módulo {module_id}")
            self.show_error_placeholder(module_id, str(e))
    
    def _update_scroll_region(self):
        """Actualizar región de scroll después de cargar contenido"""
        self.content_canvas.configure(scrollregion=self.content_canvas.bbox("all"))
    
    def show_placeholder(self, module_id):
        """Mostrar placeholder para módulos no implementados"""
        placeholder_frame = tk.Frame(self.content_area, bg='#f8fafc')
        placeholder_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(
            placeholder_frame,
            text=f"📋 Módulo {module_id.title()}",
            font=('Segoe UI', 24, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=(50, 20))
        
        tk.Label(
            placeholder_frame,
            text="En desarrollo...",
            font=('Segoe UI', 16),
            fg='#6b7280',
            bg='#f8fafc'
        ).pack()
        
        # Espaciado adicional para hacer scroll visible
        tk.Frame(placeholder_frame, bg='#f8fafc', height=300).pack()
    
    def show_error_placeholder(self, module_id, error_msg):
        """Mostrar placeholder de error"""
        error_frame = tk.Frame(self.content_area, bg='#f8fafc')
        error_frame.pack(fill='both', expand=True, pady=50)
        
        tk.Label(
            error_frame,
            text=f"❌ Error en módulo {module_id.title()}",
            font=('Segoe UI', 20, 'bold'),
            fg='#dc2626',
            bg='#f8fafc'
        ).pack(pady=(50, 20))
        
        tk.Label(
            error_frame,
            text=error_msg,
            font=('Segoe UI', 12),
            fg='#6b7280',
            bg='#f8fafc'
        ).pack()
        
        # Espaciado adicional
        tk.Frame(error_frame, bg='#f8fafc', height=300).pack()
    
    def get_current_module(self):
        """Obtener módulo actual activo"""
        return self.active_module_instance
    
    def refresh_current_module(self):
        """Refrescar módulo actual"""
        if self.current_module:
            self.switch_module(self.current_module)