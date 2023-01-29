from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update, select, func

from staff.db import Session
from staff.datamodels import VirtualMachineInit, Load, VirtualMachineItem
from staff.dbmodels import VirtualMachine, Service, PhysicalMachine

from .controller import VirtualMachineController

virtMachine = APIRouter()

TAG = ('Virtual machine',)

@virtMachine.get('/', tags=TAG)
async def getAllMethod(name: str = None, host_name: str = None):
    
    async with Session() as s0:
        
        query = select(VirtualMachine).order_by(VirtualMachine.id)
        if name:
            query = query.filter(
                VirtualMachine.name.like(name + '%')
            )
        if host_name:
            query = query.filter(
                PhysicalMachine.id==VirtualMachine.pm_id,
                PhysicalMachine.name.like(host_name + '%')
            )
            
        result = await s0.execute(query)
        dataset = [VirtualMachineItem.from_orm(x[0]) for x in result.fetchall()]
        return dataset
    
@virtMachine.get('/{machine_id}', tags=TAG)
async def getMethod(machine_id: int):

    async with Session() as s0:

        controller = VirtualMachineController(s0)
        return await controller.get(machine_id)

@virtMachine.post('/', tags=TAG)
async def createMethod(item: VirtualMachineInit):
    
    async with Session() as s0:
        query = insert(VirtualMachine).values(
            **{
                key: value for key, value in item
            }
        ).returning(VirtualMachine.id)
        
        result = await s0.execute(query)
        await s0.commit()

        return {'Result': 'Created', 'id': result.fetchall()[0][0]}

@virtMachine.put('/{machine_id}', tags=TAG)
async def updateMethod(machine_id: int, item: VirtualMachineInit):
    
    async with Session() as s0:
        
        query = update(VirtualMachine).values(
            **{
                key: value for key, value in item
            }
        ).where(VirtualMachine.id==machine_id)
        
        result = await s0.execute(query)
        if result.rowcount==0:
            raise HTTPException(404)
        await s0.commit()
        return {'Result': 'Updated', 'id': machine_id}

@virtMachine.delete('/{machine_id}', tags=TAG)
async def deleteMethod(machine_id: int):

    async with Session() as s0:

        controller = VirtualMachineController(s0)
        await controller.delete(machine_id)
        return {"Result": "Delete"} 

@virtMachine.get('/{machine_id}/load', tags=TAG)
async def getLoad(machine_id: int):
    
    async with Session() as s0:
        
        query = select(VirtualMachine).where(VirtualMachine.id==machine_id)
        
        result = await s0.execute(query)
        dataset = [x for x in result.fetchall()]
        
        if dataset.__len__()==0:
            raise HTTPException(404)
        
        query = select(
            func.sum(Service.cpu).label('cpu'), 
            func.sum(Service.ram).label('ram')
            ).select_from(
                VirtualMachine
            ).where(
                VirtualMachine.id==machine_id, 
                Service.vm_id==VirtualMachine.id
            )
        result = await s0.execute(query)
        dataset = [Load.from_orm(x) for x in result.fetchall()]
        
        return dataset[0]