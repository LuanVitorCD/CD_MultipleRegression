import os
import dash
from dash import dcc, html, dash_table, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from datetime import datetime, timedelta

# Dados
data = {
    'temperatura': [25.8, 25.5, 21.8, 22.2, 20.7, 20.9, 22.3, 23.3, 22.7, 22.1, 21.4, 22.6, 22.1, 22.5, 22.7, 
                    25.4, 26.8, 25.9, 24.0, 24.3, 26.6, 26.8, 22.4, 23.7, 23.7, 23.3, 24.6, 24.3, 22.6, 22.5, 
                    23.4, 25.4, 27.2, 27.9, 28.4, 25.5, 24.3, 25.3, 27.3, 28.0, 28.4, 25.5, 23.1, 24.7, 24.3,
                    26.7, 20.9, 20.5, 21.7, 23.4, 25.2, 25.4, 25.3, 26.6, 27.8, 24.6, 23.8, 25.0, 26.5, 26.9, 
                    29.1, 28.2, 27.2, 27.1, 27.2, 27.3, 20.8, 18.7, 20.1, 20.5, 20.2, 17.4, 18.3, 19.5, 21.0, 
                    21.2, 20.7, 21.7, 22.7, 22.9, 24.0, 25.5, 22.3, 24.2, 21.5, 22.5, 23.5, 24.4, 23.7, 19.9],
    'umidade': [74, 58, 54, 57, 68, 68, 74, 73, 82, 83, 76, 71, 78, 83, 82, 76, 70, 72, 
                77, 67, 63, 64, 89, 85, 80, 84, 83, 80, 87, 83, 79, 72, 69, 70, 67, 78, 
                78, 75, 73, 68, 67, 77, 91, 81, 89, 82, 97, 88, 77, 73, 76, 73, 77, 73, 
                68, 83, 89, 85, 76, 81, 73, 72, 65, 67, 63, 62, 92, 86, 82, 85, 83, 73, 
                70, 72, 79, 81, 71, 61, 58, 64, 65, 68, 81, 74, 89, 83, 84, 76, 82, 92],
    'sensacao_termica': [26.8, 25.4, 21.8, 22.1, 20.7, 20.8, 22.6, 23.6, 23.2, 22.4, 21.6, 22.7, 22.4, 22.7, 22.9, 
                         26.7, 27.6, 26.9, 24.2, 24.6, 26.8, 27.6, 22.4, 24.4, 24.0, 24.1, 25.7, 24.9, 23.0, 22.9, 
                         24.0, 26.0, 28.3, 29.6, 29.8, 26.9, 25.0, 26.6, 28.8, 30.1, 30.0, 26.4, 23.4, 25.8, 25.1, 
                         28.9, 20.9, 20.5, 21.7, 23.7, 26.6, 26.4, 26.7, 28.0, 29.4, 25.5, 24.6, 26.4, 28.6, 29.8, 
                         31.1, 29.9, 28.4, 28.2, 27.7, 28.2, 20.8, 18.7, 20.2, 20.6, 20.2, 17.4, 18.3, 19.4, 21.1, 
                         21.3, 20.6, 21.7, 22.7, 22.9, 24.0, 26.0, 22.5, 24.6, 21.5, 22.9, 24.2, 25.0, 24.4, 19.9]
}

df = pd.DataFrame(data)

# Modelo de regressão
x = df[['temperatura', 'umidade']]
y = df['sensacao_termica']
model = LinearRegression().fit(x, y)
r2 = r2_score(y, model.predict(x))
coeficientes = model.coef_
intercepto = model.intercept_
variaveis = x.columns
termos = ' + '.join([f"({coef:.4f} × {var})" for coef, var in zip(coeficientes, variaveis)])

# Datas
datas = [f"2024-01-{dia:02d}" for dia in range(1, 32)]
datas += [f"2024-02-{dia:02d}" for dia in range(1, 29)]
datas += [f"2024-03-{dia:02d}" for dia in range(1, 32)]
df['data'] = pd.to_datetime(datas)
df['Mês'] = df['data'].dt.strftime('%B')
df['dia'] = df['data'].dt.day
meses_pt = {'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março'}
df['Mês'] = df['Mês'].map(meses_pt)
df['mes'] = df['Mês']  # Duplicado para compatibilidade com o callback

# Cores e tema
cor_fundo = '#0e1117'
cor_detalhes = '#00a8ff'
cor_texto = '#e0e0e0'
cor_texto_black = '#0e1117'
cor_card = '#1a1d24'

