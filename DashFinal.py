import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go


app = dash.Dash(__name__)

df = pd.read_csv('NewPrams.csv')


mapbox_access_token= 'pk.eyJ1Ijoic2VpbTEzIiwiYSI6ImNrNzI0eHNvMzAzc2QzZnFvMW13ZGFsaDUifQ.PFW6yngxB32bhHxOjprc3w'
mapbox_style = "mapbox://styles/plotlymapbox/cjvprkf3t1kns1cqjxuxmwixz"


topic_list= df["Topic"].unique()
question_list = df["Question"].unique()
Break_Out_Category_list=df["Break_Out_Category"].unique()
Break_Out_list=df['Break_Out'].unique()
Response_list=df['Response'].unique()


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.H6("Pregnancy data analysis"),
        ],
    )

def build_graph_title(title):
    return html.P(className="graph-title", children=title)

    

def generate_control_card():

    return html.Div(
        id="control-card",
        children=[
            html.H3("Select Topic"),
            dcc.Dropdown(
                id="Topic-select",
                options=[{"label": i, "value": i} for i in topic_list],
                value=topic_list[0],
            ),
            html.Br(),
            
            html.H3("Select Question"),
            dcc.Dropdown(
                id='Question-select',
                options=[{"label": i, "value": i} for i in question_list],
                value= question_list[0],
            ),
            html.Br(),

            html.H3("Bar plot"),
            dcc.Graph(
                id='basic-interactions',
            ),
            html.Br(),

            html.H3("Select Break Out Category"),
            dcc.Dropdown(
                id='Break-select',
                options=[{"label": i, "value": i} for i in Break_Out_Category_list],
                value= Break_Out_Category_list[0],
            ),
            html.Br(),

            html.H3("Bar plot des reponses"),
            dcc.Graph(
                id='response-bar-plot',
            ),
            html.Br(),

            html.H3("Select the response you want to study"),
            dcc.Checklist(
                id='Response-select', 
                options=[{"label": i, "value": i} for i in Response_list],
                value= [],
                labelStyle={'display': 'unset','font-family': 'Open Sans','color':'#321A37','font-size': '1.2rem'},
            ),
            html.Br(),

            dcc.Graph(id="county-choropleth"),
            html.Br(), 
            html.Div(id="tittle2", children =[build_graph_title(" How to improve Mother and Baby health depending on topic :")]),
            html.Br(),html.Br(),
            html.Div(id='display-topic', style={'display': 'unset','font-family': 'Open Sans','color':'#321A37','font-size': '1.8rem', 'line-height': '1rem', 'font-weight': '300'}),
            html.Br(),html.Br(),
            html.Div(id='display-message', style={'display': 'unset','font-family': 'Open Sans','color':'#321A37','font-size': '1.2rem', 'font-weight': '200','font-style': 'italic'}),
            html.Br(),html.Br(),
            html.Div(id='display-question', style={'display': 'unset','font-family': 'Open Sans','color':'#321A37','font-size': '1.8rem', 'line-height': '1rem', 'font-weight': '300'}),
            html.Br(), 

            html.H3("Response repartition"),
            dcc.Graph(
                id='response-bar-stack',
            ),
            html.Br(),

        ],
    )


app.layout = html.Div(
    id="app-container",
    children=[
        # Banner
        html.Div(
            id="top-row",
            children=[ 
                 html.Div(
                    className="row",
                    id="top-row-header",
                    children=[
                        html.Div(
                            id="header-container",
                            children=[
                                build_banner(),
                                html.P(
                                    id="instructions",
                                    children="US infant mortality rate has dropped 15% over the past decade, the United States continues to have one of the highest infant mortality rates among developed countries, at 5.8 per 1000 live births in 2015",
                                    style={'opacity': '0.8','color':'#321A37'}
                                ),
                                html.P(
                                    id="instructions2",
                                    children="The purpose of this protocol is to guide population health surveillance, so that the local public health unit can effectively evolving health of the population. The goal of this protocol is to support and improve the health and well-being of the population, including reducing health inequalities",
                                    style={'opacity': '0.8','color':'#321A37'}
                                ),
                                 html.Br(),
                                html.P(
                                    id="instructions3",
                                    children="How to improve health of women and child in USA ?" 
                                    "PRAMS try to work on that question by collecting amount of Data on what happend before/during/after the prengnancy of women"
                                ),
                             
                            ],
                        )
                    ], 
                 ),
                 html.Div(
                    className="row",
                    id="top-row-graphs",
                    children=[
                        # Well map
                        html.Div(
                            id="well-map-container",
                            children=[
                                build_graph_title(" Discover the data set "),
                                generate_control_card(),
                            ],
                        )
                    ],
                 )
            ],
        ),
    ],
)


@app.callback(
    Output('Question-select','options'),
    [Input('Topic-select','value')]
)
def set_question_options(selected_Topic):
    return[{'label': i, 'value':i} for i in pd.unique(df[df['Topic'] == selected_Topic]['Question'])]

@app.callback(
    Output('Question-select', 'value'),
    [Input('Question-select', 'options')])
