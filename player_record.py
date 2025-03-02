#save game record to back4app
#contribute from zorro
#https://dashboard.back4app.com/

import parse
import json
import requests
import pytz
from datetime import datetime

    
APP_ID = "royN65vTTmxskaiUFQpYsg9onPOvoyOgoHElyPy3"
REST_KEY = "BtjFNg4nos4XsnqsgCTfINVdK7migDbpFVuKpc6a"    
CLIENT_KEY="spXI8JzbtLdNUTuYNibHcjwH1r5NFkR4S7F8xrNn"

BASE_URL = "https://parseapi.back4app.com/classes/SoccerPlayers"
HEADERS = {
    "X-Parse-Application-Id": APP_ID,
    "X-Parse-REST-API-Key": REST_KEY,
    "Content-Type": "application/json"
}

#class Player(parse.ParseObject):
#    pass

#def saveRecord(player_name, player_score, game_level=0):
#    player = Player()
#    player.set('name', player_name)
#    player.set('score', player_score)
#    player.set('gameLevel', game_level)
#    player.set('cheatMode', False)
#    current_time = datetime.now(pytz.UTC)
#    print(current_time)
#    player.set('updateTime', current_time)
#    player.save()
    

#def queryRecord(player_name):
#    query = Player.query
#    query.equal_to('name', player_name)
#    players = query.find()
#    for player in players:
#        print(player.get('score'))
        
#another mode
def queryPlayer(player_name):
    header = {
        "X-Parse-Application-Id": APP_ID,
        "X-Parse-REST-API-Key": REST_KEY
    }    
    object_id = "IWakGxYcTD"
    url = BASE_URL+"/"+ object_id
    response = requests.get(url, headers=header)
    if (response.status_code == 200):
        print(response.json())   
    else:
        print(response)       
    return 100

def savePlayer(player_name, player_score, game_level=0):
    payload = {
        "playerName": player_name,
        "gameScore": player_score, 
        "gameLevel": game_level,
        "cheatMode": False}      

    print("HEADERS", HEADERS)
    print("BASE_URL", BASE_URL)
    print("json", json.dumps(payload))
    response = requests.post(BASE_URL, headers=HEADERS, json=payload)
    print(response.status_code, response.json())       