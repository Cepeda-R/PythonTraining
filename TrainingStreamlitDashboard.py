import pandas as pd
import streamlit as st
import plotly.express as px

data = pd.read_csv('gdp.csv')

country = data['Country Name'].unique().tolist()

st.sidebar.title("Gross Domestic Product | GDP ")
st.sidebar.info(
    "GDP measures the monetary value of final"
    "goods and services produced in a country in a given period of time")
    

#Country #1
with st.sidebar:
    option_country_1 = st.selectbox(
        'WHAT COUNTRY DO YOU WANT TO KNOW?',
            country)

    data_filtered_table_1 = data[data['Country Name'].str.contains(option_country_1)]
    st.write(data_filtered_table_1)

#Country #2
    option_country_2 = st.selectbox(
        'WHAT COUNTRY DO YOU WANT TO COMPARE?',
            country)

    data_filtered_table_2 = data[data['Country Name'].str.contains(option_country_2)]
    st.write(data_filtered_table_2)

#Treat Data & Merge two countries for Data Analysis

#COUNTRY1

data_filtered_table_1_T = data_filtered_table_1.transpose()  

#using reset_index() to set index into column and remove year from there
data_filtered_table_1_T=data_filtered_table_1_T.reset_index()

data_filtered_table_1_T.rename(columns=data_filtered_table_1_T.iloc[0], inplace=True)

# Create a new column with index values
data_filtered_table_1_T['Year'] = data_filtered_table_1_T['Country Name']
data_filtered_table_1_T[option_country_1] = data_filtered_table_1_T[data_filtered_table_1_T.columns[1]]

# Remove first two rows
data_filtered_table_1_T = data_filtered_table_1_T.tail(-2)

# Retrieve only 2 treated columns
data_filtered_table_1_T = data_filtered_table_1_T[data_filtered_table_1_T.columns[1:3]]


# COUNTRY2

data_filtered_table_2_T = data_filtered_table_2.transpose()  

#using reset_index() to set index into column
data_filtered_table_2_T=data_filtered_table_2_T.reset_index()

data_filtered_table_2_T.rename(columns=data_filtered_table_2_T.iloc[0], inplace=True)

# Create a new column with index values
data_filtered_table_2_T['Year'] = data_filtered_table_2_T['Country Name']
data_filtered_table_2_T[option_country_2] = data_filtered_table_2_T[data_filtered_table_2_T.columns[1]]

# Remove first two rows
data_filtered_table_2_T = data_filtered_table_2_T.tail(-2)

# Retrieve only 2 treated columns
data_filtered_table_2_T = data_filtered_table_2_T[data_filtered_table_2_T.columns[1:3]]

#MERGE TWO COLUMNS - Year is the lock column
result = pd.merge(data_filtered_table_1_T, data_filtered_table_2_T, on = ['Year'])

#MELT Dataframe - Transform 2 columns into one - Right Configuration for Barcharts
result=pd.melt(result,id_vars=['Year'],var_name='Countries', value_name='GDP')

fig = px.bar(
    data_frame = result,
    x = 'Year',
    color = 'Countries',
    y = 'GDP',
    orientation = "v",
    barmode = 'group',
    title='GDP PERFORMANCE TREND BY COUNTRY',
    text_auto='.2s')

fig.update_traces(textfont_size=10, textangle=0, textposition="outside", cliponaxis=False)
#fig.show() for plotly directly

fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))

st.plotly_chart(fig)








