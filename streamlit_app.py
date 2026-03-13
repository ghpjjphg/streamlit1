import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import kagglehub
import os
import glob

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Data Analytics Coffee | Juan Pablo Henao",
    page_icon="☕",
    layout="wide"
)

# Estilo profesional personalizado (Colores Café)
st.markdown("""
    <style>
    .main { background-color: #fdfaf7; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 12px; border-left: 6px solid #6f4e37; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #6f4e37; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f1e4d8; border-radius: 5px 5px 0 0; padding: 10px 20px; color: #6f4e37; }
    .stTabs [aria-selected="true"] { background-color: #6f4e37 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    try:
        path = kagglehub.dataset_download("ahmedmohamedibrahim1/coffee-analisys-project")
        # Búsqueda recursiva para evitar IndexError
        csv_files = glob.glob(os.path.join(path, "**/*.csv"), recursive=True)
        if not csv_files: return None
        
        target_file = next((f for f in csv_files if "Sales" in f), csv_files[0])
        df = pd.read_csv(target_file)
        
        # Limpieza básica
        if 'transaction_date' in df.columns:
            df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        if 'unit_price' in df.columns and 'transaction_qty' in df.columns:
            df['total_bill'] = df['unit_price'] * df['transaction_qty']
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# --- NAVEGACIÓN ---
if 'view' not in st.session_state:
    st.session_state.view = 'landing'

# --- LANDING PAGE ---
if st.session_state.view == 'landing':
    col_text, col_img = st.columns([1, 1], gap="large")
    with col_text:
        st.title("☕ Coffee Insights & Analytics")
        st.subheader("Proyecto Nivel Integrador | Talento Tech")
        st.markdown("""
        ### Análisis del Mercado del Café
        Bienvenido al panel de control diseñado por **Juan Pablo Henao**. 
        Aquí exploraremos los datos de ventas para optimizar la toma de decisiones.
        """)
        if st.button("🚀 Ingresar al Panel de Trabajo"):
            st.session_state.view = 'panel'
            st.rerun()
    with col_img:
        st.image("https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?q=80&w=1000", use_container_width=True)

# --- PANEL DE TRABAJO ---
else:
    df = load_data()
    if df is not None:
        st.sidebar.title("📊 Navegación")
        menu = st.sidebar.radio("Secciones:", ["Dashboard", "Documentación", "Volver al Inicio"])
        
        if menu == "Volver al Inicio":
            st.session_state.view = 'landing'
            st.rerun()
        elif menu == "Documentación":
            st.title("📑 Documentación")
            with st.expander("Metodología"):
                st.write("Análisis descriptivo con Python, Seaborn y Plotly.")
        else:
            st.title("📈 Panel de Análisis")
            # KPIs
            c1, c2, c3 = st.columns(3)
            c1.metric("Ingresos Totales", f"${df['total_bill'].sum():,.0f}")
            c2.metric("Ticket Promedio", f"${df['total_bill'].mean():,.2f}")
            c3.metric("Ventas", f"{len(df):,}")

            # Gráficos
            tab1, tab2 = st.tabs(["🔬 Seaborn", "🕒 Tendencias"])
            with tab1:
                st.markdown("### Dispersión de Precios")
                st.help("Análisis estadístico de precios por categoría.")
                plt.figure(figsize=(10, 5))
                sns.boxplot(data=df, x='unit_price', y='product_category', palette="YlOrBr")
                st.pyplot(plt)
                plt.close()
            with tab2:
                fig = px.histogram(df, x='unit_price', title="Distribución de Precios", color_discrete_sequence=['#6f4e37'])
                st.plotly_chart(fig, use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.write("**Autor:** Juan Pablo Henao")

