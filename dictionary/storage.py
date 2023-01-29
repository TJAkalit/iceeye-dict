from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, update, select

from staff.db import Session
from staff.datamodels import StorageInit, StorageItem, StorageType, PhysicalMachineItem
from staff.dbmodels import Storage, PhysicalMachine
from .controller import StorageControler

storage = APIRouter()

TAGS = ("Storage",)


@storage.get("/", tags=TAGS)
async def getAllMethod(machine_name: str = None):

    async with Session() as s0:

        query_0 = select(Storage).order_by(Storage.id)

        if machine_name:
            query_0 = query_0.filter(
                PhysicalMachine.name.like(machine_name + "%"),
                PhysicalMachine.id==Storage.pm_id,
            )

        result_0 = await s0.execute(query_0)
        dataset_0 = [StorageItem.from_orm(x[0]) for x in result_0.fetchall()]

        return dataset_0


@storage.get("/{obj_id}", tags=TAGS)
async def getMethod(obj_id: int):

    async with Session() as s0:

        query_0 = (
            select(Storage).where(Storage.id == obj_id)
        )

        result_0 = await s0.execute(query_0)
        rows = result_0.fetchall()
        if rows.__len__() == 0:
            raise HTTPException(404)
        row = rows[0]
        return StorageItem.from_orm(rows[0][0])


@storage.post("/", tags=TAGS)
async def createMethod(item: StorageInit):

    async with Session() as s0:

        query = (
            insert(Storage)
            .values(**{key: value for key, value in item if key != "type"})
            .values(type=StorageType(item.type).value)
            .returning(Storage.id)
        )
        result = await s0.execute(query)
        await s0.commit()

        return {"Result": "Created", "id": result.fetchall()[0][0]}


@storage.put("/{obj_id}", tags=TAGS)
async def updateMethod(obj_id: int, item: StorageInit):

    async with Session() as s0:

        query_0 = select(Storage).where(Storage.id == obj_id)
        result_0 = await s0.execute(query_0)
        dataset_0 = [None for _ in result_0.fetchall()]

        if dataset_0.__len__() == 0:
            raise HTTPException(404)
        
        query_1 = (
            update(Storage)
            .values(**{key: value for key, value in item if key != "type"})
            .values(type=StorageType(item.type).value)
            .where(Storage.id == obj_id)
        )

        result = await s0.execute(query_1)
        if result.rowcount == 0:
            raise HTTPException(404)
        await s0.commit()
        return {"Result": "Updated", "id": obj_id}


@storage.delete("/{obj_id}", tags=TAGS)
async def deleteMethod(obj_id: int):

    async with Session() as s0:

        query_0 = select(Storage).where(Storage.id == obj_id)
        result_0 = await s0.execute(query_0)
        dataset_0 = [None for _ in result_0.fetchall()]
        if dataset_0.__len__() == 0:
            raise HTTPException(404)

        await StorageControler(s0).delete(obj_id)
        return {"Result": "Deleted"}
