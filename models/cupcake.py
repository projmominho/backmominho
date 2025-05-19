from sqlalchemy import Column, Integer, String, Float, Boolean
from db import Base


# Model Cupcake - representa a tabela cupcakes no banco de dados
class Cupcake(Base):
    __tablename__ = "cupcake"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    disponibilidade = Column(Boolean, default=True)
    ingredientes = Column(String)
    peso = Column(Float)
    dimensoes = Column(String)
    informacoes_nutricionais = Column(String)
    imagem = Column(String)
