from typing import Any
import jwt


class SigletonMeta(type):
    
    ises = {}
    
    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        
        if cls not in cls.ises:
            cls.ises[cls] = super().__call__(*args, **kwds)
        
        return cls.ises[cls]

class KeyVault(metaclass=SigletonMeta):
    
    openKey = None
    
    def __init__(self):
        
        with open('key.crt', 'rb') as file:
    
            self.openKey = file.read()

    @property
    def publicKey(self)-> bytes:
        
        return self.openKey

def encodeToken(payload: dict):
    
    return jwt.encode(
        payload=payload,
        key=KeyVault().privateKey,
        algorithm='RS256',
    )
    
def decodeToken(data: str):
    
    return jwt.decode(
        jwt=data,
        key=KeyVault().publicKey,
        algorithms=['RS256'],
        verify=True,
    )
