from connection_handler import ConnectionHandler
from sqlalchemy import (
    Column,
    String,
    Integer,
    Time
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(180), nullable=False)
    email = Column(String(50), unique=False, nullable=False)
    telefone = Column(String(100), nullable=False)
    horario = Column(Time, nullable=False)
    servicos = Column(String(100), nullable=False)

    def __repr__(self):
        return f"Cliente: <{self.nome}, {self.servicos}>"

handler = ConnectionHandler()

Base.metadata.create_all(bind=handler.conn)

