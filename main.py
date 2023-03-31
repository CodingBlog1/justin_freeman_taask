#import Libraries
import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None


#Load the dataset
data = pd.read_csv("Play_By_Play_2018_2022.csv",encoding="ISO-8859-1",low_memory=False)
offensive_coordinator_df = pd.read_excel("Offensive Coordinators.xlsx")
data.drop("Unnamed: 0",axis=1,inplace=True)


'''1.You can eliminate all rows where 'play' does not equal 1 (this eliminates unhelpful plays)'''
df_usefull_player = data[data['play'] == 1]
df_usefull_player.reset_index(inplace=True)



'''2 . So what I'd like is to add a column to the play by play file above for "Pos_Offensive_Coordinator"
which will match the field 'posteam' to "Team" and the field 'season' to the corresponding column... 
this will tell us who the offensive coordinator was for each offense'''


for i, row in df_usefull_player.iterrows():
    if row['posteam'] in offensive_coordinator_df['Team'].values and row['season'] in list(df_usefull_player.season.unique()):
        df_usefull_player.loc[i,'Pos_Offensive_Coordinator'] = offensive_coordinator_df.loc[offensive_coordinator_df['Team'] == row['posteam'], row['season']].values[0]
# print("append")



'''3. Add another column called "Pos_Head_Coach" that points to either "home_coach" or "away_coach" based on whether "posteam_type" is home or away
If "posteam_type" = home, set "Pos_Head_Coach" to "home_coach"
If "posteam_type" = away, set "Post_Head_Coach" to "away_coach" '''

df_usefull_player['Pos_Head_Coach'] = df_usefull_player.apply(lambda x: x['home_coach'] if x['posteam_type'] == 'home' else x['away_coach'], axis=1)




'''4. Using data from current season (that is already known) + 2 former seasons, add a column called "Pos_OC_Pass_OE" and a column called "Pos_HC_Pass_OE"
 Example for value of "Pos_OC_Pass_OE" in week 5 of 2022, it should calculate based on all plays from season = 2021 (all weeks), season = 2020 (all weeks), and season = 2022 (weeks 1 through 4 only)
 Calculation for "Pos_OC_Pass_OE" sums "pass_oe" for the Offensive Coordinate (Pos_Offensive_Coordinator) over relevant sample divided by total number of plays
 Calculation for "Pos_HC_Pass_OE" sums "pass_oe" for the Offensive Coordinate (Pos_Head_Coach) over relevant sample divided by total number of plays'''




# define a function to calculate Pos_OC_Pass_OE for a given coach and week
def calc_pos_oc_pass_oe(coach, season, week):
    relevant_data = df_usefull_player[(df_usefull_player['Pos_Offensive_Coordinator'] == coach) & ((df_usefull_player['season'] == season) | (df_usefull_player['season'] == season-1)) & ((df_usefull_player['season'] < season) | (df_usefull_player['week'] < week))]
    pass_oe_sum = relevant_data['pass_oe'].sum()
    total_plays = relevant_data['pass_oe'].count()
    if total_plays == 0:
        return None
    else:
        return pass_oe_sum / total_plays

# define a function to calculate Pos_HC_Pass_OE for a given coach and week
def calc_pos_hc_pass_oe(coach, season, week):
    relevant_data = df_usefull_player[(df_usefull_player['Pos_Head_Coach'] == coach) & ((df_usefull_player['season'] == season) | (df_usefull_player['season'] == season-1)) & ((df_usefull_player['season'] < season) | (df_usefull_player['week'] < week))]
    pass_oe_sum = relevant_data['pass_oe'].sum()
    total_plays = relevant_data['pass_oe'].count()                                 
    if total_plays == 0:
        return None
    else:
        return pass_oe_sum / total_plays

# add the Pos_OC_Pass_OE and Pos_HC_Pass_OE columns to the dataset
df_usefull_player['Pos_OC_Pass_OE'] = df_usefull_player.apply(lambda row: calc_pos_oc_pass_oe(row['Pos_Offensive_Coordinator'], row['season'], row['week']), axis=1)
df_usefull_player['Pos_HC_Pass_OE'] = df_usefull_player.apply(lambda row: calc_pos_hc_pass_oe(row['Pos_Head_Coach'], row['season'], row['week']), axis=1)








