
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd

# Configuração da página
st.set_page_config(
    page_title="Análise da Formação Técnica em Enfermagem",
    page_icon="🏥",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def load_data():
    dados_raciais = pd.read_csv('CassificacaoRacialRendaSexo.csv')
    dados_cargos = pd.read_csv('CargosCarreira.csv')
    dados_evasao = pd.read_csv('TaxaEvasao.csv')
    dados_rap = pd.read_csv('RelacaoAlunoProfessorRAP.csv')
    dados_orcamento = pd.read_csv('PanoramaOrcamentario.csv')
    return dados_raciais, dados_cargos, dados_evasao, dados_rap, dados_orcamento

# Carregando dados
dados_raciais, dados_cargos, dados_evasao, dados_rap, dados_orcamento = load_data()

# Sidebar
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione uma página:",
    ["Visão Geral", "Distribuição Geográfica", "Perfil Sociodemográfico", "Indicadores Educacionais", "Análise Orçamentária"]
)

# Título principal
st.title("Análise da Formação Técnica em Enfermagem nas Universidades Federais")

# Páginas
if pagina == "Visão Geral":
    st.header("Visão Geral")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Total de instituições
        total_inst = dados_raciais['Instituicao'].nunique()
        st.metric("Total de Instituições", total_inst)
        
        # Gráfico de matrículas por região
        fig_matriculas = px.bar(
            dados_raciais.groupby('Região')['Número de Matrículas'].sum().reset_index(),
            x='Região',
            y='Número de Matrículas',
            title='Matrículas por Região'
        )
        st.plotly_chart(fig_matriculas)
    
    with col2:
        # Total de matrículas
        total_matriculas = dados_raciais['Número de Matrículas'].sum()
        st.metric("Total de Matrículas", f"{total_matriculas:,.0f}")
        
        # Gráfico de evasão
        fig_evasao = px.line(
            dados_evasao.groupby('Ano')['Taxa de Evasão'].mean().reset_index(),
            x='Ano',
            y='Taxa de Evasão',
            title='Evolução da Taxa de Evasão'
        )
        st.plotly_chart(fig_evasao)

elif pagina == "Distribuição Geográfica":
    st.header("Distribuição Geográfica")
    
    # Mapa de distribuição
    dados_mapa = dados_raciais.groupby(['UF', 'Estado'])['Número de Matrículas'].sum().reset_index()
    
    # Criar mapa base
    m = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)
    
    # Adicionar marcadores para cada estado
    for idx, row in dados_mapa.iterrows():
        folium.Circle(
            location=[0, 0],  # Você precisará adicionar as coordenadas corretas
            popup=f"{row['Estado']}: {row['Número de Matrículas']} matrículas",
            radius=float(row['Número de Matrículas'])/10,
            color='red',
            fill=True
        ).add_to(m)
    
    folium_static(m)

elif pagina == "Perfil Sociodemográfico":
    st.header("Perfil Sociodemográfico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribuição por raça/cor
        fig_raca = px.pie(
            dados_raciais.groupby('CorRaca')['Número de Matrículas'].sum().reset_index(),
            values='Número de Matrículas',
            names='CorRaca',
            title='Distribuição por Raça/Cor'
        )
        st.plotly_chart(fig_raca)
    
    with col2:
        # Distribuição por renda
        fig_renda = px.pie(
            dados_raciais.groupby('RendaFamiliar')['Número de Matrículas'].sum().reset_index(),
            values='Número de Matrículas',
            names='RendaFamiliar',
            title='Distribuição por Renda Familiar'
        )
        st.plotly_chart(fig_renda)

elif pagina == "Indicadores Educacionais":
    st.header("Indicadores Educacionais")
    
    # Relação aluno-professor
    fig_rap = px.line(
        dados_rap,
        x='Ano',
        y='RAP',
        title='Relação Aluno-Professor ao Longo do Tempo'
    )
    st.plotly_chart(fig_rap)
    
    # Taxa de evasão por região
    fig_evasao_regiao = px.box(
        dados_evasao,
        x='Região',
        y='Taxa de Evasão',
        title='Taxa de Evasão por Região'
    )
    st.plotly_chart(fig_evasao_regiao)

elif pagina == "Análise Orçamentária":
    st.header("Análise Orçamentária")
    
    # Evolução orçamentária
    fig_orcamento = px.line(
        dados_orcamento,
        x='Ano',
        y='Orçamento',
        title='Evolução do Orçamento ao Longo do Tempo'
    )
    st.plotly_chart(fig_orcamento)
    
    # Distribuição do orçamento por região
    fig_orcamento_regiao = px.bar(
        dados_orcamento.groupby('Região')['Orçamento'].sum().reset_index(),
        x='Região',
        y='Orçamento',
        title='Distribuição do Orçamento por Região'
    )
    st.plotly_chart(fig_orcamento_regiao)
