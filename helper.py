import numpy as np 

def medal_tally(data):
    medal_tally = data.drop_duplicates(
        subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum(
    )[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Total'] = medal_tally['Total'].astype('int')
    return medal_tally

# For filtering according to country and year
def country_year_list(data):
    years = data['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    countries = np.unique(data['region'].dropna().values).tolist()
    countries.sort()
    countries.insert(0, 'Overall')

    return years, countries

def filter_medalTally(data, year, country):
    medal_data = data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_data = medal_data
    if year != 'Overall' and country == 'Overall':
        temp_data = medal_data[medal_data['Year'] == int(year)]
    if year == 'Overall' and country != 'Overall':
        flag=1
        temp_data = medal_data[medal_data['region'] == country]
    if year != 'Overall' and country != 'Overall':
        temp_data = medal_data[(medal_data['Year'] == int(year)) & (medal_data['region'] == country)]
    if flag == 1:
        temp_data = temp_data.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].reset_index()
    else:
        temp_data = temp_data.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    temp_data['Total'] = temp_data['Gold'] + temp_data['Silver'] + temp_data['Bronze']
    temp_data['Gold'] = temp_data['Gold'].astype('int')
    temp_data['Silver'] = temp_data['Silver'].astype('int')
    temp_data['Bronze'] = temp_data['Bronze'].astype('int')
    temp_data['Total'] = temp_data['Gold'] + temp_data['Silver'] + temp_data['Bronze']
    temp_data['Total'] = temp_data['Total'].astype('int')
    
    return temp_data

def data_over_time(data, col):
    df_over_time = data.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    return df_over_time

def mostSuccessfullAthlete_Sport(data, sport):
    mod_data = data.dropna(subset=['Medal'])

    if sport != 'Overall':
        mod_data = mod_data[mod_data['Sport'] == sport]

    mod_data = mod_data['Name'].value_counts().reset_index().head(10).merge(
        data, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    mod_data.rename(columns={'index':'Athlete Names', 'Name_x': 'Medals', 'region': 'Region'}, inplace=True)
    return mod_data 

def countryWiseAnalysis(data, country):
    mod_data = data.dropna(subset=['Medal']) # removing nan medals
    mod_data = mod_data.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal']) # remove duplicate team wins
    country_data = mod_data[mod_data['region'] == country]
    country_data = country_data.groupby('Year').count()['Medal'].reset_index()
    return country_data

def mostSuccessfullAthlete_Country(data, country):
    mod_data = data.dropna(subset=['Medal'])
    mod_data = mod_data[mod_data['region'] == country]
    mod_data = mod_data['Name'].value_counts().reset_index().head(10).merge(
        data, left_on='index', right_on='Name', how='left')[['index', 'Name_x', 'Sport']].drop_duplicates('index')
    mod_data.rename(columns={'index':'Athlete Names', 'Name_x': 'Medals', 'region': 'Region'}, inplace=True)
    return mod_data 

def male_vs_female(data):
    male = data[data['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    female = data[data['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    male_vs_female = male.merge(female, on='Year', how='left')
    male_vs_female.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    male_vs_female.fillna(0, inplace=True)
    return male_vs_female


