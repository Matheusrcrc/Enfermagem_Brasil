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
        # Carregando as duas partes do arquivo de classificação racial
        dados_raciais_parte1 = pd.read_csv('data/CassificacaoRacialRendaSexo_parte1.csv', encoding='utf-8', sep=';')
        dados_raciais_parte2 = pd.read_csv('data/CassificacaoRacialRendaSexo_parte2.csv', encoding='utf-8', sep=';')
        # Concatenando as duas partes
        dados_raciais = pd.concat([dados_raciais_parte1, dados_raciais_parte2], ignore_index=True)
        
        # Carregando os demais arquivos
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

