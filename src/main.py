import random, json
from typing import Optional
from os import path
from fastapi import FastAPI , WebSocket, status 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Response
import os

from .utils import Notifall



app = FastAPI(redoc_url='/uidoc')

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


OwnerData = {
    'username':'admin',
    'password':'admin',
    'ownertoken':None}


GameRoom = {}



@app.get('/data', tags=['admin'])
async def GetData(token:str, response:Response) -> Optional[dict]:
    try:
        if token == OwnerData['ownertoken']:
            response.status_code = status.HTTP_200_OK
            data = {'settings': GameRoom[OwnerData['ownertoken']]['settings'],
                    'users': [GameRoom[OwnerData['ownertoken']]['users'][i]['username'] for i in GameRoom[OwnerData['ownertoken']]['users']],
                    }
            
            return {'Message': 'Data is ready.',
                    'data': data,}
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
        return None
     
     
     
     
     
@app.post('/auth/owner', status_code=status.HTTP_200_OK, tags=['admin'])
async def LoginOwner(username:str , password:str, response:Response) -> dict:
    try:
        if OwnerData['username'] == username:
            
            if OwnerData['password'] == password:
                ownerToken = ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))
                OwnerData['ownertoken'] = ownerToken
                
                GameRoom[ownerToken] = {'settings':{'spycount':1, 'ownerplay':True , 'word':None},
                                        'users':{},
                                        }
                GameRoom[OwnerData['ownertoken']]['users'][ownerToken] = {'username': username, 'spy':False, 'admin':True, 'ws':None}
                
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
    
    
    
    

     
@app.post('/setting/spys/', tags=['admin'])
async def SpyCounts(token:str, count:int, response:Response) -> dict:
    try:
        if token == OwnerData['ownertoken']:
            if count and count !=0 :
                
                if count > len(GameRoom[OwnerData['ownertoken']]['users']):
                    return {'Message':'spies must be less than users',}    
                
                    
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
    
    
    
    
@app.post('/setting/ownerin/', tags=['admin'])
async def OwnerPlay(token:str, ownerin:bool, response:Response) -> dict:
    try:
        if token == OwnerData['ownertoken']:
            if ownerin :
                GameRoom[OwnerData['ownertoken']]['settings']['ownerplay'] = True
                response.status_code = status.HTTP_200_OK
            else:
                GameRoom[OwnerData['ownertoken']]['settings']['ownerplay'] = False
                response.status_code = status.HTTP_200_OK
                
            return {'Message':'Owner play status changed.',
                    'currentSettings':GameRoom[OwnerData['ownertoken']]['settings']}
            
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
    
    
    
    
    
    
@app.post('/setting/word/', tags=['admin'])
async def OwnerWord(token:str, word:str, response:Response) -> dict:
    try:
        if token == OwnerData['ownertoken']:
            
            GameRoom[OwnerData['ownertoken']]['settings']['word'] = word
            response.status_code = status.HTTP_200_OK
        
            return {'Message':'Owner play status changed.',
                    'currentSettings':GameRoom[OwnerData['ownertoken']]['settings']}
            
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
    
      
      
      
      
            
   
@app.websocket('/ws/owner/{token}')
async def ConnectOwnner(websocket:WebSocket, token:str) -> list:
    try:
        if token in GameRoom:
            await websocket.accept()
            GameRoom[token]['users'][token]['ws'] = websocket
           
            while True :
                data = await websocket.receive_json()     
        else:
            await websocket.close(1000, "Token does\'t match") 
                
    except Exception as err:
        print(f'Error found in websocket owner - {err}')
    
    
    
        
    
    
    
    
    
    
@app.post('/join/user', status_code=status.HTTP_200_OK, tags=['user'])
async def JoinUser(username:str) -> dict:
    try :
        UserToken = ''.join(random.choice(["0","1","2","3","4","5","6","7","8","9"]) for _ in range(6))
        GameRoom[OwnerData['ownertoken']]['users'][UserToken]= {'username': username, 'spy':False, 'admin':False, 'ws':None}
        
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
                GameRoom[OwnerData['ownertoken']]['users'][token]['ws'] = websocket
                
                
                msg = {'event':'New user joined.',
                            'username':GameRoom[OwnerData['ownertoken']]['users'][token]['username'],
                            'total':len(GameRoom[OwnerData['ownertoken']]['users'])
                        }
                
                userslist = [GameRoom[OwnerData['ownertoken']]['users'][i]['ws'] for i in GameRoom[OwnerData['ownertoken']]['users'].keys()]
                
                await Notifall(msg ,userslist)
                
                while True :
                    data = await websocket.receive_json()     
                    
            else:
                await websocket.close(1000, "Token does\'t match") 
   
        else :
            return {'Message':'Invalid token.',}
        
    except Exception as err:
        print(f'Error found in websocket users - {err}')
    
    
    
    
    
    
    
    
    
    
    
@app.post('/game/start', tags=['Game behavior'])
async def StartGame(token:str, response:Response):
    try:
        if token == OwnerData['ownertoken']:
            
            users = [i for i in GameRoom[OwnerData['ownertoken']]['users'].keys()]
            spycounts = int(GameRoom[OwnerData['ownertoken']]['settings']['spycount'])
            ownerplay = GameRoom[OwnerData['ownertoken']]['settings']['ownerplay']
            ownerword = GameRoom[OwnerData['ownertoken']]['settings']['word']
            
            wordspath = path.join(os.getcwd(), 'words.json')
            
            for i in users:
                GameRoom[OwnerData['ownertoken']]['users'][i]["spy"] = False
            
            if not path.exists(wordspath) :
                return {'Message':'Words path does\'nt exists.',}
            
           
            with open(wordspath, 'r') as f :
                words = json.load(f)    
                selectedWord = random.choice(words['words'])
        
            if not ownerplay :
                selectedWord = ownerword
                users.remove(OwnerData['ownertoken'])
                       
            if len(users) > 0 :
                spys = random.choices(users, k= spycounts)
                for i in spys:
                    GameRoom[OwnerData['ownertoken']]['users'][i]["spy"] = True


            spyeisList = []
            othersList = []
            
            for i in users:
                if GameRoom[OwnerData['ownertoken']]['users'][i]["spy"] == True :
                    spyeisList.append(GameRoom[OwnerData['ownertoken']]['users'][i]["ws"])
                else :
                    othersList.append(GameRoom[OwnerData['ownertoken']]['users'][i]["ws"])
                    

            msgusers = {'event':'Game is loading', 'data':selectedWord}
            await Notifall(msgusers , othersList)
            msgspyies = {'event':'Game is loading', 'data':'You are spy'}
            await Notifall(msgspyies , spyeisList)          
    
                    
            return {'Message':'Game is loading.',}    
        
            
            
        else :
            
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exists.',}
               
    except Exception as err:
        print(f'Error found in OwnerIn - {err}')
        return None
     
     
     
     
     
     
     
     
     
     

@app.post('/game/end', tags=['Game behavior'])
async def EndGame(token:str , response:Response) -> dict:
    try:
        if token == OwnerData['ownertoken']:
            users = [i for i in GameRoom[OwnerData['ownertoken']]['users'].keys()]
            
            for i in users:
                await GameRoom[OwnerData['ownertoken']]['users'][i]['ws'].close()

            GameRoom.clear()
            return {'Message':'The Game closed.',}
        
        else :
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {'Message':'the token does\'nt exits.',}
                    
    except Exception as err:
        print(f'Error found in EndGame - {err}')
        return None
     
    
    
    