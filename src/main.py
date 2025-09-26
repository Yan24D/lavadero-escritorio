"""
Sistema de Gestión de Lavadero de Vehículos
Aplicación principal - Punto de entrada
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_config import db
from src.auth.login import LoginWindow

class LaundryApp:
    """Aplicación principal del sistema de lavadero"""
    
    def __init__(self):
        self.root = None
        self.current_user = None
        self.current_role = None
    
    def initialize_database(self):
        """Inicializar y probar conexión a base de datos"""
        print("🚀 Iniciando Sistema de Lavadero...")
        
        if not db.test_connection():
            messagebox.showerror(
                "Error de Conexión", 
                "No se pudo conectar a la base de datos MySQL.\n\n"
                "Verifica que:\n"
                "• XAMPP esté ejecutándose\n"
                "• MySQL esté activo\n"
                "• La base de datos 'lavadero' exista\n"
                "• Las credenciales en .env sean correctas"
            )
            return False
        return True
    
    def start_login(self):
        """Iniciar ventana de login"""
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal
        
        # Crear ventana de login
        login_window = LoginWindow(self.root, self.on_login_success)
        
        # Centrar ventana en la pantalla
        self.root.geometry("450x600")
        self.root.eval('tk::PlaceWindow . center')
        
        # Configuraciones de la ventana principal
        self.root.title("Sistema Lavadero - Login")
        self.root.resizable(True, True)
        
        # Evento al cerrar la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        return self.root
    
    def on_login_success(self, user_data):
        """Callback cuando el login es exitoso"""
        self.current_user = user_data
        self.current_role = user_data['rol']
        
        print(f"✅ Login exitoso: {user_data['nombre']} ({user_data['rol']})")
        
        # Ocultar ventana de login
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Cargar interfaz según el rol
        if self.current_role == 'admin':
            self.load_admin_interface()
        else:
            self.load_secretary_interface()
    
    def load_admin_interface(self):
        """Cargar interfaz de administrador"""
        try:
            from src.admin.admin_panel import AdminPanel
            
            self.root.deiconify()  # Mostrar ventana principal
            AdminPanel(self.root, self.current_user, self.logout)
            print("✅ Panel del administrador cargado exitosamente")
            
        except Exception as e:
            print(f"❌ Error cargando panel del administrador: {e}")
            # Fallback - mostrar mensaje temporal si falla
            self.root.geometry("1200x800")
            self.root.title("Sistema Lavadero - Panel Administrador")
            
            frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
            frame.pack(fill='both', expand=True)
            
            title = tk.Label(
                frame, 
                text="❌ Error cargando interfaz de administrador", 
                font=('Arial', 24, 'bold'),
                fg='white',
                bg='#2c3e50'
            )
            title.pack(pady=(50, 20))
            
            logout_btn = tk.Button(
                frame,
                text="Cerrar Sesión",
                font=('Arial', 12),
                bg='#e74c3c',
                fg='white',
                padx=30,
                pady=10,
                command=self.logout
            )
            logout_btn.pack(pady=20)
        
    def load_secretary_interface(self):
        
        """Cargar interfaz de secretario"""
        try:
            from src.secretary.register import SecretaryRegisterPanel
            
            self.root.deiconify()  # Mostrar ventana principal
            
            # Crear panel del secretario
            SecretaryRegisterPanel(self.root, self.current_user, self.logout)
            print("✅ Panel del secretario cargado exitosamente")
            
        except Exception as e:
            print(f"❌ Error cargando panel del secretario: {e}")
            # Fallback - mostrar interfaz temporal
            self.root.geometry("1000x700")
            self.root.title("Sistema Lavadero - Panel Secretario")
            
            frame = tk.Frame(self.root, bg='#34495e', padx=20, pady=20)
            frame.pack(fill='both', expand=True)
            
            title = tk.Label(
                frame, 
                text=f"👋 Error cargando interfaz", 
                font=('Arial', 24, 'bold'),
                fg='white',
                bg='#34495e'
            )
            title.pack(pady=(50, 20))
            
            logout_btn = tk.Button(
                frame,
                text="Cerrar Sesión",
                font=('Arial', 12),
                bg='#e67e22',
                fg='white',
                padx=30,
                pady=10,
                command=self.logout
            )
            logout_btn.pack(pady=20)
    
    def logout(self):
        """Cerrar sesión y volver al login"""
        self.current_user = None
        self.current_role = None
        
        # Limpiar ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Volver a mostrar login
        self.root.geometry("400x300")
        self.root.title("Sistema Lavadero - Login")
        
        from src.auth.login import LoginWindow
        LoginWindow(self.root, self.on_login_success)
    
    def on_closing(self):
        """Manejar cierre de aplicación"""
        if messagebox.askokcancel("Salir", "¿Deseas salir del sistema?"):
            db.disconnect()
            self.root.destroy()
            sys.exit()
    
    def run(self):
        """Ejecutar la aplicación"""
        if not self.initialize_database():
            return
        
        root = self.start_login()
        root.mainloop()

def main():
    """Función principal"""
    app = LaundryApp()
    app.run()

if __name__ == "__main__":
    main()

"""
Sistema de Gestión de Lavadero de Vehículos
Aplicación principal - Punto de entrada
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_config import db
from src.auth.login import LoginWindow

