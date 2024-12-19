import sqlalchemy as db
from dataclasses import dataclass
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Carregar variáveis do arquivo .env
load_dotenv()

# Por padrão, usar a URL pública para desenvolvimento local
DATABASE_URI = "mysql://root:kFUyaGqweaKQgjjmnkbHtbQEFSLCjAYK@junction.proxy.rlwy.net:48430/railway"

# Se estiver em produção no Railway, usar a URL privada
if os.getenv('PRODUCTION') == 'true':
    DATABASE_URI = "mysql://root:kFUyaGqweaKQgjjmnkbHtbQEFSLCjAYK@mysql-q8fq.railway.internal:3306/railway"

@dataclass
class ConnectionHandler:
    conn: Engine = None
    session: Session = None

    def __post_init__(self):
        try:
            logger.info("Tentando conectar ao banco de dados...")
            
            self.conn = db.create_engine(
                DATABASE_URI,
                pool_size=10,
                max_overflow=20,
                pool_timeout=30,
                pool_recycle=3600
            )

            # Testar a conexão
            with self.conn.connect() as connection:
                logger.info("Conexão bem-sucedida!")

            self.session = Session(bind=self.conn)

        except OperationalError as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def commit_transaction(self):
        try:
            self.session.commit()
        except Exception as e:
            logger.error(f"Erro ao realizar commit: {e}")
            self.session.rollback()
            raise

    def rollback_transaction(self):
        try:
            self.session.rollback()
        except Exception as e:
            logger.error(f"Erro ao realizar rollback: {e}")
            raise

# Testar a conexão com o banco de dados
try:
    handler = ConnectionHandler()
except Exception as e:
    logger.error(f"Erro inesperado: {e}")