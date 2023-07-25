import pandas as pd
from keras.utils import to_categorical
import numpy as np
import random
import itertools


class Preprocessing_data:
    
    def __init__(self,main_df):
        self.main_df = main_df
    
    """
    Splits the data BEFORE any data manipulation and argumentation for proper testing data
    """
    def split_train_test_data(self,ratio):
        self.train_df = self.main_df.sample(frac = 1-ratio)
        self.test_df = self.main_df.drop(self.train_df.index)
        return (self.train_df,self.test_df)
    
    """
    For each champion Id you will get hot encoded values (dictionary output)
    """
    def get_dict_for_one_hot_encoding(self):
        #list of all unique champions in whole dataframe
        unique_champions = pd.unique(self.main_df.drop('Win',axis=1).values.ravel('K'))
        unique_champions_categorical = to_categorical(unique_champions)
        hot_encoded_champions = np.unique(unique_champions_categorical,axis=1)

        #dictionary for encoding and decoding (one hot encoding)
        self.dict_for_encoding_champion_ids = dict(zip(unique_champions,hot_encoded_champions))
        
        return self.dict_for_encoding_champion_ids

    def double_data_by_swapping_teams(self):
        #We can double the data by flipping the win column +(swapping first 5 champions with the last 5 champions)
        flipped_train_df = pd.DataFrame({'Win':~self.train_df['Win'],
                                       'Champion_0':self.train_df['Champion_5'],
                                       'Champion_1':self.train_df['Champion_6'],
                                       'Champion_2':self.train_df['Champion_7'],
                                       'Champion_3':self.train_df['Champion_8'],
                                       'Champion_4':self.train_df['Champion_9'],
                                       'Champion_5':self.train_df['Champion_0'],
                                       'Champion_6':self.train_df['Champion_1'],
                                       'Champion_7':self.train_df['Champion_2'],
                                       'Champion_8':self.train_df['Champion_3'],
                                       'Champion_9':self.train_df['Champion_4']})

        self.train_df_doubled = pd.concat([self.train_df,flipped_train_df],ignore_index=True)
        
        return self.train_df_doubled
    
    """
    This data argumentation removes the order of each champion position.
    But it increases the amount of data by a lot.
    Need to pass a parameter of how many permutations for each team.
    Eg. 7 permutations of a team is equal to 49 random permutations of a game (2 teams is 7*7=49)
    There are 14400 permutations of a single game, so we pick few random ones.
    """
    def get_permutations_of_each_team(self,permut):
        first_team_df = self.train_df_doubled[['Champion_0','Champion_1','Champion_2','Champion_3','Champion_4']]
        second_team_df = self.train_df_doubled[['Champion_5','Champion_6','Champion_7','Champion_8','Champion_9']]
        result = list(self.train_df_doubled['Win'].astype(int))
        
        permutation_result = []

        for each_result in result:
            for n in range(permut*permut):
                permutation_result.append([each_result])
                
        print(len(permutation_result))


        first_team_single_game = list(first_team_df.iloc[0])
        second_team_single_game = list(second_team_df.iloc[0])
        all_game_permutations = []

        for i in range(len(first_team_df)):
            first_team_single_game = list(first_team_df.iloc[i])
            second_team_single_game = list(second_team_df.iloc[i])
            new_data_for_first_game = []
            
            first_team_all_permutation = list(itertools.permutations(first_team_single_game))
            for each_permutation in random.choices(first_team_all_permutation, k =permut):
                second_team_all_permutation = list(itertools.permutations(second_team_single_game))
                for each_nd_permutation in random.choices(second_team_all_permutation,k=permut):
                    new_data_for_first_game.append(each_permutation+each_nd_permutation)
            all_game_permutations.extend(new_data_for_first_game)
            
        
        permutation_result = np.array(list(permutation_result))
        all_game_permutations = np.array(all_game_permutations)

        train_array_doubled_permutated = np.concatenate((permutation_result, all_game_permutations),axis=1)

        self.train_df_doubled_permutated = pd.DataFrame(train_array_doubled_permutated,columns=['Win','Champion_0','Champion_1','Champion_2',
                                                      'Champion_3','Champion_4','Champion_5',
                                                      'Champion_6','Champion_7','Champion_8','Champion_9'])
        
        return self.train_df_doubled_permutated
    
    """
    Hot encoding increases the memory requirements by quite a bit
    Returns training dataset.
    """
    def one_hot_encode_df(self, main_data):
        
        y = main_data['Win'].astype(int)
        X = main_data.drop('Win',axis=1).astype(int)


        #hot encode data-map it to previous dictionary for encoding
        for each_column in X.columns:
            X[each_column] = X[each_column].map(self.dict_for_encoding_champion_ids)

        X = np.array(X)
        y = np.array(y)

        #Put it in correct data format for the neural network
        all_data = []

        for i in range(len(X)):
            X_single_piece_of_data = []
            for j in range(10):
                X_single_piece_of_data.extend(X[i][j])
            all_data.append(X_single_piece_of_data)

        X = np.array(all_data)
        X = X.astype(int)
        
        return (X,y)

