"""
Dashboard Principal - Módulo de Estadísticas y KPIs
"""

import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import calendar
from .base_module import BaseModule

class DashboardModule(BaseModule):
    """Dashboard principal con métricas del negocio"""
    
    def setup_module(self):
        """Configurar dashboard principal"""
        # Datos generales
        self.today = datetime.now()
        self.current_month = self.today.month
        self.current_year = self.today.year
        
        # Crear interfaz
        self.create_header()
        self.create_main_content()
        
        # Cargar datos
        self.load_dashboard_data()
    
    def create_header(self):
        """Crear header del dashboard"""
        header_frame = tk.Frame(self.parent, bg='#f8fafc')
        header_frame.pack(fill='x', pady=(0, 30))
        
        # Título principal
        title_label = tk.Label(
            header_frame,
            text="📈 Dashboard - Panel de Control",
            font=('Segoe UI', 24, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(side='left')
        
        # Selector de período
        period_frame = tk.Frame(header_frame, bg='#f8fafc')
        period_frame.pack(side='right')
        
        tk.Label(
            period_frame,
            text="Período:",
            font=('Segoe UI', 12, 'bold'),
            bg='#f8fafc',
            fg='#374151'
        ).pack(side='left', padx=(0, 10))
        
        # Combobox para seleccionar mes
        months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        self.month_var = tk.StringVar(value=months[self.current_month - 1])
        month_combo = ttk.Combobox(
            period_frame,
            textvariable=self.month_var,
            values=months,
            state='readonly',
            width=12
        )
        month_combo.pack(side='left', padx=(0, 10))
        month_combo.bind('<<ComboboxSelected>>', self.on_period_change)
        
        # Combobox para año
        current_year = self.today.year
        years = [str(year) for year in range(current_year - 2, current_year + 1)]
        
        self.year_var = tk.StringVar(value=str(self.current_year))
        year_combo = ttk.Combobox(
            period_frame,
            textvariable=self.year_var,
            values=years,
            state='readonly',
            width=8
        )
        year_combo.pack(side='left', padx=(0, 10))
        year_combo.bind('<<ComboboxSelected>>', self.on_period_change)
        
        # Botón refrescar
        refresh_btn = tk.Button(
            period_frame,
            text="🔄 Actualizar",
            font=('Segoe UI', 10, 'bold'),
            bg='#2563eb',
            fg='white',
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.load_dashboard_data
        )
        refresh_btn.pack(side='left')
    
    def create_main_content(self):
        """Crear contenido principal del dashboard"""
        # Container principal
        main_container = tk.Frame(self.parent, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        # KPIs principales (fila superior)
        self.create_kpis_section(main_container)
        
        # Gráficos y estadísticas (fila media)
        self.create_charts_section(main_container)
        
        # Tablas de resumen (fila inferior)
        self.create_tables_section(main_container)
    
    def create_kpis_section(self, parent):
        """Crear sección de KPIs principales"""
        kpis_frame = tk.Frame(parent, bg='#f8fafc')
        kpis_frame.pack(fill='x', pady=(0, 30))
        
        # Título de sección
        tk.Label(
            kpis_frame,
            text="📊 Indicadores Principales",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=(0, 20))
        
        # Grid de KPIs
        kpis_grid = tk.Frame(kpis_frame, bg='#f8fafc')
        kpis_grid.pack(fill='x')
        
        # Crear cards de KPIs (se llenarán con datos)
        self.kpi_cards = {}
        kpi_configs = [
            ("total_ingresos", "💰 Ingresos Totales", "#059669"),
            ("total_servicios", "🚗 Servicios Realizados", "#2563eb"),
            ("promedio_servicio", "📊 Promedio por Servicio", "#7c3aed"),
            ("total_comisiones", "💳 Comisiones Pagadas", "#dc2626"),
            ("ganancia_neta", "💎 Ganancia Neta", "#059669"),
            ("servicios_hoy", "⚡ Servicios Hoy", "#d97706")
        ]
        
        for i, (key, title, color) in enumerate(kpi_configs):
            # Calcular posición en grid (2 columnas por fila)
            row = i // 3
            col = i % 3
            
            card_frame = tk.Frame(kpis_grid, bg=color, relief='solid', borderwidth=1)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='ew')
            
            # Configurar columnas del grid
            if col == 0:  # Solo configurar una vez por fila
                kpis_grid.grid_columnconfigure(0, weight=1)
                kpis_grid.grid_columnconfigure(1, weight=1)
                kpis_grid.grid_columnconfigure(2, weight=1)
            
            # Contenido del card
            card_content = tk.Frame(card_frame, bg=color)
            card_content.pack(fill='both', expand=True, padx=20, pady=20)
            
            # Título
            title_label = tk.Label(
                card_content,
                text=title,
                font=('Segoe UI', 11, 'bold'),
                fg='white',
                bg=color
            )
            title_label.pack()
            
            # Valor (se actualizará con datos)
            value_label = tk.Label(
                card_content,
                text="Cargando...",
                font=('Segoe UI', 18, 'bold'),
                fg='white',
                bg=color
            )
            value_label.pack(pady=(8, 0))
            
            self.kpi_cards[key] = value_label
    
    def create_charts_section(self, parent):
        """Crear sección de gráficos"""
        charts_frame = tk.Frame(parent, bg='#f8fafc')
        charts_frame.pack(fill='x', pady=(0, 30))
        
        # Título de sección
        tk.Label(
            charts_frame,
            text="📈 Análisis y Tendencias",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=(0, 20))
        
        # Grid para gráficos
        charts_grid = tk.Frame(charts_frame, bg='#f8fafc')
        charts_grid.pack(fill='x')
        charts_grid.grid_columnconfigure(0, weight=1)
        charts_grid.grid_columnconfigure(1, weight=1)
        
        # Gráfico de ingresos diarios
        self.create_daily_chart(charts_grid)
        
        # Gráfico de servicios por tipo
        self.create_services_chart(charts_grid)
    
    def create_daily_chart(self, parent):
        """Crear gráfico de ingresos diarios"""
        chart_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        chart_frame.grid(row=0, column=0, padx=(0, 15), pady=10, sticky='nsew')
        
        # Header del gráfico
        chart_header = tk.Frame(chart_frame, bg='#f8fafc')
        chart_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            chart_header,
            text="📊 Ingresos Diarios del Mes",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=15)
        
        # Área del gráfico (simulado con barras texto)
        self.daily_chart_area = tk.Frame(chart_frame, bg='white')
        self.daily_chart_area.pack(fill='both', expand=True, padx=20, pady=20)
    
    def create_services_chart(self, parent):
        """Crear gráfico de servicios por tipo"""
        chart_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        chart_frame.grid(row=0, column=1, padx=(15, 0), pady=10, sticky='nsew')
        
        # Header del gráfico
        chart_header = tk.Frame(chart_frame, bg='#f8fafc')
        chart_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            chart_header,
            text="🥧 Servicios por Tipo de Vehículo",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=15)
        
        # Área del gráfico
        self.services_chart_area = tk.Frame(chart_frame, bg='white')
        self.services_chart_area.pack(fill='both', expand=True, padx=20, pady=20)
    
    def create_tables_section(self, parent):
        """Crear sección de tablas resumen"""
        tables_frame = tk.Frame(parent, bg='#f8fafc')
        tables_frame.pack(fill='both', expand=True)
        
        # Título de sección
        tk.Label(
            tables_frame,
            text="📋 Resúmenes Detallados",
            font=('Segoe UI', 16, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=(0, 20))
        
        # Grid para tablas
        tables_grid = tk.Frame(tables_frame, bg='#f8fafc')
        tables_grid.pack(fill='both', expand=True)
        tables_grid.grid_columnconfigure(0, weight=1)
        tables_grid.grid_columnconfigure(1, weight=1)
        
        # Tabla de lavadores
        self.create_workers_table(tables_grid)
        
        # Tabla de servicios recientes
        self.create_recent_services_table(tables_grid)
    
    def create_workers_table(self, parent):
        """Crear tabla de rendimiento de lavadores"""
        table_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        table_frame.grid(row=0, column=0, padx=(0, 15), pady=10, sticky='nsew')
        
        # Header de la tabla
        table_header = tk.Frame(table_frame, bg='#f8fafc')
        table_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            table_header,
            text="👥 Rendimiento de Lavadores",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=15)
        
        # Treeview para lavadores
        columns = ('Lavador', 'Servicios', 'Ingresos', 'Comisión')
        
        self.workers_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        self.workers_tree.heading('Lavador', text='Lavador')
        self.workers_tree.heading('Servicios', text='Servicios')
        self.workers_tree.heading('Ingresos', text='Ingresos')
        self.workers_tree.heading('Comisión', text='Comisión')
        
        # Ancho de columnas
        self.workers_tree.column('Lavador', width=120)
        self.workers_tree.column('Servicios', width=80, anchor='center')
        self.workers_tree.column('Ingresos', width=100, anchor='center')
        self.workers_tree.column('Comisión', width=100, anchor='center')
        
        # Scrollbar para la tabla
        workers_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.workers_tree.yview)
        self.workers_tree.configure(yscrollcommand=workers_scrollbar.set)
        
        # Pack
        self.workers_tree.pack(side='left', fill='both', expand=True, padx=20, pady=(0, 20))
        workers_scrollbar.pack(side='right', fill='y', pady=(0, 20), padx=(0, 20))
    
    def create_recent_services_table(self, parent):
        """Crear tabla de servicios recientes"""
        table_frame = tk.Frame(parent, bg='white', relief='solid', borderwidth=1)
        table_frame.grid(row=0, column=1, padx=(15, 0), pady=10, sticky='nsew')
        
        # Header de la tabla
        table_header = tk.Frame(table_frame, bg='#f8fafc')
        table_header.pack(fill='x', padx=1, pady=1)
        
        tk.Label(
            table_header,
            text="🕒 Servicios Recientes",
            font=('Segoe UI', 14, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        ).pack(pady=15)
        
        # Treeview para servicios recientes
        columns = ('Fecha', 'Vehículo', 'Servicio', 'Costo')
        
        self.recent_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=8)
        
        # Configurar columnas
        self.recent_tree.heading('Fecha', text='Fecha')
        self.recent_tree.heading('Vehículo', text='Vehículo')
        self.recent_tree.heading('Servicio', text='Servicio')
        self.recent_tree.heading('Costo', text='Costo')
        
        # Ancho de columnas
        self.recent_tree.column('Fecha', width=80, anchor='center')
        self.recent_tree.column('Vehículo', width=80, anchor='center')
        self.recent_tree.column('Servicio', width=120)
        self.recent_tree.column('Costo', width=80, anchor='center')
        
        # Scrollbar
        recent_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.recent_tree.yview)
        self.recent_tree.configure(yscrollcommand=recent_scrollbar.set)
        
        # Pack
        self.recent_tree.pack(side='left', fill='both', expand=True, padx=20, pady=(0, 20))
        recent_scrollbar.pack(side='right', fill='y', pady=(0, 20), padx=(0, 20))
    
    def on_period_change(self, event=None):
        """Cuando cambia el período seleccionado"""
        # Obtener mes y año seleccionados
        months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        
        month_name = self.month_var.get()
        self.current_month = months.index(month_name) + 1
        self.current_year = int(self.year_var.get())
        
        # Recargar datos
        self.load_dashboard_data()
    
    def load_dashboard_data(self):
        """Cargar todos los datos del dashboard"""
        try:
            # Calcular fechas del período
            start_date = f"{self.current_year}-{self.current_month:02d}-01"
            
            # Último día del mes
            last_day = calendar.monthrange(self.current_year, self.current_month)[1]
            end_date = f"{self.current_year}-{self.current_month:02d}-{last_day}"
            
            # Cargar KPIs
            self.load_kpis(start_date, end_date)
            
            # Cargar gráficos
            self.load_daily_chart(start_date, end_date)
            self.load_services_chart(start_date, end_date)
            
            # Cargar tablas
            self.load_workers_table(start_date, end_date)
            self.load_recent_services()
            
        except Exception as e:
            print(f"Error cargando datos del dashboard: {e}")
            # Mostrar datos por defecto en caso de error
            self.load_default_data()
    
    def load_kpis(self, start_date, end_date):
        """Cargar KPIs principales"""
        try:
            # Query para KPIs del período
            kpi_query = """
                SELECT 
                    COALESCE(SUM(costo), 0) as total_ingresos,
                    COUNT(*) as total_servicios,
                    COALESCE(AVG(costo), 0) as promedio_servicio,
                    COALESCE(SUM(comision_calculada), 0) as total_comisiones,
                    COALESCE(SUM(ganancia_neta), 0) as ganancia_neta
                FROM vista_registros_completos 
                WHERE fecha BETWEEN %s AND %s
                AND pago = 'Pagado'
            """
            
            kpi_result = self.db.execute_query(kpi_query, (start_date, end_date))
            
            # Query para servicios de hoy
            today_query = """
                SELECT COUNT(*) as servicios_hoy
                FROM vista_registros_completos 
                WHERE fecha = CURDATE()
                AND pago = 'Pagado'
            """
            
            today_result = self.db.execute_query(today_query)
            
            if kpi_result:
                data = kpi_result[0]
                servicios_hoy = today_result[0]['servicios_hoy'] if today_result else 0
                
                # Actualizar KPIs
                self.kpi_cards['total_ingresos'].config(text=f"${data['total_ingresos']:,.0f}")
                self.kpi_cards['total_servicios'].config(text=f"{data['total_servicios']:,}")
                self.kpi_cards['promedio_servicio'].config(text=f"${data['promedio_servicio']:,.0f}")
                self.kpi_cards['total_comisiones'].config(text=f"${data['total_comisiones']:,.0f}")
                self.kpi_cards['ganancia_neta'].config(text=f"${data['ganancia_neta']:,.0f}")
                self.kpi_cards['servicios_hoy'].config(text=f"{servicios_hoy}")
            
        except Exception as e:
            print(f"Error cargando KPIs: {e}")
            # Datos por defecto en caso de error
            for key in self.kpi_cards:
                self.kpi_cards[key].config(text="N/A")
    
    def load_daily_chart(self, start_date, end_date):
        """Cargar gráfico de ingresos diarios"""
        try:
            # Limpiar área del gráfico
            for widget in self.daily_chart_area.winfo_children():
                widget.destroy()
            
            # Query para ingresos diarios
            daily_query = """
                SELECT 
                    DATE(fecha) as dia,
                    COALESCE(SUM(costo), 0) as ingresos_dia
                FROM vista_registros_completos 
                WHERE fecha BETWEEN %s AND %s
                AND pago = 'Pagado'
                GROUP BY DATE(fecha)
                ORDER BY dia DESC
                LIMIT 15
            """
            
            daily_result = self.db.execute_query(daily_query, (start_date, end_date))
            
            if daily_result:
                # Crear gráfico de barras simple
                max_ingreso = max([row['ingresos_dia'] for row in daily_result]) if daily_result else 1
                
                for i, row in enumerate(daily_result[:10]):  # Mostrar últimos 10 días
                    # Frame para cada barra
                    bar_frame = tk.Frame(self.daily_chart_area, bg='white')
                    bar_frame.pack(fill='x', pady=2)
                    
                    # Fecha
                    date_str = row['dia'].strftime('%d/%m') if hasattr(row['dia'], 'strftime') else str(row['dia'])
                    tk.Label(
                        bar_frame,
                        text=date_str,
                        font=('Segoe UI', 9),
                        bg='white',
                        width=8
                    ).pack(side='left')
                    
                    # Barra visual
                    bar_width = int((row['ingresos_dia'] / max_ingreso) * 200) if max_ingreso > 0 else 0
                    bar_color = '#059669' if row['ingresos_dia'] > 0 else '#e5e7eb'
                    
                    bar_canvas = tk.Canvas(bar_frame, height=20, bg='white', highlightthickness=0)
                    bar_canvas.pack(side='left', fill='x', expand=True, padx=(10, 0))
                    
                    if bar_width > 0:
                        bar_canvas.create_rectangle(0, 5, bar_width, 15, fill=bar_color, outline=bar_color)
                    
                    # Valor
                    tk.Label(
                        bar_frame,
                        text=f"${row['ingresos_dia']:,.0f}",
                        font=('Segoe UI', 9, 'bold'),
                        bg='white',
                        fg='#374151'
                    ).pack(side='right', padx=(10, 0))
            else:
                tk.Label(
                    self.daily_chart_area,
                    text="No hay datos para mostrar",
                    font=('Segoe UI', 12),
                    fg='#6b7280',
                    bg='white'
                ).pack(expand=True)
                
        except Exception as e:
            print(f"Error cargando gráfico diario: {e}")
    
    def load_services_chart(self, start_date, end_date):
        """Cargar gráfico de servicios por tipo"""
        try:
            # Limpiar área del gráfico
            for widget in self.services_chart_area.winfo_children():
                widget.destroy()
            
            # Query para servicios por tipo de vehículo
            services_query = """
                SELECT 
                    vehiculo_nombre,
                    COUNT(*) as cantidad,
                    COALESCE(SUM(costo), 0) as ingresos_tipo
                FROM vista_registros_completos 
                WHERE fecha BETWEEN %s AND %s
                AND pago = 'Pagado'
                GROUP BY vehiculo_nombre
                ORDER BY cantidad DESC
            """
            
            services_result = self.db.execute_query(services_query, (start_date, end_date))
            
            if services_result:
                total_servicios = sum([row['cantidad'] for row in services_result])
                colors = ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed']
                
                for i, row in enumerate(services_result):
                    # Frame para cada tipo
                    item_frame = tk.Frame(self.services_chart_area, bg='white')
                    item_frame.pack(fill='x', pady=5)
                    
                    # Color indicator
                    color = colors[i % len(colors)]
                    color_label = tk.Label(
                        item_frame,
                        text="●",
                        font=('Segoe UI', 16),
                        fg=color,
                        bg='white'
                    )
                    color_label.pack(side='left', padx=(0, 10))
                    
                    # Nombre del vehículo
                    tk.Label(
                        item_frame,
                        text=row['vehiculo_nombre'],
                        font=('Segoe UI', 11, 'bold'),
                        bg='white',
                        fg='#374151'
                    ).pack(side='left')
                    
                    # Porcentaje y cantidad
                    percentage = (row['cantidad'] / total_servicios) * 100 if total_servicios > 0 else 0
                    info_text = f"{percentage:.1f}% ({row['cantidad']} servicios)"
                    
                    tk.Label(
                        item_frame,
                        text=info_text,
                        font=('Segoe UI', 10),
                        bg='white',
                        fg='#6b7280'
                    ).pack(side='right')
            else:
                tk.Label(
                    self.services_chart_area,
                    text="No hay datos para mostrar",
                    font=('Segoe UI', 12),
                    fg='#6b7280',
                    bg='white'
                ).pack(expand=True)
                
        except Exception as e:
            print(f"Error cargando gráfico de servicios: {e}")
    
    def load_workers_table(self, start_date, end_date):
        """Cargar tabla de rendimiento de lavadores"""
        try:
            # Limpiar tabla
            for item in self.workers_tree.get_children():
                self.workers_tree.delete(item)
            
            # Query para rendimiento de lavadores
            workers_query = """
                SELECT 
                    lavador,
                    COUNT(*) as total_servicios,
                    COALESCE(SUM(costo), 0) as total_ingresos,
                    COALESCE(SUM(comision_calculada), 0) as total_comision
                FROM vista_registros_completos 
                WHERE fecha BETWEEN %s AND %s
                AND pago = 'Pagado'
                GROUP BY lavador
                ORDER BY total_ingresos DESC
            """
            
            workers_result = self.db.execute_query(workers_query, (start_date, end_date))
            
            if workers_result:
                for row in workers_result:
                    self.workers_tree.insert('', 'end', values=(
                        row['lavador'],
                        f"{row['total_servicios']}",
                        f"${row['total_ingresos']:,.0f}",
                        f"${row['total_comision']:,.0f}"
                    ))
                    
        except Exception as e:
            print(f"Error cargando tabla de lavadores: {e}")
    
    def load_recent_services(self):
        """Cargar servicios recientes"""
        try:
            # Limpiar tabla
            for item in self.recent_tree.get_children():
                self.recent_tree.delete(item)
            
            # Query para servicios recientes
            recent_query = """
                SELECT 
                    fecha,
                    vehiculo_nombre,
                    servicio_nombre,
                    costo
                FROM vista_registros_completos 
                WHERE pago = 'Pagado'
                ORDER BY fecha DESC, hora DESC
                LIMIT 15
            """
            
            recent_result = self.db.execute_query(recent_query)
            
            if recent_result:
                for row in recent_result:
                    fecha_str = row['fecha'].strftime('%d/%m') if hasattr(row['fecha'], 'strftime') else str(row['fecha'])
                    
                    self.recent_tree.insert('', 'end', values=(
                        fecha_str,
                        row['vehiculo_nombre'],
                        row['servicio_nombre'][:15] + "..." if len(row['servicio_nombre']) > 15 else row['servicio_nombre'],
                        f"${row['costo']:,.0f}"
                    ))
                    
        except Exception as e:
            print(f"Error cargando servicios recientes: {e}")
    
    def load_default_data(self):
        """Cargar datos por defecto en caso de error"""
        # KPIs por defecto
        for key in self.kpi_cards:
            self.kpi_cards[key].config(text="Error")
    
    def refresh(self):
        """Refrescar datos del dashboard"""
        self.load_dashboard_data()
    
    def cleanup(self):
        """Limpiar recursos del dashboard"""
        pass