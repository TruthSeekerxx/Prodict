import requests

class GatherData:
    
    def __init__(self,api_key,server):
        
        self.api_key = api_key
        self.server = server
        
    def gather_master_player_names(self):
        
        try:
            master_players_info = requests.get("https://euw1.api.riotgames.com/lol/league/v4/masterleagues/by-queue/RANKED_SOLO_5x5?api_key="+self.api_key).json()['entries']
        except:
            return 'ERROR'
        
        return [i['summonerName'] for i in master_players_info]
        
    def gather_puuids_by_name(self,names,max_number=5):

        all_player_puuids = []
        nr_of_errors = 0 #in case an error pops up-either non existant name or some other error on the api end

        for each_name in names[:max_number]:
            try:
                all_player_puuids.append(requests.get("https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+each_name+"?api_key="+self.api_key).json()['puuid'])
            except:
                nr_of_errors+=1
                
        return all_player_puuids
        
    def gather_match_history(self,puuids):
        
        #This list will include none too
        all_match_ids = []
        
        for each_puuid in puuids:
            all_match_ids.extend(requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/"+each_puuid+"/ids?start=0&count=100&api_key="+self.api_key).json())

        return all_match_ids
    
    def gather_ranked_database_for_ml(self,all_games):
        iteration_counter = 0
        nr_of_games = str(len(set(all_games)))
        all_data = [] #this is to be used for actual machine learning prediction
        
        for each_game in list(set(all_games)): #only unique games
            iteration_counter+=1
            print(str(iteration_counter)+' out of '+nr_of_games)
            try:
                full_single_game_info = requests.get("https://europe.api.riotgames.com/lol/match/v5/matches/"+each_game+"?api_key="+self.api_key).json()
            except:
                continue
                
            
            single_game_ml_data = []
            
            #try except in case some games are missing from the api
            try:
                if full_single_game_info['info']['queueId'] == 420:    #Only really care about the ranked games - in which queueId = 420
                    all_participants = full_single_game_info['info']['participants']
                    single_game_ml_data.append(all_participants[0]['win'])
                    for i in range(10):
                        single_game_ml_data.append(all_participants[i]['championId'])
                else:
                    print('not a ranked game')
                    continue
            except:
                continue
                    
            all_data.append(single_game_ml_data)
            
        
        return all_data
                
                
            
#%%




