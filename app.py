
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
import geopandas as gpd
import os

# Configuração da página
st.set_page_config(
    page_title="Análise da Formação Técnica em Enfermagem",
    page_icon="🏥",
    layout="wide"
)

# Função para carregar dados com tratamento de erros
@st.cache_data
def load_data():
    try:
        dados_raciais = pd.read_csv('data/CassificacaoRacialRendaSexo.csv', encoding='utf-8')
        dados_cargos = pd.read_csv('data/CargosCarreira.csv', encoding='utf-8')
        dados_evasao = pd.read_csv('data/TaxaEvasao.csv', encoding='utf-8')
        dados_rap = pd.read_csv('data/RelacaoAlunoProfessorRAP.csv', encoding='utf-8')
        dados_orcamento = pd.read_csv('data/PanoramaOrcamentario.csv', encoding='utf-8')
        return dados_raciais, dados_cargos, dados_evasao, dados_rap, dados_orcamento
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar arquivo: {str(e)}")
        return None, None, None, None, None
    except pd.errors.EmptyDataError:
        st.error("Um ou mais arquivos CSV estão vazios")
        return None, None, None, None, None
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")
        return None, None, None, None, None

# Carregando dados
dados = load_data()

# Verificar se os dados foram carregados corretamente
if all(x is not None for x in dados):
    dados_raciais, dados_cargos, dados_evasao, dados_rap, dados_orcamento = dados
else:
    st.error("Não foi possível carregar todos os dados necessários")
    st.stop()

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
        try:
            dados_matriculas = dados_raciais.groupby('Região')['Número de Matrículas'].sum().reset_index()
            fig_matriculas = px.bar(
                dados_matriculas,
                x='Região',
                y='Número de Matrículas',
                title='Matrículas por Região'
            )
            st.plotly_chart(fig_matriculas)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de matrículas: {str(e)}")
    
    with col2:
        # Total de matrículas
        total_matriculas = dados_raciais['Número de Matrículas'].sum()
        st.metric("Total de Matrículas", f"{total_matriculas:,.0f}")
        
        # Gráfico de evasão
        try:
            dados_evasao_media = dados_evasao.groupby('Ano')['Taxa de Evasão'].mean().reset_index()
            fig_evasao = px.line(
                dados_evasao_media,
                x='Ano',
                y='Taxa de Evasão',
                title='Evolução da Taxa de Evasão'
            )
            st.plotly_chart(fig_evasao)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de evasão: {str(e)}")

elif pagina == "Distribuição Geográfica":
    st.header("Distribuição Geográfica")
    
    try:
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
    except Exception as e:
        st.error(f"Erro ao gerar mapa: {str(e)}")

elif pagina == "Perfil Sociodemográfico":
    st.header("Perfil Sociodemográfico")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            # Distribuição por raça/cor
            dados_raca = dados_raciais.groupby('CorRaca')['Número de Matrículas'].sum().reset_index()
            fig_raca = px.pie(
                dados_raca,
                values='Número de Matrículas',
                names='CorRaca',
                title='Distribuição por Raça/Cor'
            )
            st.plotly_chart(fig_raca)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de raça/cor: {str(e)}")
    
    with col2:
        try:
            # Distribuição por renda
            dados_renda = dados_raciais.groupby('RendaFamiliar')['Número de Matrículas'].sum().reset_index()
            fig_renda = px.pie(
                dados_renda,
                values='Número de Matrículas',
                names='RendaFamiliar',
                title='Distribuição por Renda Familiar'
            )
            st.plotly_chart(fig_renda)
        except Exception as e:
            st.error(f"Erro ao gerar gráfico de renda: {str(e)}")

elif pagina == "Indicadores Educacionais":
    st.header("Indicadores Educacionais")
    
    try:
        # Relação aluno-professor
        fig_rap = px.line(
            dados_rap,
            x='Ano',
            y='RAP',
            title='Relação Aluno-Professor ao Longo do Tempo'
        )
        st.plotly_chart(fig_rap)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de relação aluno-professor: {str(e)}")
    
    try:
        # Taxa de evasão por região
        fig_evasao_regiao = px.box(
            dados_evasao,
            x='Região',
            y='Taxa de Evasão',
            title='Taxa de Evasão por Região'
        )
        st.plotly_chart(fig_evasao_regiao)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de evasão por região: {str(e)}")

elif pagina == "Análise Orçamentária":
    st.header("Análise Orçamentária")
    
    try:
        # Evolução orçamentária
        fig_orcamento = px.line(
            dados_orcamento,
            x='Ano',
            y='Orçamento',
            title='Evolução do Orçamento ao Longo do Tempo'
        )
        st.plotly_chart(fig_orcamento)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de evolução orçamentária: {str(e)}")
    
    try:
        # Distribuição do orçamento por região
        dados_orcamento_regiao = dados_orcamento.groupby('Região')['Orçamento'].sum().reset_index()
        fig_orcamento_regiao = px.bar(
            dados_orcamento_regiao,
            x='Região',
            y='Orçamento',
            title='Distribuição do Orçamento por Região'
        )
        st.plotly_chart(fig_orcamento_regiao)
    except Exception as e:
        st.error(f"Erro ao gerar gráfico de orçamento por região: {str(e)}")
