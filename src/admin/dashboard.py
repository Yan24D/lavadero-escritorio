import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from database.db_config import db

class AdminDashboard:
    def __init__(self, parent):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        tk.Label(
            self.parent,
            text="📈 Dashboard",
            font=("Segoe UI", 20, "bold"),
            bg="#f8fafc"
        ).pack(pady=20)

        # Aquí agregarás cards, estadísticas y gráficos
    def show_dashboard(self):
        """Mostrar dashboard con estadísticas"""
        # Título del módulo
        title_frame = tk.Frame(self.content_area, bg='#f8fafc')
        title_frame.pack(fill='x', pady=(0, 20))
        
        title_label = tk.Label(
            title_frame,
            text="📈 Dashboard - Estadísticas del Negocio",
            font=('Segoe UI', 24, 'bold'),
            fg='#1e293b',
            bg='#f8fafc'
        )
        title_label.pack(side='left')
        
        # Filtros de fecha
        filters_frame = tk.Frame(self.content_area, bg='white', relief='solid', borderwidth=1)
        filters_frame.pack(fill='x', pady=(0, 20))
        
        filters_content = tk.Frame(filters_frame, bg='white')
        filters_content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(
            filters_content,
            text="📅 Filtros de Período:",
            font=('Segoe UI', 12, 'bold'),
            bg='white'
        ).pack(side='left')
        
        # Selector de período
        period_var = tk.StringVar(value="semana")
        periods = [("Última Semana", "semana"), ("Último Mes", "mes"), ("Rango Custom", "custom")]
        
        for text, value in periods:
            rb = tk.Radiobutton(
                filters_content,
                text=text,
                variable=period_var,
                value=value,
                font=('Segoe UI', 10),
                bg='white',
                command=lambda: self.update_dashboard_data(period_var.get())
            )
            rb.pack(side='left', padx=(20, 0))
        
        # Cards de resumen
        self.create_dashboard_cards()
        
        # Gráficos
        self.create_dashboard_charts(period_var.get())
        
        # Cargar datos iniciales
        self.update_dashboard_data("semana")
    
    def create_dashboard_cards(self):
        """Crear cards de resumen para dashboard"""
        cards_frame = tk.Frame(self.content_area, bg='#f8fafc')
        cards_frame.pack(fill='x', pady=(0, 20))
        
        # Card 1 - Ingresos Totales
        ingresos_card = self.create_summary_card(
            cards_frame, "💰 Ingresos Totales", "$0", "#059669", 0
        )
        
        # Card 2 - Servicios Realizados
        servicios_card = self.create_summary_card(
            cards_frame, "⚙️ Servicios Realizados", "0", "#2563eb", 1
        )
        
        # Card 3 - Lavadores Activos
        lavadores_card = self.create_summary_card(
            cards_frame, "👥 Lavadores Activos", "0", "#d97706", 2
        )
        
        # Card 4 - Promedio por Día
        promedio_card = self.create_summary_card(
            cards_frame, "📊 Promedio Diario", "$0", "#7c3aed", 3
        )
        
        # Guardar referencias para actualizar
        self.dashboard_cards = {
            'ingresos': ingresos_card,
            'servicios': servicios_card,
            'lavadores': lavadores_card,
            'promedio': promedio_card
        }
    
    def create_summary_card(self, parent, title, value, color, column):
        """Crear una card de resumen"""
        card = tk.Frame(parent, bg=color, relief='solid', borderwidth=1)
        card.pack(side='left', fill='x', expand=True, padx=5 if column > 0 else 0)
        
        content = tk.Frame(card, bg=color)
        content.pack(fill='both', expand=True, padx=20, pady=20)
        
        title_label = tk.Label(
            content,
            text=title,
            font=('Segoe UI', 11, 'bold'),
            fg='white',
            bg=color
        )
        title_label.pack()
        
        value_label = tk.Label(
            content,
            text=value,
            font=('Segoe UI', 20, 'bold'),
            fg='white',
            bg=color
        )
        value_label.pack(pady=(8, 0))
        
        return {'title': title_label, 'value': value_label}
    
    def create_dashboard_charts(self, period):
        """Crear gráficos del dashboard"""
        # Container para gráficos
        charts_container = tk.Frame(self.content_area, bg='#f8fafc')
        charts_container.pack(fill='both', expand=True)
        
        # Gráfico de ingresos por día
        chart1_frame = tk.Frame(charts_container, bg='white', relief='solid', borderwidth=1)
        chart1_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        tk.Label(
            chart1_frame,
            text="📈 Ingresos por Día",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(pady=(15, 10))
        
        # Crear figura de matplotlib
        self.fig1, self.ax1 = plt.subplots(figsize=(8, 4))
        self.canvas1 = FigureCanvasTkAgg(self.fig1, chart1_frame)
        self.canvas1.get_tk_widget().pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Gráfico de servicios por tipo
        chart2_frame = tk.Frame(charts_container, bg='white', relief='solid', borderwidth=1)
        chart2_frame.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        tk.Label(
            chart2_frame,
            text="🥧 Servicios por Tipo",
            font=('Segoe UI', 14, 'bold'),
            bg='white',
            fg='#1e293b'
        ).pack(pady=(15, 10))
        
        # Crear segunda figura
        self.fig2, self.ax2 = plt.subplots(figsize=(6, 4))
        self.canvas2 = FigureCanvasTkAgg(self.fig2, chart2_frame)
        self.canvas2.get_tk_widget().pack(fill='both', expand=True, padx=15, pady=(0, 15))
    
    def update_dashboard_data(self, period):
        """Actualizar datos del dashboard"""
        try:
            # Calcular fechas según el período
            end_date = datetime.now().date()
            
            if period == "semana":
                start_date = end_date - timedelta(days=7)
            elif period == "mes":
                start_date = end_date - timedelta(days=30)
            else:  # custom - por ahora usar semana
                start_date = end_date - timedelta(days=7)
            
            # Query para resumen general
            summary_query = """
                SELECT 
                    COUNT(*) as total_servicios,
                    COALESCE(SUM(costo), 0) as total_ingresos,
                    COUNT(DISTINCT lavador) as lavadores_activos
                FROM vista_registros_completos
                WHERE fecha BETWEEN %s AND %s
            """
            
            summary_data = db.execute_query(summary_query, (start_date, end_date))
            
            if summary_data:
                data = summary_data[0]
                days_count = (end_date - start_date).days or 1
                promedio_diario = data['total_ingresos'] / days_count
                
                # Actualizar cards
                self.dashboard_cards['ingresos']['value'].config(text=f"${data['total_ingresos']:,.0f}")
                self.dashboard_cards['servicios']['value'].config(text=str(data['total_servicios']))
                self.dashboard_cards['lavadores']['value'].config(text=str(data['lavadores_activos']))
                self.dashboard_cards['promedio']['value'].config(text=f"${promedio_diario:,.0f}")
            
            # Actualizar gráficos
            self.update_charts(start_date, end_date)
            
        except Exception as e:
            print(f"Error actualizando dashboard: {e}")
            messagebox.showerror("Error", "Error al cargar datos del dashboard")
    
    def update_charts(self, start_date, end_date):
        """Actualizar gráficos con nuevos datos"""
        try:
            # Gráfico 1: Ingresos por día
            daily_query = """
                SELECT fecha, SUM(costo) as ingresos
                FROM vista_registros_completos
                WHERE fecha BETWEEN %s AND %s
                GROUP BY fecha
                ORDER BY fecha
            """
            
            daily_data = db.execute_query(daily_query, (start_date, end_date))
            
            # Limpiar gráfico anterior
            self.ax1.clear()
            
            if daily_data:
                dates = [row['fecha'] for row in daily_data]
                ingresos = [row['ingresos'] for row in daily_data]
                
                self.ax1.plot(dates, ingresos, marker='o', linewidth=2, color='#059669')
                self.ax1.set_title('Ingresos Diarios', fontsize=12, pad=20)
                self.ax1.set_ylabel('Ingresos ($)')
                self.ax1.grid(True, alpha=0.3)
                
                # Formato de fechas
                self.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
                self.ax1.xaxis.set_major_locator(mdates.DayLocator(interval=1))
                plt.setp(self.ax1.xaxis.get_majorticklabels(), rotation=45)
            else:
                self.ax1.text(0.5, 0.5, 'No hay datos', ha='center', va='center', transform=self.ax1.transAxes)
            
            self.fig1.tight_layout()
            self.canvas1.draw()
            
            # Gráfico 2: Servicios por tipo
            services_query = """
                SELECT servicio_nombre, COUNT(*) as cantidad
                FROM vista_registros_completos
                WHERE fecha BETWEEN %s AND %s
                GROUP BY servicio_nombre
                ORDER BY cantidad DESC
                LIMIT 5
            """
            
            services_data = db.execute_query(services_query, (start_date, end_date))
            
            # Limpiar gráfico anterior
            self.ax2.clear()
            
            if services_data:
                services = [row['servicio_nombre'] for row in services_data]
                counts = [row['cantidad'] for row in services_data]
                
                colors = ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed']
                
                self.ax2.pie(counts, labels=services, autopct='%1.1f%%', colors=colors[:len(counts)])
                self.ax2.set_title('Distribución de Servicios', fontsize=12, pad=20)
            else:
                self.ax2.text(0.5, 0.5, 'No hay datos', ha='center', va='center', transform=self.ax2.transAxes)
            
            self.canvas2.draw()
            
        except Exception as e:
            print(f"Error actualizando gráficos: {e}")
    
    