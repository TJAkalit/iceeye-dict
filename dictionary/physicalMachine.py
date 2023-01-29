from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update, select, func

from staff.db import Session
from staff.datamodels import (
    PhysicalMachineInit,
    PhysicalMachineLoad,
    VirtualMachineItem,
    PhysicalMachineStorageSize,
    PhysicalMachineItem,
)
from staff.dbmodels import PhysicalMachine, VirtualMachine, Storage

from .controller import PhysicalMachineController

physMachine = APIRouter()

TAG = ("Physical machine",)


@physMachine.get("/", tags=TAG)
async def getAllMethod(name: str = None):

    async with Session() as s0:
        
        query = select(PhysicalMachine).order_by(PhysicalMachine.id)
        if name:
            query = query.filter(PhysicalMachine.name.like(name + '%'))
            
        result = await s0.execute(query)
        dataset = [PhysicalMachineItem.from_orm(x[0]) for x in result.fetchall()]
        return dataset


@physMachine.get("/{machine_id}", tags=TAG)
async def getMethod(machine_id: int):

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        return await controller.get(machine_id)


@physMachine.post("/", tags=TAG)
async def createMethod(item: PhysicalMachineInit):

    async with Session() as s0:
        query = (
            insert(PhysicalMachine)
            .values(**{key: value for key, value in item})
            .returning(PhysicalMachine.id)
        )

        result = await s0.execute(query)
        await s0.commit()

        return {"Result": "Created", "id": result.fetchall()[0][0]}


@physMachine.put("/{machine_id}", tags=TAG)
async def updateMethod(machine_id: int, item: PhysicalMachineInit):

    async with Session() as s0:

        query = (
            update(PhysicalMachine)
            .values(**{key: value for key, value in item})
            .where(PhysicalMachine.id == machine_id)
        )

        result = await s0.execute(query)
        if result.rowcount == 0:
            raise HTTPException(404)
        await s0.commit()
        return {"Result": "Updated", "id": machine_id}


@physMachine.delete("/{machine_id}", tags=TAG)
async def deleteMethod(machine_id: int):

    async with Session() as s0:

        controller = PhysicalMachineController(s0)
        await controller.delete(machine_id)
        return {"Result": "Delete"}
    
@physMachine.get('/storages/', tags=TAG)
async def getStorages():
    
    async with Session() as s0:
        
        query = select(
            PhysicalMachine.id.label('id'),  
            func.sum(Storage.size).label('size')    
        ).where(
            PhysicalMachine.id==Storage.pm_id
        ).group_by(
            PhysicalMachine.id
        )
        result = await s0.execute(query)
        dataset = [PhysicalMachineStorageSize.from_orm(x) for x in result.fetchall()]
        
        return dataset


@physMachine.get("/load/", tags=TAG)
async def getLoad(machine_id: int = 0):

    async with Session() as s0:
        
        q_size = select(
            Storage.pm_id.label('id'),
            func.sum(Storage.size).label('size'),
        ).group_by(
            Storage.pm_id
        ).cte('storage_size')
        
        query = (
            select(
                func.sum(VirtualMachine.cpu).label("cpu_sum"),
                func.sum(VirtualMachine.ram).label("ram_sum"),
                func.sum(VirtualMachine.size).label('virtual_machine_size'),
                q_size.c.size.label('storage_sum'),
                PhysicalMachine.id,
                PhysicalMachine.name,
                PhysicalMachine.cpu,
                PhysicalMachine.ram,
                func.coalesce(PhysicalMachine.cpu_multiply, 0).label("cpu_multiply"),
            )
            .select_from(PhysicalMachine)
            .where(
                VirtualMachine.pm_id == PhysicalMachine.id,
                Storage.pm_id==PhysicalMachine.id,
            )
            .join(q_size, (q_size.c.id==PhysicalMachine.id))
            .group_by(
                PhysicalMachine.id,
                PhysicalMachine.name,
                PhysicalMachine.cpu,
                PhysicalMachine.ram,
                q_size.c.size,
            )
            .order_by(PhysicalMachine.id)
        )

        if machine_id != 0:
            query = query.where(PhysicalMachine.id == machine_id)

        result = await s0.execute(query)
        dataset = [PhysicalMachineLoad.from_orm(x) for x in result.fetchall()]

        for item in dataset:

            query_0 = select(VirtualMachine).where(VirtualMachine.pm_id == item.id)
            result = await s0.execute(query_0)
            item.virtual_machines = [
                VirtualMachineItem.from_orm(x[0]) for x in result.fetchall()
            ]

        return dataset
