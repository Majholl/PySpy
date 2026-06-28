import random
from typing import Optional

from fastapi import FastAPI , WebSocket, status 
from fastapi import Response


from .utils import Notifall



app = FastAPI(redoc_url='/uidoc')



OwnerData = {
    'username':'nameless',
    'password':'nameless',
    'ownertoken':None}


GameRoom = {}



@app.get('/data')
async def GetData(token:str, response:Response) -> Optional[dict]:
    try:
        if token == OwnerData['ownertoken']:
            response.status_code = status.HTTP_200_OK
            data = {'settings': GameRoom[OwnerData['ownertoken']]['settings'],
                    'users': GameRoom[OwnerData['ownertoken']]['users']
                    }
            
            return {'Message': 'Data is ready.',
                    'data': data,}
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
        return None
     
     
     
     
     
@app.post('/auth/owner', status_code=status.HTTP_200_OK)
def LoginOwner(username:str , password:str, response:Response) -> dict:
    try:
        if OwnerData['username'] == username:
            
            if OwnerData['password'] == password:
                ownerToken = ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))
                OwnerData['ownertoken'] = ownerToken
                GameRoom[ownerToken] = {'settings':{'spycount':0, 'ownerplay':False},
                                        'users':{},
                                        'usersws':[],
                                        }
                GameRoom[OwnerData['ownertoken']]['users'][ownerToken] = username
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
    
    

     
@app.websocket('/ws/owner/{token}')
async def ConnectOwnner(websocket:WebSocket, token:str) -> list:
    try:
        if token in GameRoom:
            await websocket.accept()
            GameRoom[token]['usersws'].append(websocket)
            while True :
                data = await websocket.receive_json()     
        else:
            await websocket.close(1000, "Token does\'t match") 
                
    except Exception as err:
        print(f'Error found in websocket owner - {err}')
    
    
    
    
    
    
@app.post('/setting/spys/')
async def SpyCounts(token:str, count:int, response:Response) -> dict:
    try:
        if token == OwnerData['ownertoken']:
            if count and count !=0 :
                GameRoom[OwnerData['ownertoken']]['settings']['spycount'] = count
                response.status_code = status.HTTP_200_OK
    
                return {'Message':'Spy numbers set.',
                        'currentSettings':GameRoom[OwnerData['ownertoken']]['settings']
                    }
                 
            else :
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {'Message':'spy numbers must be greater then zero.',}        
        
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in SpyCounts - {err}')
    
    
    
    









@app.post('/setting/ownerin/')
async def OwnerIn(token:str, ownerin:bool, response:Response) -> dict:
    try:
        if token == OwnerData['ownertoken']:
            if ownerin :
                GameRoom[OwnerData['ownertoken']]['settings']['ownerplay'] = True
                response.status_code = status.HTTP_200_OK
                
                return {'Message':'Owner play status changed.',
                        'currentSettings':GameRoom[OwnerData['ownertoken']]['settings']}
            else :
                response.status_code = status.HTTP_400_BAD_REQUEST
                return {'Message':'set owner status to play or not',}        
        
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
    
    
        
    
    
    
    
    
@app.post('/join/user', status_code=status.HTTP_200_OK)
def JoinUser(username:str) -> dict:
    try :
        UserToken = ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))
        GameRoom[OwnerData['ownertoken']]['users'][UserToken]= username
        
        return {'Message':'User loged in successfully.',
                'username': username,
                'token':UserToken}
        
    except Exception as err :
        print(f'Error found in JoinUser - {err}')
    

    
        
    
@app.websocket('/ws/user/{token}')
async def ConnectUser(websocket:WebSocket, token:str) -> list:
    try:
        if token :
            
            if token in GameRoom[OwnerData['ownertoken']]['users'].keys():
                await websocket.accept()
                GameRoom[OwnerData['ownertoken']]['usersws'].append(websocket)
                
                
                msg = {'event':'New user joined.',
                            'username':GameRoom[OwnerData['ownertoken']]['users'][token],
                            'total':len(GameRoom[OwnerData['ownertoken']]['users'])
                        }
                
                await Notifall(msg , GameRoom[OwnerData['ownertoken']]['usersws'])
                
                while True :
                    data = await websocket.receive_json()     
            else:
                await websocket.close(1000, "Token does\'t match") 
   
        else :
            return {'Message':'Invalid token.',}
        
    except Exception as err:
        print(f'Error found in websocket users - {err}')
    
    
    
    
    
    
@app.post('/game/start')
async def StartGame(token:str, response:Response):
    try:
        if token == OwnerData['ownertoken']:
            
            msg = {'event':'Game is loading',}
            await Notifall(msg , GameRoom[OwnerData['ownertoken']]['usersws'])
                
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
        return None
     
    