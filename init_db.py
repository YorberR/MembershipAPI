#!/usr/bin/env python3
"""
Script para inicializar la base de datos y crear todas las tablas.
Ejecuta este script después de configurar tu .env con la conexión a PostgreSQL.
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path para importar los módulos
sys.path.append(str(Path(__file__).parent))

from sqlmodel import SQLModel, text
from app.db.db import engine
from app.core.logging import setup_logging, get_logger

# Importar todos los modelos para que SQLModel los registre
from app.models import (
    Customer, Plan, Transaction, CustomerPlan, Invoice
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


def init_database():
    """Inicializar la base de datos creando todas las tablas."""
    try:
        logger.info("Iniciando creación de tablas en la base de datos...")
        
        # Crear todas las tablas
        SQLModel.metadata.create_all(engine)
        
        logger.info("Tablas creadas exitosamente!")
        logger.info("Las siguientes tablas fueron creadas:")
        
        # Listar las tablas creadas
        for table_name in SQLModel.metadata.tables.keys():
            logger.info(f"  - {table_name}")
            
    except Exception as e:
        logger.error(f"Error al crear las tablas: {e}")
        sys.exit(1)


def check_database_connection():
    """Verificar la conexión a la base de datos."""
    try:
        logger.info("Verificando conexión a la base de datos...")
        
        # Intentar conectar
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            logger.info("Conexión a la base de datos exitosa!")
            return True
            
    except Exception as e:
        logger.error(f"Error de conexión a la base de datos: {e}")
        logger.error("Verifica tu configuración en el archivo .env")
        return False


if __name__ == "__main__":
    print("Inicializando base de datos...")
    
    # Verificar conexión primero
    if not check_database_connection():
        sys.exit(1)
    
    # Crear tablas
    init_database()
    
    print("Base de datos inicializada correctamente!")
    print("Puedes ejecutar tu aplicación con: python start.py")