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
world_cup_transformed_data = pd.read_csv('world_cup_transformed_data.csv')
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
        dcc.Graph(id='map-first'),
        dcc.Graph(id='map-second')

    ]
)



@app.callback(
    dash.dependencies.Output('map-first', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_map_first(selected_tournament):

    print('selected_tournament')
    print(selected_tournament)
    if selected_tournament == 'FIFA World Cup':
        print("hellllllllllllo")
        print(world_cup_transformed_data.columns)

        fig2 = px.choropleth(world_cup_transformed_data, locations="Team", locationmode='country names',
                                color=world_cup_transformed_data['score'], hover_name="Team",
                                title='Color and Score', hover_data=['score'],
                                color_discrete_map=color_legend_world_cup)

        fig2.update_layout(title='Countries Best results(Women)'.format(selected_tournament))

        return fig2

    else:
        fig = px.choropleth(UEFA_women_transformed_data, locations="Team", locationmode='country names',
                            color=UEFA_women_transformed_data['score'], hover_name="Team",
                            title='Color and Score', hover_data=['score'],
                            color_discrete_map=color_legend_UEFA)

        fig.update_layout(title='Countries Best results'.format(selected_tournament))
        return fig




@app.callback(
    dash.dependencies.Output('map-second', 'figure'),
    [dash.dependencies.Input('tournament-dropdown', 'value')]
)
def update_map_second(selected_tournament):
        print('selected_tournament')
        print(selected_tournament)
        tournament_data = df[df['tournament'] == selected_tournament]

        filtered_data = pd.DataFrame(columns=['Country', 'total_times'])

        d = tournament_data.groupby(['tournament', 'country', 'year']).size().reset_index()[['tournament', 'country', 'year']]
        d = d.groupby(['tournament', 'country']).size().reset_index()
        d.rename(columns={0: 'count'}, inplace=True)

        fig_map = px.choropleth(d, locations="country", locationmode='country names',
                                hover_name="country", color="count",
                                color_continuous_scale='RdBu')

        fig_map.update_layout(title='Hosting Countries(Women)'.format(selected_tournament))
        return fig_map



if __name__ == '__main__':
    app.run_server(debug=True)

