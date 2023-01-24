from fastapi import FastAPI, Request, Response
from staff.password import decodeToken
from dictionary import dictionary

app = FastAPI()
app.include_router(dictionary, prefix='/dictionary')

# @app.middleware('http')
# async def secureUrls(request: Request, call_next):
    
#     response = await call_next(request)
    
#     try:
#         jwt = request.cookies.get('ie_a_main')
#         decoded = decodeToken(jwt)
#         print(decoded)
#     except:
        
#         response = Response(status_code=401)

#     return response