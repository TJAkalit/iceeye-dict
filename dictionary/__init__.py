from fastapi import APIRouter
from staff.db import Session
from .physicalMachine import physMachine
from .virtualMachine import virtMachine
from .service import service

dictionary = APIRouter()

dictionary.include_router(physMachine, prefix='/phys-machine' )
dictionary.include_router(virtMachine, prefix='/virt-machine' )
dictionary.include_router(service, prefix='/service' )