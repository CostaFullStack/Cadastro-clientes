import sqlalchemy as db
from dataclasses import dataclass
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter credenciais do banco de dados do arquivo .env
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# String de conexão para MySQL com pymysql
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

@dataclass(kw_only=True)
class ConnectionHandler:
    host: str = DB_HOST
    user: str = DB_USER
    password: str = DB_PASSWORD
    database: str = DB_NAME
    port: int = int(DB_PORT)
    conn: Engine = None
    session: Session = None

    def __post_init__(self):
        # Criar a conexão com o banco de dados usando SQLAlchemy
        self.conn = db.create_engine(DATABASE_URI)
        # Criar uma sessão para interagir com o banco
        self.session = Session(bind=self.conn)

# Instanciar a classe ConnectionHandler para criar a conexão
handler = ConnectionHandler()