class LaundryApp:
    """Aplicación principal del sistema de lavadero"""
    
    def __init__(self):
        self.root = None
        self.current_user = None
        self.current_role = None
    
    def initialize_database(self):
        """Inicializar y probar conexión a base de datos"""
        print("🚀 Iniciando Sistema de Lavadero...")
        
        if not db.test_connection():
            messagebox.showerror(
                "Error de Conexión", 
                "No se pudo conectar a la base de datos MySQL.\n\n"
                "Verifica que:\n"
                "• XAMPP esté ejecutándose\n"
                "• MySQL esté activo\n"
                "• La base de datos 'lavadero' exista\n"
                "• Las credenciales en .env sean correctas"
            )
            return False
        return True
    
    def start_login(self):
        """Iniciar ventana de login"""
        self.root = tk.Tk()
        self.root.withdraw()  # Ocultar ventana principal
        
        # Crear ventana de login
        login_window = LoginWindow(self.root, self.on_login_success)
        
        # Centrar ventana en la pantalla
        self.root.geometry("400x300")
        self.root.eval('tk::PlaceWindow . center')
        
        # Configuraciones de la ventana principal
        self.root.title("Sistema Lavadero - Login")
        self.root.resizable(False, False)
        
        # Evento al cerrar la aplicación
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        return self.root
    
    def on_login_success(self, user_data):
        """Callback cuando el login es exitoso"""
        self.current_user = user_data
        self.current_role = user_data['rol']
        
        print(f"✅ Login exitoso: {user_data['nombre']} ({user_data['rol']})")
        
        # Ocultar ventana de login
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Cargar interfaz según el rol
        if self.current_role == 'admin':
            self.load_admin_interface()
        else:
            self.load_secretary_interface()
    
    def load_admin_interface(self):
        """Cargar interfaz de administrador"""
        self.root.deiconify()  # Mostrar ventana principal
        self.root.geometry("1200x800")
        self.root.title("Sistema Lavadero - Panel Administrador")
        
        # Por ahora, mostrar mensaje temporal
        frame = tk.Frame(self.root, bg='#2c3e50', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        title = tk.Label(
            frame, 
            text=f"👋 Bienvenido, {self.current_user['nombre']}", 
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='#2c3e50'
        )
        title.pack(pady=(50, 20))
        
        subtitle = tk.Label(
            frame,
            text="Panel de Administrador",
            font=('Arial', 16),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        subtitle.pack(pady=(0, 30))
        
        # Botón temporal de logout
        logout_btn = tk.Button(
            frame,
            text="Cerrar Sesión",
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            padx=30,
            pady=10,
            command=self.logout
        )
        logout_btn.pack(pady=20)
    
    def load_secretary_interface(self):
        """Cargar interfaz de secretario"""
        from src.secretary.register import SecretaryRegisterPanel
        
        self.root.deiconify()  # Mostrar ventana principal
        
        # Crear panel del secretario
        SecretaryRegisterPanel(self.root, self.current_user, self.logout)
    
    def logout(self):
        """Cerrar sesión y volver al login"""
        self.current_user = None
        self.current_role = None
        
        # Limpiar ventana actual
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Volver a mostrar login
        self.root.geometry("400x300")
        self.root.title("Sistema Lavadero - Login")
        
        from src.auth.login import LoginWindow
        LoginWindow(self.root, self.on_login_success)
    
    def on_closing(self):
        """Manejar cierre de aplicación"""
        if messagebox.askokcancel("Salir", "¿Deseas salir del sistema?"):
            db.disconnect()
            self.root.destroy()
            sys.exit()
    
    def run(self):
        """Ejecutar la aplicación"""
        if not self.initialize_database():
            return
        
        root = self.start_login()
        root.mainloop()

def main():
    """Función principal"""
    app = LaundryApp()
    app.run()

if __name__ == "__main__":
    main()