def set_question_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('basic-interactions','figure'),
    [Input('Question-select','value')]
)
def set_BarPlot_BO(selected_Question):
    s = df[(df['Question'] == selected_Question)].groupby(['Break_Out_Category','Question']).size().to_frame('count').reset_index()
    data = [go.Scatter(
        x=s['Break_Out_Category'],
        y=s['count'],
        mode='markers',
        marker =dict(size=s['count']/3, color="#FBB6B1")
        )]
    layout = go.Layout(
        title = go.layout.Title(
            text = "Repartion of the subdject that influence the women's response at the question"
            ),
    )
    return go.Figure(data = data, layout = layout)

@app.callback(
    Output('Break-select', 'value'),
    [Input('Break-select', 'options')])
def set_Break_value(available_Break):
    return available_Break[0]['value']

@app.callback(
    Output('response-bar-plot','figure'),
    [Input('Break-select','value'), Input('Question-select','value')]
)
def set_BarPlot_BO(selected_Break, selected_Question):
    return px.bar(df[(df['Question'] == selected_Question) & (df['Break_Out_Category'] == selected_Break)], x="Break_Out", color="Response",barmode="group",color_discrete_sequence = px.colors.sequential.Burg)

@app.callback(
    Output('Response-select', 'options'),
    [Input('Break-select','value'), Input('Question-select','value')]
)
def set_response_options(selected_Break, selected_Question):
    return[{'label': i, 'value':i} for i in pd.unique(df[(df['Question'] == selected_Question) & (df['Break_Out_Category'] == selected_Break)]["Response"])]


@app.callback(
    Output('Response-select', 'value'),
    [Input('Response-select', 'options')])
def set_Response(available_response):
    return [available_response[0]['value'],available_response[-1]['value']]

@app.callback(
    Output("county-choropleth", "figure"),
    [Input('Question-select','value'), Input('Response-select','value')]
)

def display_map(selected_Question, selected_Response):
    u = df[(df['Question'] == selected_Question)].groupby(['LocationAbbr','Response']).size().to_frame('count').reset_index()
    Tes = u[u['Response'].isin(selected_Response)].groupby(['LocationAbbr'], as_index=False).sum()
    data = [go.Choropleth(
        colorscale = 'redor',
        autocolorscale = False,
        locations = Tes['LocationAbbr'],
        z = Tes['count'],
        locationmode = 'USA-states',
        marker = go.choropleth.Marker(
            line = go.choropleth.marker.Line(
                color = 'rgb(255,255,255)',
                width = 2
            )
        ),
        colorbar = go.choropleth.ColorBar(
            title = " count of response ")
    )]
    layout = go.Layout(
        title = go.layout.Title(
            text = 'Repartion of response by state'
            ),
        geo = go.layout.Geo(
            scope = 'usa',
            projection = go.layout.geo.Projection(type = 'albers usa'),
            showlakes = True,
            lakecolor = 'rgb(255, 255, 255)'),
    )
    # fig = dict(data=data, layout=layout)
    # return fig
    return go.Figure(data = data, layout = layout)

@app.callback(
    [Output('display-topic','children'), Output('display-message','children')],
    [Input('Topic-select','value')]
)
def print(selected_Topic):
    if selected_Topic == "Sleep Behaviors" :
        return ("You select the topic : {}".format(selected_Topic), "SIDS (Sudden Infant Death Syndrome) is the leading cause of death among infants between the age of 1 month and 1 year, and the third leading cause of infant mortalityMaintaining both a safe sleep position and a safe sleep environment can reduce the risk of SUID/SIDS. Doctor recommended to place an infant on their back for every sleep .So regulate and improving Baby sleep is significant.")
    if selected_Topic == "Breastfeeding" :
        return ("You select the topic : {}".format(selected_Topic), "Women initiated breastfeeding, many stopped by the time their infant was 3–4 months old also health organizations recommend that babies be exclusively breastfed for the first 6 months of life. But Breast feeding is important for the baby health.")
    if selected_Topic == "Oral Health" :
        return ("You select the topic : {}".format(selected_Topic), "Providing oral health services to pregnant women not only improves women’s oral health, but also presents an important opportunity for pregnant women to receive education on how to prevent dental cavities for their children. could help delay or prevent mother-to-child transmission of the infectious agent associated with dental caries, or cavities. The cavity-causing bacteria can be passed from caregivers, especially mothers, to children.")
        
@app.callback(
    Output('display-question','children'),
    [Input('Question-select','value')]
)
def print(selected_Question):
    return "Your Question : {}".format(selected_Question)

@app.callback(
    Output('response-bar-stack','figure'),
    [Input('Question-select','value')]
)
def set_BarStack_rp(selected_Question):
    u = df[(df['Question'] == selected_Question)].groupby(["Break_Out_Category","Response"], as_index=False).mean()
    return px.bar(u, x="Break_Out_Category", y="Data_Value", color='Response',color_discrete_sequence = px.colors.sequential.Burg)


if __name__ == '__main__':
    app.run_server(debug=True)