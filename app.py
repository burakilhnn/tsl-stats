import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
import streamlit as st
import base64

st.title('Turkish Super League Stats')

st.markdown("""
This app shows Turkish Super League matches stats from 1959 to 2020!
* **Data source:** [Turkish Super League Data](https://www.kaggle.com/faruky/turkish-super-league-matches-19592020).
""")

st.sidebar.header('Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1959,2021))))

def load_data(selected_year):
    df = pd.read_csv("../turkish-league-app/turkish_league.csv")
    selected_year = int(selected_year)
    filt = df['Season'] == selected_year
    df2 = df[filt]
    return df2

league_data = load_data(selected_year)

# Sidebar - Team selection
sorted_unique_team = sorted(league_data.Home.unique())
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

print(selected_team)

# Filtering data
df_selected_team = league_data[(league_data.Home.isin(selected_team)) | (league_data.Visitor.isin(selected_team))]

st.header('Display Match Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

team = df_selected_team.copy()
team['Results'] = ""
team_index = team.index

def result(df,indexes):
    for index in indexes:
        if df.loc[index,'Result'] == 'H':
            if df.loc[index,'Home'] == selected_team[0]:
                df.at[index,'Results'] = 'Win'
            else:
                df.at[index,'Results'] = 'Lose'
        elif df.loc[index,'Result'] == 'A':
            if df.loc[index,'Visitor'] == selected_team[0]:
                df.at[index,'Results'] = 'Win'
            else:
                df.at[index,'Results'] = 'Lose'
        else:
            df.at[index,'Results'] = 'Draw'
    return df

team = result(team,team_index)

if len(selected_team) == 1:
    if st.button('Team Statistics'):
        st.header(selected_team[0] + ' in '+str(selected_year)+'/'+str(selected_year+1)+' Season')
        with sns.axes_style("white"):
            f, ax = plt.subplots(figsize=(7, 5),dpi=200)
            ax = sns.countplot(team['Results'],palette='Set2')
        st.pyplot(f)
    