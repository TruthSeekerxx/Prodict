from data_gathering import GatherData
from keys import riot_api_key
import pandas as pd


main_class = GatherData(riot_api_key,'EUROPE')

master_player_names = main_class.gather_master_player_names()

master_player_puuids = main_class.gather_puuids_by_name(master_player_names,max_number=2000)

match_history_game_ids = main_class.gather_match_history(master_player_puuids)

basic_ml_data = main_class.gather_ranked_database_for_ml(match_history_game_ids)



ml_df =  pd.DataFrame(basic_ml_data,columns=['Win','Champion_0','Champion_1','Champion_2',
                                              'Champion_3','Champion_4','Champion_5',
                                              'Champion_6','Champion_7','Champion_8','Champion_9'])


ml_df.to_csv('LoL_data_for_training')