from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update

from staff.db import Session
from staff.datamodels import VirtualMachineInit
from staff.dbmodels import VirtualMachine

from .controller import VirtualMachineController

virtMachine = APIRouter()

TAG = ('Virtual machine',)

@virtMachine.get('/', tags=TAG)
async def getAllMethod():
    
    async with Session() as s0:
        
        controller = VirtualMachineController(s0)
        return await controller.all()
    
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
