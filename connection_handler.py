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

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter credenciais do banco de dados do arquivo .env
host = os.getenv('DB_HOST', 'aws-0-sa-east-1.pooler.supabase.com')
user = os.getenv('DB_USER', 'postgres.olhvmubncytcqaottytr')  # Transaction Pooler user
password = os.getenv('DB_PASSWORD', 'default_password')
port = os.getenv('DB_PORT', '6543')
dbname = os.getenv('DB_NAME', 'postgres')

# Validar se as variáveis obrigatórias estão presentes
required_envs = [host, user, password, port, dbname]
if not all(required_envs):
    raise ValueError("Algumas variáveis de ambiente estão faltando no arquivo .env!")

# Construir a string de conexão para o Transaction Pooler
DATABASE_URI = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"

@dataclass(kw_only=True)
class ConnectionHandler:
    host: str = host
    user: str = user
    password: str = password
    database: str = dbname
    port: int = int(port) if port.isdigit() else 6543
    conn: Engine = None
    session: Session = None

    def __post_init__(self):
        try:
            # Criar a conexão com o banco de dados usando SQLAlchemy
            logger.info("Tentando conectar ao banco de dados...")
            self.conn = db.create_engine(DATABASE_URI)

            # Testar a conexão
            with self.conn.connect() as connection:
                logger.info("Conexão bem-sucedida!")

            # Criar uma sessão para interagir com o banco
            self.session = Session(bind=self.conn)
        except OperationalError as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            raise

# Instanciar a classe ConnectionHandler para criar a conexão
try:
    handler = ConnectionHandler()
except ValueError as e:
    logger.error(f"Erro de configuração: {e}")
except Exception as e:
    logger.error(f"Erro inesperado: {e}")
