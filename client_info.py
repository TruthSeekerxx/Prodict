import re
import os
import requests
import psutil
import time


def check_client():
    game_open = "LeagueClient.exe" in (i.name() for i in psutil.process_iter())
    if game_open==False:
        check_client.yo='Client not open'
    else:
        check_client.yo='Client open'



def get_passwords():
    try:
        #This gets necessary information automatically to use requests.
        x = os.popen("wmic PROCESS WHERE name='LeagueClientUx.exe' GET commandline")
        text = x.read()
        match_id = re.search(r'--app-port=\w\w\w\w\w', text)
        port = match_id.group()[-5:]
        match_token = re.search(r'--remoting-auth-token=\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S\S', text)
        match_token_id = match_token.group()[22:]
        
        
        r = requests.get('https://127.0.0.1:'+port+'/lol-champ-select/v1/session', auth=('riot',match_token_id), verify=('C:\\Users\\user\\.spyder-py3\\riotgames.pem'))
        get_passwords.mydict = r.json()
    except:
        print('trying again...')
        time.sleep(1)
        get_passwords()


def check_Cselect():
    if get_passwords.mydict.get('httpStatus')!=None:
        check_Cselect.yo='Not in champion select'
    else:
        check_Cselect.yo='In champion select'



def lookup_teams():
    lookup_teams.myTeam = []
    lookup_teams.theirTeam = []
    for each in range(5):
        ids = get_passwords.mydict['myTeam'][each]['championId']
        lookup_teams.myTeam.append(ids)
        ids_2 = get_passwords.mydict['theirTeam'][each]['championId']
        lookup_teams.theirTeam.append(ids_2)


