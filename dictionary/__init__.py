from fastapi import APIRouter, HTTPException
from staff.db import Session
from sqlalchemy import (
    select, insert, update, delete,
)
from staff.dbmodels import PhysicalMachine
from staff.datamodels import PhysicalMachineInit, PhysicalMachineItem
from .physMachine import PhysicalMachineController

dictionary = APIRouter()

@dictionary.get('/phys-machine')
async def getAllPhysM():

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        return await controller.all()

@dictionary.get('/phys-machine/{machine_id}')
async def getPhysM(machine_id: int):

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        return await controller.get(machine_id)

@dictionary.post('/phys-machine/')
async def createPhysM(item: PhysicalMachineInit):
    
    async with Session() as s0:
        query = insert(PhysicalMachine).values(
            **{
                key: value for key, value in item
            }
        ).returning(PhysicalMachine.id)
        
        result = await s0.execute(query)
        await s0.commit()

        return {'Result': 'Created', 'id': result.fetchall()[0][0]}
    
@dictionary.delete('/phys-machine/{machine_id}')
async def deletePhysM(machine_id: int):

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        await controller.delete(machine_id)
        return {"Result": "Delete"} 
