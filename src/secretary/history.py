"""
Módulo de Consulta de Historial para Secretario
Permite consultar el historial de servicios registrados
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.db_config import db
from secretary.base_module import BaseModule


class HistoryModule(BaseModule):
    """Módulo para consultar historial de servicios"""
    
    def __init__(self, user_data):
        super().__init__(user_data)
        self.history_tree = None
    
    def render(self, parent):
        """Renderizar módulo de historial"""
        self.parent_frame = parent
        self.clear_parent(parent)
        
        main_container = tk.Frame(parent, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        # Título
        header = self.create_section_header(
            main_container, "Consultar Historial", "📋"
        )
        header.pack(anchor='w', pady=(0, 20))
        
        # Filtros
        self.create_filters(main_container)
        
        # Tabla de resultados
        self.create_history_table(main_container)
        
        # Cargar datos iniciales
        self.load_data()
    
    def create_filters(self, parent):
        """Crear panel de filtros"""
        filters_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        filters_frame.pack(fill='x', pady=(0, 20))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=15)
        
        filters_row = tk.Frame(filters_content, bg='white')
        filters_row.pack(fill='x')
        
        # Filtro por fecha
        date_frame = tk.Frame(filters_row, bg='white')
        date_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.filter_date = self.create_input_field(date_frame, "Fecha:")
        self.filter_date.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Filtro por placa
        plate_frame = tk.Frame(filters_row, bg='white')
        plate_frame.pack(side='left', fill='x', expand=True, padx=10)
        self.filter_plate = self.create_input_field(plate_frame, "Placa:")
        
        # Filtro por lavador
        washer_frame = tk.Frame(filters_row, bg='white')
        washer_frame.pack(side='left', fill='x', expand=True, padx=10)
        self.filter_washer = self.create_input_field(washer_frame, "Lavador:")
        
        # Botón buscar
        search_btn_frame = tk.Frame(filters_row, bg='white')
        search_btn_frame.pack(side='right', padx=(10, 0))
        tk.Label(search_btn_frame, text="", bg='white').pack()
        
        search_btn = self.create_button(
            search_btn_frame, "🔍 Buscar",
            self.search_history, bg_color='#2563eb'
        )
        search_btn.pack(pady=(5, 0))
    
    def create_history_table(self, parent):
        """Crear tabla de historial"""
        table_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        table_frame.pack(fill='both', expand=True)
        
        table_title_frame = tk.Frame(table_frame, bg='#f8fafc', height=50)
        table_title_frame.pack(fill='x')
        table_title_frame.pack_propagate(False)
        
        table_title = tk.Label(
            table_title_frame,
            text="📊 Resultados de la Búsqueda",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        table_title.pack(side='left', padx=20, pady=15)
        
        columns = ('ID', 'Fecha', 'Hora', 'Vehículo', 'Placa', 
                   'Servicio', 'Costo', 'Lavador', 'Estado')
        
        self.history_tree = ttk.Treeview(
            table_frame, columns=columns, show='headings', height=15
        )
        
        # Configurar encabezados
        self.history_tree.heading('ID', text='ID')
        self.history_tree.heading('Fecha', text='Fecha')
        self.history_tree.heading('Hora', text='Hora')
        self.history_tree.heading('Vehículo', text='Vehículo')
        self.history_tree.heading('Placa', text='Placa')
        self.history_tree.heading('Servicio', text='Servicio')
        self.history_tree.heading('Costo', text='Costo')
        self.history_tree.heading('Lavador', text='Lavador')
        self.history_tree.heading('Estado', text='Estado')
        
        # Configurar ancho de columnas
        self.history_tree.column('ID', width=50, anchor='center')
        self.history_tree.column('Fecha', width=100, anchor='center')
        self.history_tree.column('Hora', width=80, anchor='center')
        self.history_tree.column('Vehículo', width=100, anchor='center')
        self.history_tree.column('Placa', width=100, anchor='center')
        self.history_tree.column('Servicio', width=150)
        self.history_tree.column('Costo', width=100, anchor='center')
        self.history_tree.column('Lavador', width=120)
        self.history_tree.column('Estado', width=100, anchor='center')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame, orient='vertical', command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        
        # Empaquetar tabla y scrollbar
        self.history_tree.pack(
            side='left', fill='both', expand=True, padx=20, pady=20
        )
        scrollbar.pack(side='right', fill='y', pady=20, padx=(0, 20))
    
    def load_data(self):
        """Cargar datos iniciales"""
        self.search_history()
    
    def refresh(self):
        """Refrescar datos"""
        self.search_history()
    
    def search_history(self):
        """Buscar en el historial con filtros"""
        try:
            # Limpiar tabla
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Consulta base
            base_query = """
                SELECT id, fecha, hora, vehiculo_nombre, placa, 
                       servicio_nombre, costo, lavador, pago
                FROM vista_registros_completos
                WHERE 1=1
            """
            
            params = []
            
            # Aplicar filtro por fecha
            if self.filter_date.get().strip():
                base_query += " AND fecha = %s"
                params.append(self.filter_date.get().strip())
            
            # Aplicar filtro por placa
            if self.filter_plate.get().strip():
                base_query += " AND placa LIKE %s"
                params.append(f"%{self.filter_plate.get().strip()}%")
            
            # Aplicar filtro por lavador
            if self.filter_washer.get().strip():
                base_query += " AND lavador LIKE %s"
                params.append(f"%{self.filter_washer.get().strip()}%")
            
            # Ordenar y limitar resultados
            base_query += " ORDER BY fecha DESC, hora DESC LIMIT 100"
            
            # Ejecutar consulta
            results = db.execute_query(base_query, params if params else None)
            
            if results:
                for row in results:
                    # Formatear datos
                    fecha = row['fecha'].strftime('%Y-%m-%d') if row['fecha'] else ''
                    hora = str(row['hora']) if row['hora'] else ''
                    costo = f"${row['costo']:,.0f}" if row['costo'] else '$0'
                    placa = row['placa'] or 'N/A'
                    lavador = row['lavador'] or 'N/A'
                    
                    # Insertar fila en tabla
                    self.history_tree.insert('', 'end', values=(
                        row['id'],
                        fecha,
                        hora,
                        row['vehiculo_nombre'],
                        placa,
                        row['servicio_nombre'],
                        costo,
                        lavador,
                        row['pago']
                    ))
            else:
                # Mostrar mensaje cuando no hay resultados
                self.history_tree.insert('', 'end', values=(
                    '', '', '', 'No se encontraron resultados',
                    '', '', '', '', ''
                ))
                
        except Exception as e:
            print(f"Error buscando historial: {e}")
            messagebox.showerror("Error", "Error al buscar en el historial")