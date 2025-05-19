from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base


# Modelo Pedido - representa a tabela de pedidos no banco de dados
class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, index=True)
    telefone = Column(String, nullable=False)
    endereco = Column(String, nullable=False)
    valor_pago = Column(Float, default=0.0)

    itens = relationship("PedidoItem", cascade="all, delete-orphan")
    status = relationship("PedidoStatus", cascade="all, delete-orphan")


# Modelo pedido_status - representa a tabela de status do pedido
class PedidoStatus(Base):
    __tablename__ = "pedido_status"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)
    data_status = Column(DateTime, default=datetime.utcnow)
    pedido_id = Column(Integer, ForeignKey("pedido.id"))


# Modelo pedido_item - representa os itens de um pedido (relacionamento com cupcakes)
class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id = Column(Integer, primary_key=True, index=True)
    quantidade = Column(Integer)
    observacoes = Column(String, default="")
    cupcake_id = Column(Integer, ForeignKey("cupcake.id"))
    pedido_id = Column(Integer, ForeignKey("pedido.id"))
