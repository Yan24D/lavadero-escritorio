# Reemplazar TODO el contenido de base_module.py con:
"""
Clase base para todos los módulos del panel de secretario
"""

import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk


class BaseModule(ABC):
    """Clase base abstracta para módulos del secretario"""
    
    def __init__(self, user_data):
        self.user_data = user_data
        self.parent_frame = None
    
    @abstractmethod
    def render(self, parent):
        """Renderizar el módulo"""
        pass
    
    @abstractmethod
    def load_data(self):
        """Cargar datos"""
        pass
    
    @abstractmethod
    def refresh(self):
        """Refrescar datos"""
        pass
    
    def clear_parent(self, parent):
        """Limpiar widgets del parent"""
        for widget in parent.winfo_children():
            widget.destroy()
    
    def create_section_header(self, parent, title, icon=""):
        """Crear encabezado de sección"""
        header = tk.Label(
            parent, text=f"{icon} {title}",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b', bg='#f8fafc'
        )
        return header
    
    def create_button(self, parent, text, command, bg_color='#2563eb', **kwargs):
        """Crear botón estándar"""
        btn = tk.Button(
            parent, text=text, command=command,
            font=('Segoe UI', 10, 'bold'),
            bg=bg_color, fg='white', relief='flat',
            padx=20, pady=10, cursor='hand2', **kwargs
        )
        return btn
    
    def create_input_field(self, parent, label_text, **kwargs):
        """Crear campo de entrada"""
        tk.Label(
            parent, text=label_text,
            font=('Segoe UI', 10, 'bold'),
            bg=parent.cget('bg'), fg='#374151'
        ).pack(anchor='w')
        
        entry = tk.Entry(
            parent, font=('Segoe UI', 10),
            relief='solid', borderwidth=1,
            bg='#f9fafb', **kwargs
        )
        entry.pack(fill='x', pady=(5, 15), ipady=8)
        return entry
    
    def format_currency(self, value):
        """Formatear como moneda"""
        try:
            return f"${float(value):,.0f}"
        except (ValueError, TypeError):
            return "$0"
    
    def format_time(self, time_obj):
        """Formatear hora"""
        if time_obj:
            return str(time_obj)[:5]
        return ""