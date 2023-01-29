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
    cpu_multiply = Column(Integer, nullable=True)

class VirtualMachine(Base):
    
    __tablename__ = 'virtual_machine'
    id = Column(Integer, primary_key=True)
    domain_id = Column(ForeignKey(Domain.id))
    name = Column(String(512), nullable=False)
    cpu = Column(Integer)
    ram = Column(Integer)
    pm_id = Column(ForeignKey(PhysicalMachine.id), nullable=True)
    size = Column(Integer)
    
class Service(Base):
    
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String(512), nullable=False)
    cpu = Column(Float)
    ram = Column(Float)
    vm_id = Column(ForeignKey(VirtualMachine.id), nullable=True)
    
class Storage(Base):
    
    __tablename__ = 'storage'
    id = Column(Integer, primary_key=True)
    pm_id = Column(ForeignKey(PhysicalMachine.id))
    name = Column(String(512), nullable=True)
    type = Column(Integer, nullable=False)
    size = Column(Integer)
    