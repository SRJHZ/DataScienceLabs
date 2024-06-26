# Import required libraries
import pandas as pd
#import dash
#import dash_html_components as html
#import dash_core_components as dcc
#previous 3 lines has been told to change into the following, due to the update of dash
from dash import dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                         {'label': 'CCAFS LC40', 'value': 'CCAFS LC40'},
                                         {'label': 'CCAFS SLC40', 'value': 'CCAFS SLC40'},
                                         {'label': 'KSC LC-39A', 'value': 'KSC LC39-A'},
                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                ],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True,
                                )),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, 
                                    max=10000, 
                                    step=1000,
                                    marks={0: '0', 2000: '2000', 4000: '4000', 6000: '6000', 8000: '8000', 10000: '10000'},
                                    value=[min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        site_counts = spacex_df['Launch Site'].value_counts().reset_index()
        site_counts.columns = ['Launch Site', 'count']
        site_counts['proportion'] = site_counts['count'] / site_counts['count'].sum()

        fig = px.pie(site_counts, values='proportion',
                     names='Launch Sites', 
                     title='Total Success Launches by Sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site] 
    
    fig = px.pie(filtered_df, values='class', 
                 names='class',  
                 title=f'Total Success Launches for site {entered_site}') 
    return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def update_graph(entered_site, payload_mass_range):
    filtered_df = spacex_df.copy()
    
    if entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]

    if payload_mass_range is not None:
        payload_min, payload_max = payload_mass_range
        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_min) 
        and (filtered_df['Payload Mass (kg)'] <= payload_max)] 

    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
                     color='Booster Version', title=f'Scatter plot for {entered_site}',
                     labels={'class': 'Mission Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'})

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
