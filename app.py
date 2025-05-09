import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from common.config import TARGET_FOLDERS, ENDPOINTS_FOLDER, CALLERS_FOLDER, SOURCE_FOLDER, WEB_REPO_URL, API_REPO_URL
from common.repo_donwloader import download_repo
from data_gather.callers_builder import build_api_caller_dictionary
from data_gather.endpoints_builder import build_api_endpoints_dictionary
from data_gather.usage_scanner import build_usage_list
from visualization.graph_builder import visualize_with_graph

def get_full_usage_list_data():
    download_repo(SOURCE_FOLDER, 'zeeguu_web', WEB_REPO_URL)
    download_repo(SOURCE_FOLDER, 'zeeguu_api', API_REPO_URL)
    endpoints_dict = build_api_endpoints_dictionary(ENDPOINTS_FOLDER)
    caller_dict = build_api_caller_dictionary(CALLERS_FOLDER)
    return build_usage_list(endpoints_dict, caller_dict)

FULL_USAGE_LIST = get_full_usage_list_data()
app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(style={'display': 'flex', 'height': '100vh', 'fontFamily': 'Arial, sans-serif'}, children=[
    html.Div(style={'width': '250px', 'padding': '20px', 'backgroundColor': '#f4f4f4', 'overflowY': 'auto',
                    'borderRight': '1px solid #ddd'}, children=[
        html.H3("Display Options", style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#333'}),
        html.Hr(),
        html.Label("Frontend Target Modules:",
                   style={'fontWeight': 'bold', 'marginTop': '15px', 'marginBottom': '5px', 'display': 'block',
                          'color': '#555'}),
        dcc.Checklist(
            id='folder-checklist',
            options=[{'label': folder, 'value': folder} for folder in TARGET_FOLDERS],
            value=TARGET_FOLDERS,
            labelStyle={'marginBottom': '6px', 'marginLeft': '10px', 'fontSize': '14px'},
        )
    ]),
    html.Div(style={'flexGrow': '1', 'padding': '15px', 'display': 'flex', 'justifyContent': 'center',
                    'alignItems': 'center', 'backgroundColor': '#fff'}, children=[
        dcc.Graph(id='dependency-graph', style={'height': '95vh', 'width': '100%'})
    ])
])


@app.callback(
    Output('dependency-graph', 'figure'),
    [Input('folder-checklist', 'value'),
     Input('dependency-graph', 'hoverData')]
)
def update_graph_figure(selected_folders, hover_data):
    hovered_node_id = None
    if hover_data and 'points' in hover_data and hover_data['points']:
        point = hover_data['points'][0]
        if 'customdata' in point and isinstance(point['customdata'], str):
            hovered_node_id = point['customdata']

    fig = visualize_with_graph(
        usage_list=FULL_USAGE_LIST,
        selected_folders=selected_folders,
        hovered_node_id=hovered_node_id
    )
    return fig


if __name__ == '__main__':
    app.run(debug=True)