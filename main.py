
from dataclasses import dataclass, field, fields
import dataclasses
from typing import List, Any

# numpy
import numpy as np


# load dash components
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash.dcc as dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly
import datetime


# Sidebar
from sidebar import sidebar

# filter
from scipy.signal import savgol_filter




class freemocap_app(object):


    def __init__(self):
        # css
        self.css_style_sheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
        self.app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP, self.css_style_sheet])
        self.sidebar =sidebar()
        self.content = html.Div(id="page-content", style=sidebar.CONTENT_STYLE)
        # html layout
        self._update_layout()
        # setup callback
        self._add_callbacks()


    def _update_layout(self):
        """update the layout for the app
        """
        self.app.layout = html.Div([dcc.Location(id="url"),
                                    self.sidebar.html(), self.content])

    def _add_callbacks(self) -> None:
        """add the callback function for the updating the figure
        """
        self.app.callback(Output("page-content", "children"),
                          [Input("url", "pathname")])(self._render_page_content)
        self.app.callback(Output('live-update-graph', 'figure'),
                          Input('interval-component', 'n_intervals'))(self._plot_3d_frame_data)
        self.app.callback(Output('live-update-acquisition-function', 'figure'),
                          Input('interval-component', 'n_intervals'))(self._plot_EI_frame_data)

    def _render_page_content(self,pathname:str) -> html.Div:
        """Render the page content based on the html path

        Args:
            pathname (str): html path

        Returns:
            dbc.Jumbotron: [html content]
        """
        if pathname == "/":
            return self._render_3d_home()
        elif pathname == "/page-1":
            return self._cost_function_settings()
        elif pathname == "/page-2":
            return html.P("Oh cool, this is page 2!")
        # If the user tries to reach a different page, return a 404 message
        return html.div([
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ])


    def _cost_function_settings(self) -> html.Div:
        # drop down menu to select the cost function
        cost_function = html.Div(
            html.Div([
                html.H1('Select cost function'),
                dcc.Dropdown(
                    id='cost-function',
                    options=[
                        {'label': 'Metabolic cost', 'value': 'Met'},
                        {'label': 'RMSSD', 'value': 'RMSSD'},
                        {'label': 'EMG', 'value': 'EMG'},
                    ],
                    value='Met'
                ),
            ])
        )
        graph = dcc.Graph(id='live-update-graph')
        return html.Div([cost_function, graph])

    def _render_3d_home(self) -> html.Div:
        """Render the 3d animation in the homepage

        Returns:
            html.Div: html division containing all the information
        """
        data = html.Div(
            html.Div([
                html.H1('Select cost function'),
                dcc.RadioItems(
                    id='cost-function',
                    options=[
                        {'label': 'Metabolic cost', 'value': 'Met'},
                        {'label': 'RMSSD', 'value': 'RMSSD'},
                        {'label': 'EMG', 'value': 'EMG'},
                    ],
                    value='Met'
                ),
                html.H4('Cost function'),
                html.Div(id='live-update-text'),
                dcc.Graph(id='live-update-graph'),
                html.H4('Acquisition function'),
                dcc.Graph(id='live-update-acquisition-function'),
                dcc.Interval(
                    id='interval-component',
                    interval=1000, # in milliseconds
                    n_intervals=0
                )
            ])
        )
        return data


    def _plot_EI_frame_data(self, n):
        data = {
            'time': [],
            'Latitude': [],
            'Longitude': [],
            'Altitude': []
        }

        # Collect some data
        for i in range(180):
            time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
            lon = np.random.randint(-180, 180)
            lat = np.random.randint(-90, 90)
            alt = np.random.randint(1, 10000)

            data['Longitude'].append(lon)
            data['Latitude'].append(lat)
            data['Altitude'].append(alt)
            data['time'].append(time)

        # Create the graph with subplots
        fig = make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
            'l': 30, 'r': 10, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

        fig.append_trace({
            'x': data['Longitude'],
            'y': data['Latitude'],
            'text': data['time'],
            'name': 'Longitude vs Latitude',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)

        return fig

    def _plot_3d_frame_data(self, n):
        data = {
            'time': [],
            'Latitude': [],
            'Longitude': [],
            'Altitude': []
        }

        # Collect some data
        for i in range(180):
            time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
            lon = np.random.randint(-180, 180)
            lat = np.random.randint(-90, 90)
            alt = np.random.randint(1, 10000)

            data['Longitude'].append(lon)
            data['Latitude'].append(lat)
            data['Altitude'].append(alt)
            data['time'].append(time)

        # Create the graph with subplots
        fig = make_subplots(rows=1, cols=1, vertical_spacing=0.2)
        fig['layout']['margin'] = {
            'l': 30, 'r': 10, 'b': 30, 't': 10
        }
        fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

        fig.append_trace({
            'x': data['time'],
            'y': data['Altitude'],
            'name': 'Altitude',
            'mode': 'lines+markers',
            'type': 'scatter'
        }, 1, 1)


        return fig


if __name__ == "__main__":
    freemocap_app().app.run_server(port=8888, debug =True)
    # freemocap_app()