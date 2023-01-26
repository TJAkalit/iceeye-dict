from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update

from staff.db import Session
from staff.datamodels import PhysicalMachineInit
from staff.dbmodels import PhysicalMachine

from .controller import PhysicalMachineController

physMachine = APIRouter()

TAG = ('Physical machine',)

@physMachine.get('/', tags=TAG)
async def getAllMethod():

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        return await controller.all()

@physMachine.get('/{machine_id}', tags=TAG)
async def getMethod(machine_id: int):

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        return await controller.get(machine_id)

@physMachine.post('/', tags=TAG)
async def createMethod(item: PhysicalMachineInit):
    
    async with Session() as s0:
        query = insert(PhysicalMachine).values(
            **{
                key: value for key, value in item
            }
        ).returning(PhysicalMachine.id)
        
        result = await s0.execute(query)
        await s0.commit()

        return {'Result': 'Created', 'id': result.fetchall()[0][0]}

@physMachine.put('/{machine_id}', tags=TAG)
async def updateMethod(machine_id: int, item: PhysicalMachineInit):
    
    async with Session() as s0:
        
        query = update(PhysicalMachine).values(
            **{
                key: value for key, value in item
            }
        ).where(PhysicalMachine.id==machine_id)
        
        result = await s0.execute(query)
        if result.rowcount==0:
            raise HTTPException(404)
        await s0.commit()
        return {'Result': 'Updated', 'id': machine_id}

@physMachine.delete('/{machine_id}', tags=TAG)
async def deleteMethod(machine_id: int):

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        await controller.delete(machine_id)
        return {"Result": "Delete"} 
