import datetime

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, ctx
from itertools import combinations

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP])

# Initialize in-memory storage for tasks and scores
tasks = []
comparisons = []
scores = []

# Define the layout of the app
app.layout = dbc.Container([
    html.Nav(className='navbar navbar-expand-lg navbar-dark bg-primary', 
        style={'paddingLeft': '1rem', 'paddingRight': '1rem'},
        id='app-page-header',
        children=[
            # represents the URL bar, doesn't render anything
            dcc.Location(id='url', refresh=False),
            html.A(className='navbar-brand',
                children=[
                    html.Img(src='assets/favicon-dark.ico', width="25", height="25", style={'filter': 'invert(1)'}),
                    html.Span('Task Priority', style={'marginLeft': '1rem'}),
                ],
                href="/",
            ),
            html.Div(style={'flex': 'auto'}),#, children=[
            html.Ul(className='navbar-nav', children=[
                html.Li(className='nav-item', children=[
                    html.A(className='nav-link',
                        children=['by Tarlis'],
                        href="https://tarlis.com.br",
                    ),
                ]),
#                html.Li(className='nav-item', children=[
#                    html.A(className='nav-link nav-link-btn',
#                        id='gh-link',
#                        children=['GitHub'],
#                        href="https://github.com/ttportela/task-priority",
#                    ),
#                ]),
            ]),
        ],
    ),
    dbc.Accordion(id='tasks-container', children=[
        dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        html.H1("Task Priority"),
                        dbc.Textarea(id="task-input", placeholder="Enter each task on a new line", rows=10, style={'minWidth': '100%'}),
                        dbc.Button("Submit", id="submit-tasks", color="primary", className="mt-2"),
                    ], width=12),
                ]),
        
            ],
            title='Step 1 - Task Input',
        ),
        dbc.AccordionItem([
                dbc.Row([
                    dbc.Col([
                        html.Div(id="comparison-container"),
                        html.Div(id="result-container"),
                    ])
                ]),
            ],
            title='Step 2 - Priority Rank',
        ),
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.Span('© '+str(datetime.datetime.now().date().year)+', by ', style={'marginLeft': '1rem'}),
            html.A(
                children=['Tarlis'],
                href="https://tarlis.com.br",
            ),
            html.Span(' on '),
            html.A(
                children=['GitHub'],
                href='https://github.com/ttportela/task-priority',
            ),
            html.Span('.'),
        ])
    ]),
], fluid=True)

@app.callback(
    Output("comparison-container", "children"),
    Input("submit-tasks", "n_clicks"),
    Input({"type": "task-button", "index": ALL}, "n_clicks"),
    State("task-input", "value"),
    State("comparison-container", "children")
)
def handle_submissions(sub_n_clicks, n_clicks, tasks, current_comparison):
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if triggered_id == "submit-tasks":
        return handle_task_submission(sub_n_clicks, tasks)
    else:
        return handle_task_comparison(n_clicks, current_comparison)

# Callback to handle task submission
#@app.callback(
#    Output("comparison-container", "children"),
#    Input("submit-tasks", "n_clicks"),
#    State("task-input", "value")
#)
def handle_task_submission(n_clicks, value):
    global tasks, comparisons, scores
    if n_clicks is None or not value:
        return ""
    
    # Split the input into tasks
    tasks = [task.strip() for task in value.split('\n') if task.strip()]
    comparisons = list(combinations(range(len(tasks)), 2))
    scores = [0] * len(tasks)

    if comparisons:
        first_pair = comparisons[0]
        return dbc.Card([
            dbc.CardBody([
                html.H5("Which task is more important?"),
                dbc.Button(tasks[first_pair[0]], id={"type": "task-button", "index": first_pair[0]}, color="primary", className="m-1"),
                dbc.Button(tasks[first_pair[1]], id={"type": "task-button", "index": first_pair[1]}, color="primary", className="m-1"),
            ])
        ])
    else:
        return ""

# Callback to handle task comparison
#@app.callback(
#    Output("comparison-container", "children"),
#    Input({"type": "task-button", "index": ALL}, "n_clicks"),
#    State("comparison-container", "children")
#)
def handle_task_comparison(n_clicks, current_comparison):
    global comparisons, scores
    if not ctx.triggered:
        return current_comparison
    
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    index = eval(button_id)["index"]
    scores[index] += 1

    if comparisons:
        comparisons.pop(0)

    if comparisons:
        next_pair = comparisons[0]
        comparison_card = dbc.Card([
            dbc.CardBody([
                html.H5("Which task is more important?"),
                dbc.Button(tasks[next_pair[0]], id={"type": "task-button", "index": next_pair[0]}, color="primary", className="m-1"),
                dbc.Button(tasks[next_pair[1]], id={"type": "task-button", "index": next_pair[1]}, color="primary", className="m-1"),
            ])
        ])
        return comparison_card
    else:
        return ""

# Callback to display the results
@app.callback(
    Output("result-container", "children"),
    Input({"type": "task-button", "index": ALL}, "n_clicks")
)
def display_results(n_clicks):
    global comparisons, tasks, scores
    if comparisons:
        return ""
    
    ranked_tasks = sorted(zip(tasks, scores), key=lambda x: x[1], reverse=True)
    result_list = dbc.ListGroup(
        [dbc.ListGroupItem([
                f"{task}", 
                dbc.Badge(f"Prioriry Score: {score}", color="info", className="me-1", style={'float': 'right'}),
            ]) for task, score in ranked_tasks],
        flush=True,
    )
    return result_list

# Run the app on a different port
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)  # Change port here
