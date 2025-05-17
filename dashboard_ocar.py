import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="Análisis Visual de Ventas de Tienda de Conveniencia",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=False)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
    return df

df = load_data()

# Sidebar para filtros globales
st.sidebar.header("Filtros")
branches = st.sidebar.multiselect("Sucursal (Branch)", options=sorted(df["Branch"].unique()), default=list(df["Branch"].unique()))
product_lines = st.sidebar.multiselect("Línea de Producto", options=sorted(df["Product line"].unique()), default=list(df["Product line"].unique()))
date_min, date_max = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input("Rango de Fechas", [date_min, date_max], min_value=date_min, max_value=date_max)

# Aplicar filtros
df_filt = df[
    (df["Branch"].isin(branches)) &
    (df["Product line"].isin(product_lines)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

st.title("Análisis Visual de Ventas de Tienda de Conveniencia")
st.markdown("---")

# 1. Evolución de las Ventas Totales
def plot_sales_evolution(df):
    sales_by_date = df.groupby("Date")["Total"].sum().reset_index()
    fig = px.line(sales_by_date, x="Date", y="Total", title="Evolución de las Ventas Totales")
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Ventas Totales")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("1. Evolución de las Ventas Totales")
st.markdown("Muestra cómo han variado las ventas totales a lo largo del tiempo.")
plot_sales_evolution(df_filt)
st.markdown("---")

# 2. Ingresos por Línea de Producto
def plot_income_by_product_line(df):
    income_by_line = df.groupby("Product line")["Total"].sum().sort_values().reset_index()
    fig = px.bar(income_by_line, x="Total", y="Product line", orientation="h", title="Ingresos por Línea de Producto")
    fig.update_layout(xaxis_title="Ingreso Total", yaxis_title="Línea de Producto")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("2. Ingresos por Línea de Producto")
st.markdown("Compara el ingreso total generado por cada línea de productos.")
plot_income_by_product_line(df_filt)
st.markdown("---")

# 3. Distribución de la Calificación de Clientes
def plot_rating_distribution(df):
    fig = px.histogram(df, x="Rating", nbins=20, title="Distribución de la Calificación de Clientes")
    fig.update_layout(xaxis_title="Calificación", yaxis_title="Frecuencia")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("3. Distribución de la Calificación de Clientes")
st.markdown("Analiza la distribución de las calificaciones de los clientes.")
plot_rating_distribution(df_filt)
st.markdown("---")

# 4. Comparación del Gasto por Tipo de Cliente
def plot_spending_by_customer_type(df):
    fig = px.box(df, x="Customer type", y="Total", color="Customer type", points="all", title="Comparación del Gasto por Tipo de Cliente")
    fig.update_layout(xaxis_title="Tipo de Cliente", yaxis_title="Gasto Total")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("4. Comparación del Gasto por Tipo de Cliente")
st.markdown("Compara la distribución del gasto total entre clientes Member y Normal.")
plot_spending_by_customer_type(df_filt)
st.markdown("---")

# 5. Relación entre Bienes Vendidos e Ingreso Bruto
def plot_quantity_vs_gross_income(df):
    fig = px.scatter(df, x="Quantity", y="gross income", color="Product line", title="Relación entre Bienes Vendidos e Ingreso Bruto", opacity=0.7)
    fig.update_layout(xaxis_title="Cantidad", yaxis_title="Ingreso Bruto")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("5. Relación entre Bienes Vendidos e Ingreso Bruto")
st.markdown("Visualiza la relación entre la cantidad de bienes vendidos y el ingreso bruto.")
plot_quantity_vs_gross_income(df_filt)
st.markdown("---")

# 6. Métodos de Pago Preferidos
def plot_payment_methods(df):
    payment_counts = df["Payment"].value_counts().reset_index()
    payment_counts.columns = ["Método de Pago", "Cantidad"]
    fig = px.pie(payment_counts, names="Método de Pago", values="Cantidad", title="Métodos de Pago Preferidos", hole=0.3)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("6. Métodos de Pago Preferidos")
st.markdown("Identifica los métodos de pago más frecuentes.")
plot_payment_methods(df_filt)
st.markdown("---")

# 7. Mapa de Calor de Correlaciones
def plot_correlation_heatmap(df):
    num_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross margin percentage", "gross income", "Rating"]
    corr = df[num_cols].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", title="Mapa de Calor de Correlaciones")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("7. Mapa de Calor de Correlaciones")
st.markdown("Visualiza la matriz de correlación entre variables numéricas.")
plot_correlation_heatmap(df_filt)
st.markdown("---")

# 8. Composición del Ingreso Bruto por Sucursal y Línea de Producto
def plot_gross_income_by_branch_and_line(df):
    grouped = df.groupby(["Branch", "Product line"])['gross income'].sum().reset_index()
    fig = px.bar(grouped, x="Branch", y="gross income", color="Product line", barmode="stack", title="Ingreso Bruto por Sucursal y Línea de Producto")
    fig.update_layout(xaxis_title="Sucursal", yaxis_title="Ingreso Bruto")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("8. Composición del Ingreso Bruto por Sucursal y Línea de Producto")
st.markdown("Muestra la contribución de cada línea de producto al ingreso bruto dentro de cada sucursal.")
plot_gross_income_by_branch_and_line(df_filt)
st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.info("Dashboard desarrollado para el análisis visual de ventas de una tienda de conveniencia. Selecciona filtros para explorar los datos de interés.")