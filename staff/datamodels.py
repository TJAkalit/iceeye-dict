from pydantic import BaseModel
from typing import Optional

class DomainItem(BaseModel):
    
    id: int
    name: str
    
    class Config:
        orm_mode = True

class DomainInit(BaseModel):
    
    name: str
    
class PhysicalMachineItem(BaseModel):
    
    id: int
    name: str
    cpu: int
    ram: int
    
    class Config:
        orm_mode = True

class PhysicalMachineInit(BaseModel):
    
    name: str
    cpu: int
    ram: int

class VirtualMachineItem(BaseModel):
    
    id: int
    name: str
    cpu: int
    ram: int
    pm_id: Optional[int]
    
    class Config:
        orm_mode = True

class VirtualMachineInit(BaseModel):
    
    name: str
    cpu: int
    ram: int
    pm_id: Optional[int]
    
class ServiceItem(BaseModel):
    
    id: int
    name: str
    cpu: int
    ram: int
    
    class Config:
        orm_mode = True

class ServiceInit(BaseModel):
    
    name: str
    cpu: float
    ram: float