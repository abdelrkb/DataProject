from src.utils.clean_data import clean_data
import dash
from dash import html, dcc
import plotly.express as px

df = clean_data()

fig = px.line(df, x="date", y="hosp", title="Évolution des hospitalisations COVID-19")

app = dash.Dash(__name__)
app.layout = html.Div([
    html.H1("Dashboard COVID-19 France", style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
