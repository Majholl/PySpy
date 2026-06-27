import random

from fastapi import FastAPI , WebSocket, status 
from fastapi import Response


app = FastAPI(redoc_url='/uidoc')

OwnerData = {
    'username':'nameless',
    'password':'nameless',
    'ownertoken':None}

GameRoom = {}
UserWs = []


@app.post('/auth/owner', status_code=status.HTTP_200_OK)
def LoginOwner(username:str , password:str, response:Response) -> dict:
    try:
        if OwnerData['username'] == username:
            
            if OwnerData['password'] == password:
                ownerToken = ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))
                OwnerData['ownertoken'] = ownerToken
                GameRoom[ownerToken] = {}
                response.status_code = status.HTTP_200_OK
                return {'Message':'Owner loged in successfully.',
                        'username': username,
                        'token':ownerToken}
                
            else :
                response.status_code = status.HTTP_404_NOT_FOUND
                return {'Message':'Wrong password',}
            
        
        else :
            response.status_code =  status.HTTP_404_NOT_FOUND
            return {'Message':'User not found.',}
        
    
    except Exception as err :
        print(f'Error found in LoginOwner - {err}')
    
    
    
    
    
    
    
@app.post('/join/user', status_code=status.HTTP_200_OK)
def JoinUser(username:str) -> dict:
    try :
        UserToken = ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))
        GameRoom[OwnerData['ownertoken']][UserToken] = username
        print(GameRoom)
        return {'Message':'User loged in successfully.',
                'username': username,
                'token':UserToken}
        
    except Exception as err :
        print(f'Error found in JoinUser - {err}')
    



     
        
    
@app.websocket('/ws/owner/{token}')
async def ConnectOwnner(websocket:WebSocket, token:str):
    try:
        if token in GameRoom:
            await websocket.accept()
            UserWs.append(websocket)
            while True :
                data = await websocket.receive_json()     
                 
    except Exception as err:
        print(f'Error found in JoinUser - {err}')
    
    
    
        
        
    
@app.websocket('/ws/user/{token}')
async def ConnectUser(websocket:WebSocket, token:str) -> list:
    try:
        if token :
            
            if token in GameRoom[OwnerData['ownertoken']].keys():
                await websocket.accept()
                UserWs.append(websocket)
                await Notifall({'event':'new user joined',
                            'username':GameRoom[OwnerData['ownertoken']][token],
                            'total':len(GameRoom[OwnerData['ownertoken']])}, UserWs)
                while True :
                    data = await websocket.receive_json()      
        else :
            return {'Message':'Invalid token.',}
        
    except Exception as err:
        print(f'Error found in JoinUser - {err}')
    
    
    
    
async def Notifall(msg: dict, users: list):
    for ws in users:
        try:
            await ws.send_json(msg)
        except:
            pass