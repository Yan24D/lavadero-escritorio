import mysql.connector
from mysql.connector import Error
import os

# Función para cargar variables de entorno manualmente (sin python-dotenv)
def load_env_manual():
    env_vars = {}
    env_file = '.env'
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
    return env_vars

# Cargar variables de entorno
env_vars = load_env_manual()

class DatabaseConfig:
    """Configuración y manejo de conexión a MySQL"""
    
    def __init__(self):
        self.host = env_vars.get('DB_HOST', 'localhost')
        self.user = env_vars.get('DB_USER', 'root')
        self.password = env_vars.get('DB_PASS', '')
        self.database = env_vars.get('DB_NAME', 'lavadero')
        self.port = int(env_vars.get('DB_PORT', 3306))
        self.connection = None
    
    def connect(self):
        """Establecer conexión con la base de datos"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset='utf8',
                autocommit=True
            )
            
            if self.connection.is_connected():
                print("✅ Conexión exitosa a MySQL")
                return True
                
        except Error as e:
            print(f"❌ Error conectando a MySQL: {e}")
            return False
    
    def disconnect(self):
        """Cerrar conexión con la base de datos"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("🔌 Conexión MySQL cerrada")
    
    def get_connection(self):
        """Obtener la conexión actual o crear una nueva"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None):
        """Ejecutar consulta SELECT"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            result = cursor.fetchall()
            cursor.close()
            return result
            
        except Error as e:
            print(f"❌ Error ejecutando consulta: {e}")
            return None
    
    def execute_insert(self, query, params=None):
        """Ejecutar consulta INSERT"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            last_id = cursor.lastrowid
            cursor.close()
            return last_id
            
        except Error as e:
            print(f"❌ Error en INSERT: {e}")
            return None
    
    def execute_update(self, query, params=None):
        """Ejecutar consulta UPDATE o DELETE"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            affected_rows = cursor.rowcount
            cursor.close()
            return affected_rows
            
        except Error as e:
            print(f"❌ Error en UPDATE/DELETE: {e}")
            return None
    
    def test_connection(self):
        """Probar la conexión a la base de datos"""
        try:
            if self.connect():
                # Probar una consulta simple
                result = self.execute_query("SELECT 1 as test")
                if result:
                    print("🧪 Prueba de conexión exitosa")
                    return True
            return False
        except Exception as e:
            print(f"❌ Error en prueba de conexión: {e}")
            return False

# Instancia global de la configuración de BD
db = DatabaseConfig()