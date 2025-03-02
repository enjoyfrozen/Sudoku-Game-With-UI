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

BASE_URL = "https://parseapi.back4app.com/SoccerPlayers"
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
    headers = {
        'X-Parse-Application-ID': APP_ID,
        'X-Parse-REST-API-Key': REST_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.get('https://parseapi.back4app.com/parse/classes/player', headers=headers)
    print(response.status_code, response.json())   
    return 100

def savePlayer(player_name, player_score, game_level=0):
    data = {
        "playerName": player_name,
        "yearOfBirth": 1997,
        "emailContact": "a.wed@email.io",
        "score": player_score, 
        "gameLevel": game_level,
        "cheatMode": False}
        
    payload = {
        "title": player_name,
        "player_score": player_score
    }
    print("HEADERS", HEADERS)
    print("BASE_URL", BASE_URL)
    print("data", json.dumps(data))
    print("json", json.dumps(payload))
    response = requests.put(BASE_URL, headers=HEADERS, json=json.dumps(payload))
    print(response.status_code, response.json())       