'''5. Using data from current season (that is already known) + 2 former seasons, add a column called "Pos_OC_Success" and a column called "Pos_HC_Success"
 a. We will define success as the sum of 'success' column divided by number of plays'''



# define a function to calculate Pos_OC_Success for a given coach and week
def Pos_OC_Success(coach, season, week):
    relevant_data = df_usefull_player[(df_usefull_player['Pos_Offensive_Coordinator'] == coach) & ((df_usefull_player['season'] == season) | (df_usefull_player['season'] == season-1)) & ((df_usefull_player['season'] < season) | (df_usefull_player['week'] < week))]
    pass_oe_sum = relevant_data['success'].sum()
    total_plays = relevant_data['success'].count()
    if total_plays == 0:
        return None
    else:
        return pass_oe_sum / total_plays

# define a function to calculate Pos_HC_Success for a given coach and week
def Pos_HC_Success(coach, season, week):
    relevant_data = df_usefull_player[(df_usefull_player['Pos_Head_Coach'] == coach) & ((df_usefull_player['season'] == season) | (df_usefull_player['season'] == season-1)) & ((df_usefull_player['season'] < season) | (df_usefull_player['week'] < week))]
    pass_oe_sum = relevant_data['success'].sum()
    total_plays = relevant_data['success'].count()                                 
    if total_plays == 0:
        return None
    else:
        return pass_oe_sum / total_plays

# add the Pos_OC_Pass_OE and Pos_HC_Pass_OE columns to the dataset
df_usefull_player['Pos_OC_Success'] = df_usefull_player.apply(lambda row: Pos_OC_Success(row['Pos_Offensive_Coordinator'], row['season'], row['week']), axis=1)
df_usefull_player['Pos_HC_Success'] = df_usefull_player.apply(lambda row: Pos_HC_Success(row['Pos_Head_Coach'], row['season'], row['week']), axis=1)










'''6.Add a column called "Weather_Type" that takes the first part of the string from 'weather' field
Examples:
Clear
Rainy
Cloudy
Partly Cloudy
Etc.'''


def get_weather_type(row): 
    weather = row.split('Temp')[0]
    
    return weather

df_usefull_player['Weather_Type'] = df_usefull_player['weather'].apply(get_weather_type)




'''7. Add a column called "Implied_Home_Team_Total", "Implied_Away_Team_Total", "Implied_Pos_Team_Total" and "Implied_Def_Team_Total"
# Implied_Home_Team_Total = total_line/2 + spread_line
# Implied_Away_Team_Total = total_line/2 - spread_line
# Implied_Pos_Team_Total = either Implied_Home_Team_Total or Implied_Away_Team_Total based on whether 'posteam_type' = home or away



#----------------------------------------------------modified------------------------------------------------------------------------------
# For the implied totals that you created... i need to modify that formula
# Implied_Home_Team_Total = total_line/2 + spread_line/2
# Implied_Away_Team_Total = total_line/2 - spread_line/2 '''


df_usefull_player['Implied_Home_Team_Total'] = df_usefull_player['total_line']/2 + df_usefull_player['spread_line']/2
df_usefull_player['Implied_Away_Team_Total'] = df_usefull_player['total_line']/2 - df_usefull_player['spread_line']/2



# Modify Implied_Pos_Team_Total to be equal Implied_Home_Team_Total if posteam_type = home
# Modify Implied_Pos_Team_Total to b equal Implied_Away_Team_Total if posteam_type = away

df_usefull_player.loc[df_usefull_player['posteam_type'] == 'home', 'Implied_Def_Team_Total'] = df_usefull_player['Implied_Away_Team_Total']
df_usefull_player.loc[df_usefull_player['posteam_type'] == 'away', 'Implied_Def_Team_Total'] = df_usefull_player['Implied_Home_Team_Total']



'''8.Add a column called "Posteam_Spread" that returns spread_line if posteam_type = away or returns spread_line*-1 if posteam_type = home'''

df_usefull_player['Posteam_Spread'] = df_usefull_player['spread_line'] * df_usefull_player.apply(lambda x: 1 if x['posteam_type'] == 'away' else -1 ,axis=1) 


#drop the index column from the df_usefull_player 
df_usefull_player.drop('index',inplace=True,axis=1)

#save the df_usefull_player dataframe into csv file 
df_usefull_player.to_csv("play_play_final_.csv",index=False) 