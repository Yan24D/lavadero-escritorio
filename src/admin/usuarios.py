from .base_module import BaseModule
import tkinter as tk

class UsuariosModule(BaseModule):
    def setup_module(self):
        tk.Label(
            self.parent,
            text="👥 Gestión de Usuarios",
            font=('Segoe UI', 24, 'bold'),
            bg='#f8fafc'
        ).pack(expand=True)
        
        tk.Label(
            self.parent,
            text="En desarrollo...",
            font=('Segoe UI', 14),
            fg='#6b7280',
            bg='#f8fafc'
        ).pack()