from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

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
    cpu_multiply: Optional[int]
    
    class Config:
        orm_mode = True

class PhysicalMachineInit(BaseModel):
    
    name: str
    cpu: int
    ram: int
    cpu_multiply: Optional[int]

class VirtualMachineItem(BaseModel):
    
    id: int
    name: str
    cpu: int
    ram: int
    size: int
    pm_id: Optional[int]
    
    class Config:
        orm_mode = True

class VirtualMachineInit(BaseModel):
    
    name: str
    cpu: int
    ram: int
    size: int
    pm_id: Optional[int]
    
class ServiceItem(BaseModel):
    
    id: int
    name: str
    cpu: float
    ram: float
    vm_id: Optional[int]
    
    class Config:
        orm_mode = True

class ServiceInit(BaseModel):
    
    name: str
    cpu: float
    ram: float
    vm_id: Optional[int]
    
class Load(BaseModel):
    
    ram: float
    cpu: float
    
    class Config:
        orm_mode = True
    
class PhysicalMachineLoad(BaseModel):

    id: int
    name: str
    cpu: int
    ram: int
    cpu_sum: float
    ram_sum: float
    storage_sum: int
    cpu_multiply: int
    virtual_machine_size: int
    virtual_machines: Optional[List[VirtualMachineItem]]
    
    class Config:
        orm_mode = True
        
class StorageType(Enum):
    
    SSD = 1
    HDD = 2
    NVMe = 3

class StorageInit(BaseModel):
    
    pm_id: int
    name: Optional[str]
    type: StorageType
    size: int

class StorageItem(BaseModel):
    
    id: int
    pm_id: int
    name: Optional[str]
    type: StorageType
    size: int
    
    class Config:
        orm_mode = True
        
class PhysicalMachineStorageSize(BaseModel):
    
    id: int
    size: int
    
    class Config:
        orm_mode = True
