from dash import html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd
from config import CONFIG

df = pd.read_csv(CONFIG["DATA_PATH"]["CLEANED"], sep=",")

# Layout du composant
hospitalisation_component = html.Div([
    html.H3("Évolution des hospitalisations COVID-19 par région", style={'textAlign': 'center'}),

    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': reg, 'value': reg} for reg in sorted(df['lib_reg'].unique())],
        value='Île-de-France',
        clearable=False,
        style={'width': '60%', 'margin': 'auto'}
    ),

    dcc.Graph(id='hospitalisation-graph')
])

@callback(
    Output('hospitalisation-graph', 'figure'),
    Input('region-dropdown', 'value')
)
def update_hospitalisation_graph(selected_region):
    # Filtrer sur la région
    filtered_df = df[df['lib_reg'] == selected_region]

    aggregated = (
        filtered_df.groupby('date', as_index=False)[['hosp']]
        .sum()
    )

    fig = px.line(
        aggregated,
        x='date',
        y='hosp',
        title=f"Hospitalisations COVID-19 — {selected_region}",
        labels={'hosp': 'Patients hospitalisés', 'date': 'Date'},
        template='plotly'
    )
    fig.update_layout(title_x=0.5)
    return fig

