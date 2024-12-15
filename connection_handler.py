import sqlalchemy as db
from dataclasses import dataclass
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

# Obter credenciais do banco de dados do arquivo .env
host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
port = os.getenv('port')
dbname = os.getenv('dbname')

# String de conexão para MySQL com pymysql
DATABASE_URI = f"postgres://{user}:{password}@{host}:{port}/{dbname}"

@dataclass(kw_only=True)
class ConnectionHandler:
    host: str = host
    user: str = user
    password: str = password
    database: str = dbname
    port: int = int(port)
    conn: Engine = None
    session: Session = None

    def __post_init__(self):
        # Criar a conexão com o banco de dados usando SQLAlchemy
        self.conn = db.create_engine(DATABASE_URI)
        # Criar uma sessão para interagir com o banco
        self.session = Session(bind=self.conn)

# Instanciar a classe ConnectionHandler para criar a conexão
handler = ConnectionHandler()
