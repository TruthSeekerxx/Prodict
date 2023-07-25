from Preprocessing import Preprocessing_data
import keras
from keras import layers
import pandas as pd

main_df = pd.read_csv('LoL_data_for_training',index_col= [0])

main_class = Preprocessing_data(main_df)

train_df_raw,test_df_raw = main_class.split_train_test_data(0.2)

dictionary_one_hot_encoding = main_class.get_dict_for_one_hot_encoding()

train_df_doubled = main_class.double_data_by_swapping_teams()

#train_df_permutated = main_class.get_permutations_of_each_team(0)

X_train,y_train = main_class.one_hot_encode_df(train_df_doubled)

X_test,y_test = main_class.one_hot_encode_df(test_df_raw)



#%%

model = keras.Sequential([
        layers.Dense(10,input_shape=(1650,), activation="relu", name="input_layer"),
        layers.Dropout(0.2),
        layers.Dense(10, activation="relu", name="hidden_layer_1"),
        layers.Dropout(0.2),
        layers.Dense(1,activation="sigmoid", name="output_layer")])


model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(X_train, y_train,validation_data=(X_test, y_test), epochs=50, batch_size=2)










