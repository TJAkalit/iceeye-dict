from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update

from staff.db import Session
from staff.datamodels import ServiceInit
from staff.dbmodels import Service

from .controller import ServiceController

service = APIRouter()

TAG = ('Service',)

@service.get('/', tags=TAG)
async def getAllMethod():

    async with Session() as s0:

        controller = ServiceController(s0)
        return await controller.all()

@service.get('/{machine_id}', tags=TAG)
async def getMethod(machine_id: int):

    async with Session() as s0:

        controller = ServiceController(s0)
        return await controller.get(machine_id)
    
@service.post('/', tags=TAG)
async def createMethod(item: ServiceInit):
    
    async with Session() as s0:
        query = insert(Service).values(
            **{
                key: value for key, value in item
            }
        ).returning(Service.id)
        
        result = await s0.execute(query)
        await s0.commit()

        return {'Result': 'Created', 'id': result.fetchall()[0][0]}
    
@service.put('/{machine_id}', tags=TAG)
async def updateMethod(machine_id: int, item: ServiceInit):
    
    async with Session() as s0:
        
        query = update(Service).values(
            **{
                key: value for key, value in item
            }
        ).where(Service.id==machine_id)
        
        result = await s0.execute(query)
        if result.rowcount==0:
            raise HTTPException(404)
        await s0.commit()
        return {'Result': 'Updated', 'id': machine_id}

@service.delete('/{machine_id}', tags=TAG)
async def deleteMethod(machine_id: int):

    async with Session() as s0:

        controller = ServiceController(s0)
        await controller.delete(machine_id)
        return {"Result": "Delete"} 
