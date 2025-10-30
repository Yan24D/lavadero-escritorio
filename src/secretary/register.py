"""
Módulo de Registro de Servicios para Secretario
Maneja el registro de vehículos y servicios prestados
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re
from database.db_config import db
from secretary.base_module import BaseModule


class RegisterModule(BaseModule):
    """Módulo para registrar servicios"""
    
    def __init__(self, user_data):
        super().__init__(user_data)
        self.vehicle_types = []
        self.lavadores_data = []
        self.current_services = []
        self.selected_service = None
    
    def render(self, parent):
        """Renderizar módulo de registro"""
        self.parent_frame = parent
        self.clear_parent(parent)
        
        main_container = tk.Frame(parent, bg='#f8fafc')
        main_container.pack(fill='both', expand=True)
        
        header = self.create_section_header(
            main_container,
            "Detalles del Servicio",
            "📋"
        )
        header.pack(anchor='w', pady=(0, 20))
        
        # Canvas con scrollbar
        canvas_frame = tk.Frame(main_container, bg='#f8fafc')
        canvas_frame.pack(fill='both', expand=True)
        
        canvas = tk.Canvas(canvas_frame, bg='#f8fafc', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg='#f8fafc')
        
        # IMPORTANTE: Esta función ajusta el ancho del contenido al canvas
        def _on_frame_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        def _on_canvas_configure(event):
            # Ajustar el ancho del frame interno al ancho del canvas
            canvas.itemconfig(canvas_window, width=event.width)
        
        scrollable_frame.bind("<Configure>", _on_frame_configure)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Scroll con mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux scroll up
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux scroll down

        # Form container
        form_container = tk.Frame(scrollable_frame, bg='white', relief='solid', borderwidth=1)
        form_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        form_content = tk.Frame(form_container, bg='white')
        form_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        self.create_form_fields(form_content)
        self.load_data()

    def create_form_fields(self, parent):
        """Crear campos del formulario"""
        # Fila 1: Fecha y Hora
        row1 = tk.Frame(parent, bg='white')
        row1.pack(fill='x', pady=(0, 15))
        
        date_frame = tk.Frame(row1, bg='white')
        date_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.date_entry = self.create_input_field(date_frame, "Fecha:")
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        time_frame = tk.Frame(row1, bg='white')
        time_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.time_entry = self.create_input_field(time_frame, "Hora:")
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))
        
        # Fila 2: Tipo de Vehículo y Placa
        row2 = tk.Frame(parent, bg='white')
        row2.pack(fill='x', pady=(0, 15))
        
        vehicle_frame = tk.Frame(row2, bg='white')
        vehicle_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        tk.Label(
            vehicle_frame, text="Tipo de Vehículo:",
            font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151'
        ).pack(anchor='w')
        
        self.vehicle_var = tk.StringVar()
        self.vehicle_combo = ttk.Combobox(
            vehicle_frame, textvariable=self.vehicle_var,
            font=('Segoe UI', 10), state='readonly'
        )
        self.vehicle_combo.pack(fill='x', pady=(5, 0), ipady=8)
        self.vehicle_combo.bind('<<ComboboxSelected>>', self.on_vehicle_selected)
        
        plate_frame = tk.Frame(row2, bg='white')
        plate_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.plate_entry = self.create_input_field(plate_frame, "Placa:")
        
        # Fila 3: Servicio
        row3 = tk.Frame(parent, bg='white')
        row3.pack(fill='x', pady=(0, 15))
        
        self.service_var = tk.StringVar()
        tk.Label(
            row3, text="Servicio:",
            font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151'
        ).pack(anchor='w')
        
        self.service_combo = ttk.Combobox(
            row3, textvariable=self.service_var,
            font=('Segoe UI', 10), state='readonly'
        )
        self.service_combo.pack(fill='x', pady=(5, 0), ipady=8)
        self.service_combo.bind('<<ComboboxSelected>>', self.on_service_selected)
        
        # Fila 4: Costo y Porcentaje
        row4 = tk.Frame(parent, bg='white')
        row4.pack(fill='x', pady=(0, 15))
        
        cost_frame = tk.Frame(row4, bg='white')
        cost_frame.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.cost_entry = self.create_input_field(cost_frame, "Costo ($):")
        
        percent_frame = tk.Frame(row4, bg='white')
        percent_frame.pack(side='right', fill='x', expand=True, padx=(10, 0))
        self.percent_entry = self.create_input_field(percent_frame, "Porcentaje (%):")
        self.percent_entry.insert(0, "50.00")
        
        # Fila 5: Lavador
        row5 = tk.Frame(parent, bg='white')
        row5.pack(fill='x', pady=(0, 15))
        
        self.lavador_var = tk.StringVar()
        tk.Label(
            row5, text="Lavador:",
            font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151'
        ).pack(anchor='w')
        
        self.lavador_combo = ttk.Combobox(
            row5, textvariable=self.lavador_var,
            font=('Segoe UI', 10), state='readonly'
        )
        self.lavador_combo.pack(fill='x', pady=(5, 0), ipady=8)
        
        # Fila 6: Estado de Pago
        row6 = tk.Frame(parent, bg='white')
        row6.pack(fill='x', pady=(0, 15))
        
        tk.Label(
            row6, text="Estado del Pago:",
            font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151'
        ).pack(anchor='w')
        
        self.payment_status_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            row6, text="Pagado",
            variable=self.payment_status_var,
            font=('Segoe UI', 10), bg='white', fg='#374151'
        ).pack(anchor='w', pady=(5, 0))
        
        # Fila 7: Observaciones
        row7 = tk.Frame(parent, bg='white')
        row7.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            row7, text="Observaciones:",
            font=('Segoe UI', 10, 'bold'), bg='white', fg='#374151'
        ).pack(anchor='w')
        
        self.observations_text = tk.Text(
            row7, font=('Segoe UI', 10), relief='solid', borderwidth=1,
            bg='#f9fafb', height=3
        )
        self.observations_text.pack(fill='x', pady=(5, 0))
        
        # Botones
        buttons_frame = tk.Frame(parent, bg='white')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        clear_btn = self.create_button(
            buttons_frame, "🗑️ Limpiar",
            self.clear_form, bg_color='#6b7280'
        )
        clear_btn.pack(side='left', padx=(0, 10))
        
        register_btn = self.create_button(
            buttons_frame, "✅ Registrar Servicio",
            self.register_service, bg_color='#059669'
        )
        register_btn.pack(side='right')
    
    def load_data(self):
        """Cargar tipos de vehículos y lavadores"""
        try:
            self.load_vehicle_types()
            self.load_lavadores()
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando datos: {str(e)}")
    
    def refresh(self):
        """Refrescar datos"""
        self.load_data()
    
    def load_vehicle_types(self):
        """Cargar tipos de vehículos"""
        self.vehicle_types = [
            {'value': 'motorcycle', 'display': 'Motocicleta'},
            {'value': 'car', 'display': 'Automóvil'},
            {'value': 'pickup', 'display': 'Camioneta'},
            {'value': 'suv', 'display': 'SUV'},
            {'value': 'truck', 'display': 'Camión'}
        ]
        
        vehicle_names = [item['display'] for item in self.vehicle_types]
        self.vehicle_combo['values'] = vehicle_names
    
    def load_lavadores(self):
        """Cargar lista de lavadores activos"""
        try:
            query = """
                SELECT id, CONCAT(nombre, ' ', apellido) as nombre_completo 
                FROM lavadores 
                WHERE activo = 1 
                ORDER BY nombre
            """
            self.lavadores_data = db.execute_query(query) or []
            
            if self.lavadores_data:
                lavador_names = [l['nombre_completo'] for l in self.lavadores_data]
                self.lavador_combo['values'] = lavador_names
        except Exception as e:
            print(f"Error cargando lavadores: {e}")
    
    def on_vehicle_selected(self, event=None):
        """Cargar servicios cuando se selecciona un vehículo"""
        selected_display = self.vehicle_var.get()
        if not selected_display:
            return
        
        vehicle_value = next(
            (item['value'] for item in self.vehicle_types 
             if item['display'] == selected_display), None
        )
        
        if vehicle_value:
            self.load_services_for_vehicle(vehicle_value)
    
    def load_services_for_vehicle(self, vehicle_type):
        """Cargar servicios disponibles para tipo de vehículo"""
        try:
            query = """
                SELECT s.id, s.nombre, s.descripcion, sp.precio,
                    CONCAT('$', FORMAT(sp.precio, 0)) as precio_formato
                FROM servicios s
                INNER JOIN servicio_precios sp ON s.id = sp.id_servicio
                WHERE sp.tipo_vehiculo = %s AND sp.activo = 1
                ORDER BY sp.precio ASC
            """
            
            self.current_services = db.execute_query(query, (vehicle_type,)) or []
            
            service_names = [
                f"{s['nombre']} - {s['precio_formato']}" 
                for s in self.current_services
            ]
            self.service_combo['values'] = service_names
            self.service_combo.set("")
        except Exception as e:
            print(f"Error cargando servicios: {e}")
    
    def on_service_selected(self, event=None):
        """Actualizar costo cuando se selecciona un servicio"""
        selected_text = self.service_var.get()
        if not selected_text:
            return
        
        self.selected_service = next(
            (s for s in self.current_services 
             if f"{s['nombre']} - {s['precio_formato']}" == selected_text), None
        )
        
        if self.selected_service:
            self.cost_entry.delete(0, tk.END)
            self.cost_entry.insert(0, f"{self.selected_service['precio']:,.0f}")
    
    def clear_form(self):
        """Limpiar todos los campos del formulario"""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.time_entry.delete(0, tk.END)
        self.time_entry.insert(0, datetime.now().strftime('%H:%M'))
        
        self.vehicle_var.set("")
        self.plate_entry.delete(0, tk.END)
        self.service_var.set("")
        self.cost_entry.delete(0, tk.END)
        self.percent_entry.delete(0, tk.END)
        self.percent_entry.insert(0, "50.00")
        self.lavador_var.set("")
        self.payment_status_var.set(False)
        self.observations_text.delete(1.0, tk.END)
        
        self.service_combo['values'] = []
        self.selected_service = None
    
    def validate_form(self):
        """Validar campos del formulario"""
        if not self.vehicle_var.get():
            messagebox.showerror("Error", "Debe seleccionar un tipo de vehículo")
            return False
        
        if not self.selected_service:
            messagebox.showerror("Error", "Debe seleccionar un servicio")
            return False
        
        if not self.cost_entry.get().strip():
            messagebox.showerror("Error", "El campo Costo es obligatorio")
            return False
        
        try:
            datetime.strptime(self.date_entry.get(), '%Y-%m-%d')
            datetime.strptime(self.time_entry.get(), '%H:%M')
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha/hora inválido")
            return False
        
        if self.plate_entry.get().strip():
            if not self._validate_plate(self.plate_entry.get()):
                messagebox.showerror("Error", 
                    "Placa inválida. Formatos: ABC123 (carro) o ABC12D (moto)")
                return False
        
        try:
            float(self.cost_entry.get().replace(',', ''))
            float(self.percent_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Valores numéricos inválidos")
            return False
        
        return True
    
    def _validate_plate(self, plate):
        """Validar formato de placa colombiana"""
        plate = plate.upper().strip()
        patron_carro = r'^[A-Z]{3}\d{3}$'
        patron_moto = r'^[A-Z]{3}\d{2}[A-Z]$'
        return bool(re.match(patron_carro, plate) or re.match(patron_moto, plate))
    
    def register_service(self):
        """Registrar nuevo servicio en la base de datos"""
        if not self.validate_form():
            return
        
        try:
            vehicle_value = next(
                (item['value'] for item in self.vehicle_types 
                 if item['display'] == self.vehicle_var.get()), None
            )
            
            lavador_name = self.lavador_var.get()
            
            registro_data = {
                'fecha': self.date_entry.get(),
                'hora': self.time_entry.get(),
                'vehiculo': vehicle_value,
                'placa': self.plate_entry.get().strip().upper() or None,
                'id_servicio': self.selected_service['id'],
                'costo': float(self.cost_entry.get().replace(',', '')),
                'porcentaje': float(self.percent_entry.get()) or 50.0,
                'lavador': lavador_name or None,
                'observaciones': self.observations_text.get(1.0, tk.END).strip() or None,
                'pago': 'Pagado' if self.payment_status_var.get() else 'Pendiente',
                'id_usuario': self.user_data['id']
            }
            
            query = """
                INSERT INTO registros 
                (fecha, hora, vehiculo, placa, id_servicio, costo, porcentaje, 
                 lavador, observaciones, pago, id_usuario)
                VALUES (%(fecha)s, %(hora)s, %(vehiculo)s, %(placa)s, %(id_servicio)s,
                        %(costo)s, %(porcentaje)s, %(lavador)s, %(observaciones)s, 
                        %(pago)s, %(id_usuario)s)
            """
            
            registro_id = db.execute_insert(query, registro_data)
            
            if registro_id:
                messagebox.showinfo("Éxito", "Servicio registrado correctamente")
                self.clear_form()
            else:
                messagebox.showerror("Error", "No se pudo registrar el servicio")
                
        except Exception as e:
            print(f"Error registrando servicio: {e}")
            messagebox.showerror("Error", f"Error al registrar: {str(e)}")