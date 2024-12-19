import sqlalchemy as db
from dataclasses import dataclass
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Obter credenciais do banco de dados do arquivo .env (agora com os valores do Railway)
host = os.getenv('DB_HOST', 'postgres.railway.internal')
user = os.getenv('DB_USER', 'postgres')  
password = os.getenv('DB_PASSWORD', 'LWsicuUpvxGBYxNrXGsKtNqbjdGciJmE')
port = os.getenv('DB_PORT', '5432')
dbname = os.getenv('DB_NAME', 'railway')

# Validar se as variáveis obrigatórias estão presentes
required_envs = [host, user, password, port, dbname]
if not all(required_envs):
    raise ValueError("Algumas variáveis de ambiente estão faltando no arquivo .env!")

# Construir a string de conexão para o Railway
DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

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
            self.session.rollback()  # Fazer rollback em caso de erro
            raise

    def rollback_transaction(self):
        try:
            self.session.rollback()
        except Exception as e:
            logger.error(f"Erro ao realizar rollback: {e}")
            raise

# Instanciar a classe ConnectionHandler para criar a conexão
try:
    handler = ConnectionHandler()
except Exception as e:
    logger.error(f"Erro inesperado: {e}")