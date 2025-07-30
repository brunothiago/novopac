import streamlit as st
import plotly.express as px
import pandas as pd

# -------------------
# Dados simulados
# -------------------
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

# -------------------
# Título
# -------------------
st.set_page_config(layout="centered")
st.title("Dashboard de Investimentos por Modalidade")

# -------------------
# Multiseleção
# -------------------
modalidades_disponiveis = sorted(data['Modalidade'].unique())
selecionadas = st.multiselect(
    "Selecione Modalidades para Somatório:",
    modalidades_disponiveis
)

# -------------------
# Gráfico de Pizza
# -------------------
fig = px.pie(
    modalidade_sums,
    names='Modalidade',
    values='Valor',
    hole=0.4,
    title='Investimentos por Modalidade'
)

fig.update_traces(
    textinfo='label+percent',
    textposition='outside',
    textfont=dict(size=13),
    marker=dict(line=dict(color='black', width=0.5)),
    pull=[0.03]*len(modalidade_sums)
)

fig.update_layout(showlegend=False, title_x=0.5)
st.plotly_chart(fig, use_container_width=True)

# -------------------
# Resumo da Seleção
# -------------------
if selecionadas:
    df_sel = data[data['Modalidade'].isin(selecionadas)]
    total_mun = df_sel['Qtd_Mun'].sum()
    total_prop = df_sel['Qtd_Prop'].sum()
    total_valor = df_sel['Valor'].sum()

    st.subheader("🔎 Resumo das Modalidades Selecionadas")
    st.markdown(f"""
    - **Modalidades Selecionadas**: {", ".join(selecionadas)}  
    - **Total de Municípios**: {total_mun}  
    - **Total de Propostas**: {total_prop}  
    - **Valor Total**: R$ {total_valor:,.2f}
    """.replace(",", "X").replace(".", ",").replace("X", "."))

# -------------------
# Modalidade Detalhada
# -------------------
modalidade_detalhada = st.selectbox(
    "Ou selecione uma modalidade para ver detalhes:",
    modalidades_disponiveis
)

df_detalhe = data[data['Modalidade'] == modalidade_detalhada]

st.subheader(f"📌 Detalhes de: {modalidade_detalhada}")
for _, row in df_detalhe.iterrows():
    st.markdown(f"""
    **Subcategoria:** {row['Subcategoria']}  
    • Municípios: {row['Qtd_Mun']}  
    • Propostas: {row['Qtd_Prop']}  
    • Valor: R$ {row['Valor']:,.2f}
    """.replace(",", "X").replace(".", ",").replace("X", "."))
    st.markdown("---")
