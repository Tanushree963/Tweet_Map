import dash
#from jobs import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output
import plotly.graph_objs as go


app = dash.Dash()

app.layout=html.Div([
    html.H1('Visualizing tweets by location'),
    html.Iframe(id='map',srcDoc=open('Tweet-Map.html','r').read(),width='100%',height='600')
])

if __name__ == '__main__':
    app.run_server(debug=True)
