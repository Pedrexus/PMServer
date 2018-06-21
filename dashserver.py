# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 23:44:30 2018

@author: Pedro
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import nist_partition as NP

def generate_table(dataframe, max_rows=10):
    return html.Table( 
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

app = dash.Dash()

app.layout = html.Div([
    html.H4(children='Partition Matrix Table'), 
           
    dcc.Input(id='elements', value='Ca II, Fe I', type='text'),
    dcc.Input(id='temps', value='0.7, 0.6', type='text'),
    html.Div(id='table-container'),
    
])

@app.callback(
    Output('table-container', 'children'),
    [Input(component_id='elements', component_property='value'),
     Input('temps', 'value')]
)
def update_table(elements, temps):
    elements = elements.split(',')
    temps = temps.split(',')
    df = NP.partition_matrix(elements, temps)
    
    return generate_table(df)

if __name__ == '__main__':
    app.run_server(debug=True)