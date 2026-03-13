import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import kagglehub
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Data Analytics Coffee | Juan Pablo Henao",
    page_icon="☕",
    layout="wide"
)

# Estilo profesional (Tonos Café)
st.markdown("""
    <style>
    .main { background-color: #fdfaf7; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #6f4e37; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #6f4e37; color: white; border-radius: 8px; width: 100%; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1e4d8; border-radius: 5px 5px 0 0; padding: 10px 20px; }
    .stTabs [aria-selected="true"] { background-color: #6f4e37 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS (Kaggle) ---
@st.cache_data
def load_data():
    path = kagglehub.dataset_download("ahmedmohamedibrahim1/coffee-analisys-project")
    files = os.listdir(path)
    csv_file = [f for f in files if f.endswith('.csv')][0]
    df = pd.read_csv(os.path.join(path, csv_file))
    
    # Procesamiento Integrador
    if 'transaction_date' in df.columns:
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        df['hour'] = pd.to_datetime(df['transaction_time']).dt.hour if 'transaction_time' in df.columns else 0
        df['day_name'] = df['transaction_date'].dt.day_name()
        df['revenue'] = df['unit_price'] * df['transaction_qty']
    return df

# --- CONTROL DE NAVEGACIÓN ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- PÁGINA 1: LANDING PAGE ---
if not st.session_state.logged_in:
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.title("☕ Coffee Insights Engine")
        st.subheader("Análisis de Datos Nivel Integrador")
        st.markdown("""
        **Bienvenido al Panel de Control de Ventas.**
        
        Este sistema permite transformar datos crudos de transacciones de café en decisiones estratégicas. 
        Aprenderás a identificar:
        * 📈 **Tendencias de ingresos** diarios.
        * 🎯 **Productos estrella** y categorías líderes.
        * ⏰ **Horas pico** de mayor afluencia.
        
        *Analista Responsable: Juan Pablo Henao*
        """)
        if st.button("🔓 Acceder al Panel de Trabajo"):
            st.session_state.logged_in = True
            st.rerun()

    with col2:
        st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&q=80&w=1000", 
                 caption="Data Science en la industria del café", use_container_width=True)

# --- PÁGINA 2: PANEL DE TRABAJO ---
else:
    df = load_data()
    
    st.sidebar.title("🛠️ Configuración")
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/924/924514.png", width=80)
    
    page = st.sidebar.radio("Navegar a:", ["Dashboard", "Documentación", "Cerrar Sesión"])

    if page == "Cerrar Sesión":
        st.session_state.logged_in = False
        st.rerun()

    elif page == "Documentación":
        st.title("📑 Documentación del Proyecto")
        tab_doc1, tab_doc2 = st.tabs(["Origen de Datos", "Metodología"])
        with tab_doc1:
            st.write("Dataset obtenido vía `kagglehub` desde el repositorio de Ahmed Mohamed Ibrahim.")
            st.info("Estructura: 149k filas con datos de fecha, hora, ubicación de tienda y detalles de producto.")
        with tab_doc2:
            st.write("Se utilizó Python 3.x para el ETL y Seaborn para el análisis de distribución estadística.")

    else:
        st.title("📊 Panel de Análisis de Talento")
        
        # KPIs Principales
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Ingresos Totales", f"${df['revenue'].sum():,.0f}")
        kpi2.metric("Ticket Promedio", f"${df['revenue'].mean():,.2f}")
        kpi3.metric("Cant. Transacciones", f"{len(df):,}")

        # Sección de Gráficos
        st.divider()
        col_g1, col_g2 = st.columns(2)

        with col_g1:
            st.markdown("### 🧬 Distribución de Precios (Seaborn)")
            st.help("Este Boxplot muestra la variabilidad de precios por categoría. Ayuda a identificar productos Premium vs. Económicos.")
            plt.figure(figsize=(10, 6))
            sns.set_style("white")
            sns.boxplot(data=df, x='unit_price', y='product_category', palette="YlOrBr")
            plt.title("Rango de Precios por Categoría")
            st.pyplot(plt)
            plt.close()

        with col_g2:
            st.markdown("### 🌡️ Densidad de Ventas (Seaborn)")
            st.help("Un gráfico de densidad (KDE) para entender en qué rango de precios se concentra el mayor volumen de ventas.")
            plt.figure(figsize=(10, 6))
            sns.kdeplot(data=df, x='unit_price', fill=True, color="#6f4e37")
            plt.title("Concentración de Transacciones por Precio")
            st.pyplot(plt)
            plt.close()

        st.markdown("### 🕒 Mapa de Calor de Ventas por Hora")
        st.help("Gráfico interactivo de Plotly para visualizar los picos de demanda durante el día.")
        hourly_data = df.groupby('hour')['revenue'].sum().reset_index()
        fig_hour = px.line(hourly_data, x='hour', y='revenue', markers=True, 
                           color_discrete_sequence=['#6f4e37'], title="Curva de Ingresos Horaria")
        st.plotly_chart(fig_hour, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.write("Hecho por **Juan Pablo Henao**")
