from fastapi import FastAPI, Request, Response
from staff.password import decodeToken
from dictionary import dictionary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(dictionary, prefix='/api/dictionary')

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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