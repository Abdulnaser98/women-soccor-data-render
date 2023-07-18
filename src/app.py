import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html

color_legend_world_cup = {
    'Champion': 'blue',
    'Finalist': 'lightblue',
    'Semifinals': 'green',
    'Quarterfinals': 'lightgreen',
    '2nd Round': 'orange',
    '1nd Round': 'yellow'
}

color_legend_UEFA = {
    'Champion': 'blue',
    'Finalist': 'lightblue',
    'Semifinals': 'green',
    'Quarterfinals': 'lightgreen',
    'Group stage': 'orange',
}

color_legend_world_cup_men = {
    'Champion': 'blue',
    'Finalist': 'lightblue',
    'Semifinals': 'green',
    'Quarterfinals': 'lightgreen',
    '2nd Round': 'orange',
    '1nd Round': 'yellow'
}

df = pd.read_csv('results.csv')  # Replace 'results.csv' with the actual file path or DataFrame name
UEFA_women_transformed_data = pd.read_csv('UEFA_women_transformed_data.csv')
women_world_cup_transformed_data = pd.read_csv('world_cup_transformed_data.csv')
men_world_cup_transformed_data = pd.read_csv('men_world_cup_transformed_data.csv')



df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

teams = list(set(df['tournament'].unique()))
teams.sort(key=lambda x: (x != 'FIFA World Cup', x != 'UEFA Euro'))


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='tournament-dropdown',
            options=[{'label': team, 'value': team} for team in teams],
            value=None,
            placeholder='Select a tournament'
        ),
        html.Div(
            className='row',
            children=[

                        dcc.Graph(id='women_soccor_map',style={'display': 'inline-block'}),
                        dcc.Graph(id='men_soccor_map', style={'display': 'inline-block'}),
                    ]
        ),
        html.Div(
            className='row',
            children=[

                        dcc.Graph(id='women_hosting_countries',style={'display': 'inline-block'}),
                        dcc.Graph(id='men_hosting_countries', style={'display': 'inline-block'}),
                    ]
        ),
    ]

)


@app.callback(
    dash.dependencies.Output('women_soccor_map', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_women_soccor_map(selected_tournament):
    if selected_tournament == 'FIFA World Cup':
        fig = px.choropleth(women_world_cup_transformed_data, locations="Team", locationmode='country names',
                                color=women_world_cup_transformed_data['score'], hover_name="Team",
                                title='Color and Score', hover_data=['score'],
                                color_discrete_map=color_legend_world_cup)

        fig.update_layout(title='Countries Best results(Women)'.format(selected_tournament))

        return fig

    elif selected_tournament == 'UEFA Euro':
        fig = px.choropleth(UEFA_women_transformed_data, locations="Team", locationmode='country names',
                            color=UEFA_women_transformed_data['score'], hover_name="Team",
                            title='Color and Score', hover_data=['score'],
                            color_discrete_map=color_legend_UEFA)

        fig.update_layout(title='Countries Best results(Women)'.format(selected_tournament))
        return fig

    else:
        fig = px.choropleth(UEFA_women_transformed_data, locations="Team",title='Color and Score')
        fig.update_layout(title='Countries Best results(Women): There is no data yet :('.format(selected_tournament))
        return fig


@app.callback(
    dash.dependencies.Output('men_soccor_map', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_men_soccor_map(selected_tournament):

    if selected_tournament == 'FIFA World Cup':
        fig9 = px.choropleth(men_world_cup_transformed_data, locations="Team", locationmode='country names',
                    color=men_world_cup_transformed_data['score'], hover_name="Team",
                    title='Countries Best result(Men)', hover_data=['score'],
                    color_discrete_map=color_legend_world_cup_men)

        return fig9

    else:
        fig = px.choropleth(men_world_cup_transformed_data, locations="Team",
                             hover_name="Team",title='Color and Score')
        fig.update_layout(title='Countries Best result(Men): There is no data yet :('.format(selected_tournament))
        return fig




@app.callback(
    dash.dependencies.Output('women_hosting_countries', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_women_hosting_countries(selected_tournament):

        tournament_data = df[df['tournament'] == selected_tournament]
        d = tournament_data.groupby(['tournament', 'country', 'year']).size().reset_index()[['tournament', 'country', 'year']]
        d = d.groupby(['tournament', 'country']).size().reset_index()
        d.rename(columns={0: 'count'}, inplace=True)
        fig = px.choropleth(d, locations="country", locationmode='country names',
                                    hover_name="country", color="count",
                                    color_continuous_scale='RdBu')
        fig.update_layout(title='Hosting Countries(Women)'.format(selected_tournament))
        return fig


@app.callback(
    dash.dependencies.Output('men_hosting_countries', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_men_hosting_countries(selected_tournament):
    fig = px.choropleth(men_world_cup_transformed_data, locations="Team",
                             hover_name="Team",title='Color and Score')
    fig.update_layout(title='Hosting Countries(Men): There is no data yet :('.format(selected_tournament))
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

