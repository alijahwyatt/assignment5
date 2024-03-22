# %% [markdown]
# ### Assignment #4: Basic UI
# 
# DS4003 | Spring 2024
# 
# Objective: Practice buidling basic UI components in Dash. 
# 
# Task: Build an app that contains the following components user the gapminder dataset: `gdp_pcap.csv`. [Info](https://www.gapminder.org/gdp-per-capita/)
# 
# UI Components:
# A dropdown menu that allows the user to select `country`
# -   The dropdown should allow the user to select multiple countries
# -   The options should populate from the dataset (not be hard-coded)
# A slider that allows the user to select `year`
# -   The slider should allow the user to select a range of years
# -   The range should be from the minimum year in the dataset to the maximum year in the dataset
# A graph that displays the `gdpPercap` for the selected countries over the selected years
# -   The graph should display the gdpPercap for each country as a line
# -   Each country should have a unique color
# -   Graph DOES NOT need to interact with dropdown or slider
# -   The graph should have a title and axis labels in reader friendly format  
# 
# Layout:  
# - Use a stylesheet
# - There should be a title at the top of the page
# - There should be a description of the data and app below the title (3-5 sentences)
# - The dropdown and slider should be side by side above the graph and take up the full width of the page
# - The graph should be below the dropdown and slider and take up the full width of the page
# 
# Submission: 
# - There should be only one app in your submitted work
# - Comment your code
# - Submit the html file of the notebook save as `DS4003_A4_LastName.html`
# 
# 
# **For help you may use the web resources and pandas documentation. No co-pilot or ChatGPT.**

# %%
# imports
from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px

# %%
# read in dataset and look at head

df = pd.read_csv("gdp_pcap.csv")
df.head()

# %%
# load the CSS stylesheet
stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# %%
# initialize the app
app = Dash(__name__, external_stylesheets=stylesheets)

# %%
#clean the data
#create year column
df = df.melt(id_vars='country',
             var_name='year',
             value_name='gdp_per_capita')
#remove k in values, using scientific notation
df['gdp_per_capita'] = df['gdp_per_capita'].replace({'k': '*1e3'}, regex=True)

#converting year and gdp to numeric
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['gdp_per_capita'] = pd.to_numeric(df['gdp_per_capita'], errors='coerce')


# %%
#create layout 
app.layout = html.Div([
    #add title and description
    html.H2("Countries' GDP Per Capita by Year"),
    html.H5('The app looks at the GDP Per Capita by year for different countries. The data comes from gapminder dataset and the app allows users to select the country and year of their choice to look at GDP per capita. The app includes a dropdown menu, slider, and displays a graph of the GDP per capita for the selected countries over the selected years.'),
    
    html.Div([
        html.Div([
            # create dropdown menu to select countries
            html.Label('Select Countries'),
            dcc.Dropdown(
                df.country.unique(),
                id='country-dropdown',
                #initializing with first two countries
                value = ['Afghanistan', 'Angola'],
                placeholder='Select Countries',
                multi=True
            ),
        ],
         #changing format
          style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'}),
        
        html.Div([
            # create slider to select year
            dcc.RangeSlider(
               min=df['year'].min(),
               max=df['year'].max(),
               step=None,
               #initialize year silder 
               value=[1800, 1850],
               id='year-range-slider',
               #setting marks in increments of 50 instead of hard coding marks
               marks={str(year): str(year) for year in range(df['year'].min(), df['year'].max() + 1, 50)}
            ) , 
        ],
        #changing format
          style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'bottom'})
        ]),
        #gcp per capita graph
        dcc.Graph(
        id='gdp-per-capita-graph',
        #melt df to create varaible name for year
        figure=px.line(df.melt(id_vars='country', var_name='year', value_name='gdpPercap'), 
                       #x axis as year, y axis as gdp per capita, and set color to country
                       x='year', 
                       y='gdpPercap', 
                       color='country', 
                       markers=True)
                .update_layout(
                    title='GDP per Capita Over Time for Selected Countries',
                    xaxis_title='Year',
                    yaxis_title='GDP per Capita'
                )
    )

        
    ])

#define callbacks
@app.callback(
    Output('gdp-per-capita-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
#create update graph function
def update_graph(selected_countries, selected_years):

    # create filtered df based on selected countries and years
    filtered_df = df[(df['country'].isin(selected_countries)) & (df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]

    # making graph
    fig = px.line(filtered_df,
                       #set x axis to year, y axis to gdp, color to country
                       x='year', 
                       y='gdp_per_capita', 
                       title='GDP per Capita Over Time for Selected Countries',
                       color='country', 
                       markers=True)
    #create titles 
    fig.update_layout(
                    title='GDP per Capita Over Time for Selected Countries',
                    xaxis_title='Year',
                    yaxis_title='GDP per Capita',
                )
    return fig  
#run app
if __name__ == '__main__':
    app.run_server(debug=True) 


