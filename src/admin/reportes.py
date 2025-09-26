import tkinter as tk

class AdminReportes:
    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
    
    def show(self):
        # Placeholder - implementar después
        tk.Label(
            self.parent,
            text="📊 Módulo de Reportes Financieros",
            font=('Segoe UI', 20, 'bold'),
            bg='#f8fafc'
        ).pack(expand=True)