"""
Clase base para todos los módulos del panel de administración
"""

class BaseModule:
    """Clase base para todos los módulos del admin"""
    
    def __init__(self, parent, user_data, db_connection):
        self.parent = parent
        self.user_data = user_data
        self.db = db_connection
        self.setup_module()
    
    def setup_module(self):
        """Configurar módulo - debe ser implementado por cada módulo"""
        raise NotImplementedError("Cada módulo debe implementar setup_module()")
    
    def cleanup(self):
        """Limpiar recursos del módulo - opcional"""
        pass
    
    def refresh(self):
        """Refrescar datos del módulo - opcional"""
        pass
