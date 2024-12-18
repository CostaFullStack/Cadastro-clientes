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

load_dotenv()

host = os.getenv('DB_HOST', 'postgres.railway.internal')
user = os.getenv('DB_USER', 'postgres')  
password = os.getenv('DB_PASSWORD', 'LWsicuUpvxGBYxNrXGsKtNqbjdGciJmE')
port = os.getenv('DB_PORT', '5432')
dbname = os.getenv('DB_NAME', 'railway')

required_envs = [host, user, password, port, dbname]
if not all(required_envs):
    raise ValueError("Algumas variáveis de ambiente estão faltando no arquivo .env!")

DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

@dataclass(kw_only=True)
class ConnectionHandler:
    host: str = host
    user: str = user
    password: str = password
    database: str = dbname
    port: int = int(port) if port.isdigit() else 5432
    conn: Engine = None
    session: Session = None

    def __post_init__(self):
        try:
            logger.info("Tentando conectar ao banco de dados...")

            # Criar o engine com pool de conexões
            self.conn = db.create_engine(
                DATABASE_URI,
                pool_size=10,  # número de conexões no pool
                max_overflow=20,  # quantas conexões extras podem ser abertas
                pool_timeout=30,  # tempo limite para obter uma conexão do pool
                pool_recycle=3600  # tempo de reciclagem da conexão (em segundos)
            )

            with self.conn.connect() as connection:
                logger.info("Conexão bem-sucedida!")

            self.session = Session(bind=self.conn)

        except OperationalError as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

    def commit_transaction(self):
        """Comitar transação de forma segura."""
        try:
            self.session.commit()
        except Exception as e:
            logger.error(f"Erro ao realizar commit: {e}")
            self.session.rollback() 
            raise

    def rollback_transaction(self):
        """Reverter transação de forma segura."""
        try:
            self.session.rollback()
        except Exception as e:
            logger.error(f"Erro ao realizar rollback: {e}")
            raise

try:
    handler = ConnectionHandler()
except ValueError as e:
    logger.error(f"Erro de configuração: {e}")
except Exception as e:
    logger.error(f"Erro inesperado: {e}")