# Configuração do app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        'backgroundColor': cor_fundo,
        'color': cor_texto,
        'fontFamily': 'Arial, sans-serif',
        'minHeight': '100vh',
        'padding': '20px',
        'textAlign': 'center'
    },
    children=[
        # Cabeçalho
        html.Div(
            style={
                'textAlign': 'center',
                'marginBottom': '30px',
                'borderBottom': f'1px solid {cor_detalhes}',
                'paddingBottom': '15px'
            },
            children=[
                html.H1(
                    "Dashboard: Sensação Térmica",
                    style={
                        'color': cor_detalhes,
                        'fontSize': '2.5rem',
                        'marginBottom': '10px',
                        'textShadow': '0 0 5px rgba(0, 168, 255, 0.5)'
                    }
                ),
                html.P(
                    "Análise de sensação térmica baseada em temperatura e umidade",
                    style={
                        'fontSize': '1.1rem',
                        'color': '#a0a0a0'
                    }
                )
            ]
        ),
        
        # Cards de informação
        html.Div(
            style={
                'display': 'flex',
                'flexWrap': 'wrap',
                'gap': '20px',
                'marginBottom': '30px'
            },
            children=[
                # Card da equação
                html.Div(
                    style={
                        'flex': '1',
                        'minWidth': '300px',
                        'backgroundColor': cor_card,
                        'padding': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
                        'borderLeft': f'4px solid {cor_detalhes}'
                    },
                    children=[
                        html.H3(
                            "Modelo de Regressão Linear Múltipla",
                            style={
                                'color': cor_detalhes,
                                'marginTop': '0',
                                'borderBottom': f'1px solid {cor_detalhes}',
                                'paddingBottom': '10px'
                            }
                        ),
                        html.P(
                            f"Sensação térmica = {intercepto:.4f} + {termos}",
                            style={
                                'fontSize': '16px',
                                'backgroundColor': '#141920',
                                'padding': '15px',
                                'borderRadius': '5px',
                                'overflowX': 'auto'
                            }
                        )
                    ]
                ),
                
                # Card do R²
                html.Div(
                    style={
                        'width': '200px',
                        'backgroundColor': cor_card,
                        'padding': '20px',
                        'borderRadius': '8px',
                        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
                        'textAlign': 'center',
                        'display': 'flex',
                        'flexDirection': 'column',
                        'justifyContent': 'center',
                        'borderLeft': f'4px solid {cor_detalhes}'
                    },
                    children=[
                        html.H3(
                            "R²",
                            style={
                                'color': cor_detalhes,
                                'marginTop': '0'
                            }
                        ),
                        html.Div(
                            f"{r2:.4f}",
                            style={
                                'fontSize': '2.5rem',
                                'fontWeight': 'bold',
                                'color': "#0091FF",
                                'textShadow': '0 0 10px rgba(0, 119, 255, 0.7)'
                            }
                        )
                    ]
                )
            ]
        ),
        
        # Gráfico 3D com superfície de regressão
        html.Div(
            style={
                'backgroundColor': cor_card,
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
                'marginBottom': '30px'
            },
            children=[
                dcc.Graph(
                    id='grafico-3d',
                    style={
                        'height': '600px',
                        'width': '90%',  # Ajuste para menos que 100% para dar margem
                        'display': 'inline-block',  # Isso ajuda no alinhamento central
                        'margin': '0 auto',  # Centraliza horizontalmente
                        'textAlign': 'center'
                    }
                )
            ]
        ),
        
        # Controles e tabela
        html.Div(
            style={
                'backgroundColor': cor_card,
                'padding': '20px',
                'borderRadius': '8px',
                'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)'
            },
            children=[
                html.Div(
                    style={
                        'display': 'flex',
                        'alignItems': 'center',
                        'marginBottom': '20px',
                        'flexWrap': 'wrap',
                        'gap': '10px'
                    },
                    children=[
                        html.Label(
                            "Filtrar Tabela por Mês:",
                            style={
                                'fontSize': '16px',
                                'fontWeight': 'bold',
                                'color': cor_detalhes,
                                'marginRight': '10px'
                            }
                        ),
                        dcc.Dropdown(
                            id='mes-dropdown-tabela',
                            options=[
                                {'label': 'Todos os meses', 'value': 'Todos'},
                                {'label': 'Janeiro', 'value': 'Janeiro'},
                                {'label': 'Fevereiro', 'value': 'Fevereiro'},
                                {'label': 'Março', 'value': 'Março'}
                            ],
                            value='Todos',
                            clearable=True,
                            style={
                                'width': '200px',
                                'backgroundColor': "#FFFFFF",
                                'color': cor_texto_black,
                                'border': f'1px solid {cor_detalhes}'
                            },
                            placeholder='Selecione um mês',
                        )
                    ]
                ),
                
                html.H3(
                    "Dados Analisados",
                    style={
                        'color': cor_detalhes,
                        'marginTop': '0',
                        'borderBottom': f'1px solid {cor_detalhes}',
                        'paddingBottom': '10px'
                    }
                ),
                
                dash_table.DataTable(
                    id='tabela-dados',
                    columns=[
                        {'name': 'Data', 'id': 'data', 'type': 'datetime'},
                        {'name': 'Temperatura (°C)', 'id': 'temperatura', 'type': 'numeric', 'format': {'specifier': '.1f'}},
                        {'name': 'Umidade (%)', 'id': 'umidade', 'type': 'numeric', 'format': {'specifier': '.0f'}},
                        {'name': 'Sensação Térmica (°C)', 'id': 'sensacao_termica', 'type': 'numeric', 'format': {'specifier': '.1f'}}
                    ],
                    page_size=15,
                    style_table={
                        'overflowX': 'auto',
                        'borderRadius': '5px'
                    },
                    style_cell={
                        'backgroundColor': '#141920',
                        'color': cor_texto,
                        'textAlign': 'center',
                        'padding': '12px',
                        'border': f'1px solid {cor_fundo}'
                    },
                    style_header={
                        'backgroundColor': cor_detalhes,
                        'color': cor_fundo,
                        'fontWeight': 'bold',
                        'border': 'none'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#1a1d24',
                        }
                    ],
                    sort_action="native"
                )
            ]
        )
    ]
)

