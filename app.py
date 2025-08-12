import streamlit as st
import pandas as pd
import plotly.express as px

# configuration page
# Define the layout and elements for the configuration page
st.set_page_config(
    page_title="Dashboard Test",
    page_icon="⚙️",
    layout="wide"
)

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv")

# Barra lateral filtros
st.sidebar.header("Filtros")
#filtros de ano 
anos_disponiveis = sorted(df['ano'].unique())
ano_selecionado = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis )

#Filter de senioridade
senioridade_disponivel = sorted(df['senioridade'].unique())
senioridade_selecionada = st.sidebar.multiselect("Senioridade", senioridade_disponivel, default=senioridade_disponivel)

#Filtro por Tipo de Contratação
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contratação", contratos_disponiveis, default=contratos_disponiveis)

#Filtro por Tamanho de Empresa
tamanho_disponivel = sorted(df['tamanho_empresa'].unique())
tamanho_selecionado = st.sidebar.multiselect("Tamanho de Empresa", tamanho_disponivel, default=tamanho_disponivel)

# filtragem
# Dataframe Principal e filtrado
df_filtrado = df[(df['ano'].isin(ano_selecionado)) &
                 (df['senioridade'].isin(senioridade_selecionada)) &
                 (df['contrato'].isin(contratos_selecionados)) &
                 (df['tamanho_empresa'].isin(tamanho_selecionado))]

# Conteudo principal
st.title("Dashboard de Salários")
st.markdown("Análise de salários por ano, senioridade, tipo de contratação e tamanho da empresa.")

# Metricas Principais (KPIs)
st.subheader("Métricas Principais (Salario anual em Usd)")
if not df_filtrado.empty:
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0]
    cargo_mais_frequente = df_filtrado['cargo'].mode()[0]
else:
    salario_medio, salario_mediano, salario_maximo, total_registros, cargo_mais_comum = 0, 0, 0, 0, ""

col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário Médio", f"${salario_medio:,.0f}")
col2.metric("Salário Máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de Registros", f"{total_registros:,}")
col4.metric("Cargo Mais Frequente", cargo_mais_frequente)

st.markdown("---")

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(top_cargos, x='usd', y='cargo', orientation='h', title="Top 10 Cargos por Salário Médio", labels={"usd": "Salário Médio anual (USD)", "cargo": "Cargo"})

        grafico_cargos.update_layout(title_x=0.1 , yaxis={"categoryorder":"total ascending"})
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.write("Nenhum dado disponível para o gráfico.")
        
with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(df_filtrado, x='usd', nbins=30, title="Distribuição de Salários anuais", labels={"usd": "Salário Anual (USD)", "count": ""})
        grafico_hist.update_layout(title_x=0.1)    
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.write("Nenhum dado disponível para o gráfico.")
        
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index()
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade']
        grafico_remoto = px.pie(remoto_contagem, names='tipo_trabalho', values='quantidade', title="Proporção dos tipos de trabalho", hole=0.5)

        grafico_remoto.update_traces(textinfo='percent+label')
        grafico_remoto.update_layout(title_x=0.1)
        st.plotly_chart(grafico_remoto, use_container_width=True)
    else:
        st.write("Nenhum dado disponível para o gráfico.")
