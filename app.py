import streamlit as st
import pandas as pd
import numpy as np
import preprocessor
import helper
import plotly.express as px
import plotly.figure_factory as ff


data = pd.read_csv('./dataset/athlete_events.csv')
reg_data = pd.read_csv('./dataset/noc_regions.csv')
reg_data = reg_data.drop('notes', axis=1)

data = preprocessor.preprocess(data, reg_data)
st.sidebar.image('https://static8.depositphotos.com/1006206/838/i/950/depositphotos_8388773-stock-photo-olympic-rings.jpg')
st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select An Option',
    ('Medal Table', 'Overall Analysis',
     'Country-wise Analysis', 'Athlete-wise Analysis')
)
if user_menu == 'Medal Table':
    years, countries = helper.country_year_list(data)
    st.sidebar.header('Medal Table')
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)
    medal_tally = helper.filter_medalTally(data, selected_year, selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Performance in Olympics")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Overall Performance in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title("Overall Performance of " + str(selected_country))
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(str(selected_year) + " Olympics")
        st.title(str(selected_country))

    st.table(medal_tally)

if user_menu == 'Overall Analysis':
    st.title("Overall Analysis")
    editions = data['Year'].unique().shape[0]-1
    cities = data['City'].unique().shape[0]
    sports = data['Sport'].unique().shape[0]
    events = data['Event'].unique().shape[0]
    athletes = data['Name'].unique().shape[0]
    nations = data['region'].unique().shape[0]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.subheader(editions)
    with col2:
        st.header("Cities")
        st.subheader(cities)
    with col3:
        st.header("Sports")
        st.subheader(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.subheader(events)
    with col2:
        st.header("Athletes")
        st.subheader(athletes)
    with col3:
        st.header("Nations")
        st.subheader(nations)
    
    nations_vs_time = helper.data_over_time(data, 'region')
    nations_vs_time.rename(columns={'index' : 'Edition', 'Year': 'Number of Countries'}, inplace=True)
    st.header('Nations participation over the years')
    fig1 = px.line(nations_vs_time, x="Edition", y="Number of Countries")
    st.plotly_chart(fig1)

    events_vs_time = helper.data_over_time(data, 'Event')
    events_vs_time.rename(columns={'index' : 'Edition', 'Year': 'Event'}, inplace=True)
    st.header('Events over the years')
    fig2 = px.line(events_vs_time, x="Edition", y="Event")
    st.plotly_chart(fig2)

    athletes_vs_time = helper.data_over_time(data, 'Name')
    athletes_vs_time.rename(columns={'index' : 'Edition', 'Year': 'Name'}, inplace=True)
    st.header('Athletes Participation over the years')
    fig3 = px.line(athletes_vs_time, x="Edition", y="Name")
    st.plotly_chart(fig3)

    st.title("Most Successful Athletes")
    sports_data = data['Sport'].unique().tolist()
    sports_data.sort()
    sports_data.insert(0, 'Overall')
    selected_sport = st.selectbox(
     'Select a Sport', sports_data)
    most_successful_athlete_data = helper.mostSuccessfullAthlete_Sport(data, selected_sport)
    st.table(most_successful_athlete_data)

if user_menu == 'Country-wise Analysis':
    st.title('Country-wise Medals Analysis')
    countries_data = np.unique(data['region'].dropna().values).tolist()
    countries_data.sort()
    selected_country = st.sidebar.selectbox('Select a Country', countries_data)
    st.header(selected_country)
    country_data = helper.countryWiseAnalysis(data, selected_country)
    fig = px.line(country_data, x="Year", y="Medal", title='Medal Tally')
    st.plotly_chart(fig)
    st.title("Top 10 Most Successful Athletes in " + selected_country)
    most_successful_athlete_data = helper.mostSuccessfullAthlete_Country(data, selected_country)
    st.table(most_successful_athlete_data)

if user_menu == 'Athlete-wise Analysis':
    st.title('Athlete-wise Medals Analysis')
    athlete_data = data.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_data['Age'].dropna()
    x2 = athlete_data[athlete_data['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_data[athlete_data['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_data[athlete_data['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medal', 'Silver Medal', 'Bronze Medal'], show_hist=False, show_rug=False)
    st.plotly_chart(fig)
    st.title('Male and Female Athletes over the years')
    male_vs_female = helper.male_vs_female(data)
    fig = px.line(male_vs_female, x="Year", y= ["Male", "Female"])
    st.plotly_chart(fig)