@app.callback(
    Output('grafico-3d', 'figure'),
    [Input('mes-dropdown-tabela', 'value')]
)
def update_grafico(mes_selecionado):
    dff = df.copy()
    titulo = 'Sensação térmica - Todos os meses'
    
    if mes_selecionado != 'Todos':
        dff = dff[dff['Mês'] == mes_selecionado]
        titulo = f'Sensação térmica - {mes_selecionado}'

    # Scatter 3D
    fig = px.scatter_3d(
        dff, 
        x='temperatura', 
        y='umidade', 
        z='sensacao_termica',
        color='Mês',
        color_discrete_sequence=["#007fff", "#91ffe9", "#00ff26"],  #["#55f873", "#857fff", "#09d4ac"] 
        hover_data=['dia'],
        title=titulo,
        labels={
            'temperatura': 'Temperatura (°C)', 
            'umidade': 'Umidade (%)', 
            'sensacao_termica': 'Sensação Térmica (°C)'
        }
    )
    
    # Adiciona superfície de regressão
    # Define grade para temperatura e umidade
    temp_range = np.linspace(df['temperatura'].min(), df['temperatura'].max(), 20)
    umid_range = np.linspace(df['umidade'].min(), df['umidade'].max(), 20)
    xx, yy = np.meshgrid(temp_range, umid_range)
    predict_data = pd.DataFrame(np.column_stack((xx.ravel(), yy.ravel())), 
                          columns=['temperatura', 'umidade'])
    zz = model.predict(predict_data).reshape(xx.shape)
    
    surface = go.Surface(
    x=xx,
    y=yy,
    z=zz,
    surfacecolor=xx,  # Usa temperatura para definir a cor
    colorscale=[ 
        [0.0, "#006EFF"], #0000ff
        [0.5, "#FBFF0A"], #FFF674
        [1.0, "#CA0838"] #CA0838
    ],
    cmin=df['temperatura'].min(),   # Limite inferior da escala
    cmax=df['temperatura'].max(),  # Corta os 10% mais quentes
    opacity=0.65,
    showscale=False
)
    fig.add_trace(surface)
    
    # Configurações dos traços
    fig.update_traces(
        selector=dict(type='scatter3d'),
        marker=dict(
            size=6,
            opacity=1,
            line=dict(width=0.5, color='black')
        )
    )
    
    fig.update_layout(
        plot_bgcolor=cor_card,
        paper_bgcolor=cor_card,
        font_color=cor_texto,
        scene=dict(
            xaxis_title='Temperatura (°C)',
            yaxis_title='Umidade (%)',
            zaxis_title='Sensação Térmica (°C)',
            bgcolor=cor_card,
            xaxis=dict(
                gridcolor='#2a2e3a',
                zerolinecolor='#2a2e3a',
                title_font=dict(color=cor_detalhes)
            ),
            yaxis=dict(
                gridcolor='#2a2e3a',
                zerolinecolor='#2a2e3a',
                title_font=dict(color=cor_detalhes)
            ),
            zaxis=dict(
                gridcolor='#2a2e3a',
                zerolinecolor='#2a2e3a',
                title_font=dict(color=cor_detalhes)
            ),
            aspectratio=dict(x=1.6, y=1.6, z=1.6),  # Proporções iguais para aspecto de cubo
            camera=dict(eye=dict(x=-2.5, y=-2.4, z=1.5))  # Perspectiva angular
        ),
        title=dict(
            x=0.5,
            font=dict(size=20, color=cor_detalhes)
        ),
        margin=dict(l=180, r=0, b=100, t=40),
        legend=dict(
            title_font=dict(color=cor_detalhes, size=24),
            font=dict(color=cor_texto, size=20),
            bgcolor='rgba(0,0,0,0)'
        )
    )
    
    return fig

@app.callback(
    Output('tabela-dados', 'data'),
    [Input('mes-dropdown-tabela', 'value')]
)
def update_tabela(mes_selecionado):
    if mes_selecionado == 'Todos':
        dff = df.copy()
    else:
        dff = df[df['mes'] == mes_selecionado]
    
    dff_display = dff.copy()
    dff_display['data'] = dff_display['data'].dt.strftime('%d/%m/%Y')
    dff_display = dff_display[['data', 'temperatura', 'umidade', 'sensacao_termica']]
    
    return dff_display.to_dict('records')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))  
    app.run(host='0.0.0.0', port=port, debug=False)
