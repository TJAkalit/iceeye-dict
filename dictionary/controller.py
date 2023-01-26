from abc import ABC
from staff.dbmodels import (
    PhysicalMachine,
    VirtualMachine,
    Service,
)
from staff.datamodels import (
    PhysicalMachineInit, PhysicalMachineItem,
    VirtualMachineInit, VirtualMachineItem,
    ServiceInit, ServiceItem,
)
from staff.db import Session
from sqlalchemy import select, delete
from pydantic import BaseModel
from typing import List
from fastapi import HTTPException

class AbstractController(ABC):

    dbModel = None
    dataModel: BaseModel = None
    createDataModel: BaseModel = None
    s0: Session = None
    
    def __init__(self, s0: Session):
        pass
    
    async def create(self)->BaseModel:
        pass

    async def get(self)->BaseModel:
        pass

    async def all(self)->List[BaseModel]:
        pass

    async def update(self):
        pass

    async def delete(self):
        pass

class Controller(AbstractController):
    
    def __init__(self, s0):
        self.s0 = s0
    
    async def get(self, objId: int):
        
        query = select(self.dbModel).where(self.dbModel.id==objId)
        result = await self.s0.execute(query)
        data = [
            self.dataModel.from_orm(x[0]) for x in result.fetchall()
        ]
        if data.__len__()==0:
            raise HTTPException
        
        return data[0]
    
    async def all(self):
        
        query = select(self.dbModel)
        result = await self.s0.execute(query)
        data = [
            self.dataModel.from_orm(x[0]) for x in result.fetchall()
        ]
        return data
    
    async def delete(self, objId: int):
        
        query = delete(self.dbModel).where(self.dbModel.id==objId)
        result = await self.s0.execute(query)
        print(result.rowcount)
        if result.rowcount ==0:
            raise HTTPException(404)
        await self.s0.commit()
        return True

class PhysicalMachineController(Controller):

    dbModel = PhysicalMachine
    dataModel = PhysicalMachineItem

class VirtualMachineController(Controller):

    dbModel = VirtualMachine
    dataModel = VirtualMachineItem

class ServiceController(Controller):

    dbModel = Service
    dataModel = ServiceItem