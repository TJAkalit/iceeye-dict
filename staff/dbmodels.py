from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey, 
    Integer,
    String,
    Boolean,
    Float
)

Base = declarative_base()

class Domain(Base):
    
    __tablename__ = 'domain'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    parent_id = Column(ForeignKey('domain.id'))

class PhysicalMachine(Base):
    
    __tablename__ = 'physical_machine'
    id = Column(Integer, primary_key=True)
    domain_id = Column(ForeignKey(Domain.id))
    name = Column(String(512), nullable=False)
    cpu = Column(Integer)
    ram = Column(Integer)

class VirtualMachine(Base):
    
    __tablename__ = 'virtual_machine'
    id = Column(Integer, primary_key=True)
    domain_id = Column(ForeignKey(Domain.id))
    name = Column(String(512), nullable=False)
    cpu = Column(Integer)
    ram = Column(Integer)
    
class Service(Base):
    
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False)
    cpu = Column(Float)
    ram = Column(Float)