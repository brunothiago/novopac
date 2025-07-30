import dash
from dash import dcc, html, Output, Input
import plotly.express as px
import pandas as pd

# Dados simulados
data = pd.DataFrame({
    'Modalidade': [
        'Abastecimento de Água - Urbano', 'Abastecimento de Água - Urbano',
        'Abastecimento de Água - Rural', 'Abastecimento de Água - Rural',
        'Esgotamento Sanitário', 'Esgotamento Sanitário',
        'Médias e Grandes Cidades', 'Médias e Grandes Cidades',
        'Renovação de Frota', 'Renovação de Frota',
        'Regularização Fundiária', 'Regularização Fundiária',
        'Urbanização de Favelas', 'Urbanização de Favelas',
        'Contenção de Encostas', 'Contenção de Encostas',
        'Drenagem Urbana', 'Drenagem Urbana',
        'Resíduos Sólidos', 'Resíduos Sólidos',
    ],
    'Subcategoria': ['OGU', 'FIN'] * 10,
    'Qtd_Mun': [12, 10, 8, 6, 15, 12, 9, 7, 4, 5, 10, 8, 11, 9, 5, 4, 6, 5, 7, 6],
    'Qtd_Prop': [18, 15, 10, 8, 20, 17, 12, 9, 6, 7, 14, 11, 16, 13, 8, 7, 9, 8, 10, 9],
    'Valor': [
        100e6, 80e6, 40e6, 30e6, 150e6, 120e6,
        200e6, 180e6, 90e6, 85e6, 110e6, 105e6,
        130e6, 125e6, 95e6, 90e6, 75e6, 70e6,
        60e6, 55e6
    ]
})

modalidade_sums = data.groupby('Modalidade')['Valor'].sum().reset_index()

# Função para cor de contraste
def cor_contraste(cor_hex):
    cor_hex = cor_hex.lstrip('#')
    r, g, b = [int(cor_hex[i:i+2], 16) for i in (0, 2, 4)]
    brilho = (r*299 + g*587 + b*114) / 1000
    return '#000000' if brilho > 160 else '#FFFFFF'

# App
app = dash.Dash(__name__)
app.title = "Dashboard Interativo"

app.layout = html.Div(style={'fontFamily': 'Arial', 'padding': '2rem'}, children=[
    html.H2("Dashboard de Investimentos por Modalidade", style={"textAlign": "center"}),

    # Dropdown para seleção múltipla
    html.Div([
        html.Label("Selecione Modalidades para Somatório:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='dropdown-modalidades',
            options=[{'label': m, 'value': m} for m in sorted(data['Modalidade'].unique())],
            multi=True,
            placeholder="Selecione uma ou mais modalidades"
        )
    ], style={'maxWidth': '800px', 'margin': 'auto'}),

    html.Div(id='resumo-multiselecoes', style={
        'marginTop': '1rem',
        'padding': '1rem',
        'backgroundColor': '#f2f2f2',
        'borderRadius': '10px',
        'maxWidth': '800px',
        'margin': 'auto',
        'textAlign': 'center',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),

    # Gráfico de pizza
    dcc.Graph(
        id='grafico-modalidade',
        figure=px.pie(
            modalidade_sums,
            names='Modalidade',
            values='Valor',
            hole=0.4,
            title="Investimentos por Modalidade"
        ).update_traces(
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(size=14),
            marker=dict(line=dict(color='black', width=0.5)),
            pull=[0.03]*len(modalidade_sums)
        ).update_layout(
            showlegend=False,
            title_x=0.5,
            margin=dict(t=50, b=50, l=0, r=0)
        )
    ),

    html.Div(id='info-modalidade', style={
        'marginTop': '2rem',
        'padding': '1rem',
        'border': '1px solid #ccc',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'maxWidth': '800px',
        'margin': 'auto',
        'textAlign': 'center'
    }, children="Clique em uma modalidade para ver os detalhes.")
])

# Callback do somatório via dropdown
@app.callback(
    Output('resumo-multiselecoes', 'children'),
    Input('dropdown-modalidades', 'value')
)
def resumo_modalidades_selecionadas(mods):
    if not mods:
        return "Selecione uma ou mais modalidades para ver o somatório geral."

    df_filtro = data[data['Modalidade'].isin(mods)]
    qtd_mun = df_filtro['Qtd_Mun'].sum()
    qtd_prop = df_filtro['Qtd_Prop'].sum()
    valor_total = df_filtro['Valor'].sum()

    return html.Div([
        html.H3("Resumo das Modalidades Selecionadas"),
        html.P(f"Modalidades: {', '.join(mods)}"),
        html.P(f"Total de Municípios: {qtd_mun}"),
        html.P(f"Total de Propostas: {qtd_prop}"),
        html.P(f"Valor Total: R$ {valor_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    ])

# Callback do clique no gráfico
@app.callback(
    Output('info-modalidade', 'children'),
    Input('grafico-modalidade', 'clickData')
)
def detalhar_modalidade(clickData):
    if clickData:
        modalidade = clickData['points'][0]['label']
        cor_fatia = clickData['points'][0].get('color', '#CCCCCC')
        filtro = data[data['Modalidade'] == modalidade]
        cor_texto = cor_contraste(cor_fatia)

        blocos = []
        for _, row in filtro.iterrows():
            blocos.append(html.Div([
                html.H4(f"Subcategoria: {row['Subcategoria']}"),
                html.P(f"Qtd Municípios: {row['Qtd_Mun']}"),
                html.P(f"Qtd Propostas: {row['Qtd_Prop']}"),
                html.P(f"Valor Total: R$ {row['Valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
            ], style={
                'backgroundColor': cor_fatia,
                'color': cor_texto,
                'borderRadius': '8px',
                'padding': '1rem',
                'marginBottom': '1.5rem',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
            }))

        return html.Div([
            html.H3(f"Detalhes da Modalidade: {modalidade}", style={'marginBottom': '1.5rem'}),
            *blocos
        ])
    else:
        return "Clique em uma modalidade para ver os detalhes."

# Executa app
if __name__ == '__main__':
    app.run(debug=True)