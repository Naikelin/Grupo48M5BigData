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
st.text("Selecciona una tabla para ver los diferentes análisis disponibles:")

tab_names = [ f"Análisis {i+1}" for i in range(8) ]

tabs = st.tabs(tab_names)

# 1. Evolución de las Ventas Totales
def plot_sales_evolution(df):
    sales_by_date = df.groupby("Date")["Total"].sum().reset_index()
    fig = px.line(sales_by_date, x="Date", y="Total", title="Evolución de las Ventas Totales")
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Ventas Totales")
    st.plotly_chart(fig, use_container_width=True)

with tabs[0]:
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

with tabs[1]:
    st.subheader("2. Ingresos por Línea de Producto")
    st.markdown("Compara el ingreso total generado por cada línea de productos.")
    plot_income_by_product_line(df_filt)
    st.markdown("---")

# 3. Distribución de la Calificación de Clientes
def plot_rating_distribution(df):
    fig = px.histogram(df, x="Rating", nbins=20, title="Distribución de la Calificación de Clientes")
    fig.update_layout(xaxis_title="Calificación", yaxis_title="Frecuencia")
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("3. Distribución de la Calificación de Clientes")
    st.markdown("Analiza la distribución de las calificaciones de los clientes.")
    plot_rating_distribution(df_filt)
    st.markdown("---")

# 4. Comparación del Gasto por Tipo de Cliente
def plot_spending_by_customer_type(df):
    fig = px.box(df, x="Customer type", y="Total", color="Customer type", points="all", title="Comparación del Gasto por Tipo de Cliente")
    fig.update_layout(xaxis_title="Tipo de Cliente", yaxis_title="Gasto Total")
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("4. Comparación del Gasto por Tipo de Cliente")
    st.markdown("Compara la distribución del gasto total entre clientes Member y Normal.")
    plot_spending_by_customer_type(df_filt)
    st.markdown("---")

# 5. Relación entre Bienes Vendidos e Ingreso Bruto
def plot_quantity_vs_gross_income(df):
    fig = px.density_heatmap(
        df,
        x="cogs",
        y="gross income",
        nbinsx=30,
        nbinsy=30,
        title="Mapa de Densidad: Costo vs Ganancia Bruta",
        labels={"cogs": "Costo de Bienes Vendidos (COGS)", "gross income": "Ganancia Bruta"},
        marginal_x="histogram",
        marginal_y="histogram"
    )
    fig.update_layout(
        xaxis_title="Costo de Bienes Vendidos (COGS)",
        yaxis_title="Ganancia Bruta",
        coloraxis_colorbar=dict(title="Cantidad de Observaciones"),
        template="simple_white",
        height=600,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[4]:
    st.subheader("5. Relación entre Bienes Vendidos e Ingreso Bruto")
    md = """
    Analiza la relación entre la cantidad de bienes vendidos y el ingreso bruto.
    - **cogs**: Costo de los bienes
    - **gross income**: Ingreso bruto

    #### ¿Cómo leer el gráfico?
    Cada celda de color representa un rango de valores de cogs (eje X) y gross income (eje Y).

    El color indica la concentración de transacciones:

    - Colores más claros (cercanos al blanco) significan que hay más datos (ventas) en esa zona.
    - Colores más oscuros (cercanos al azul) indican menos transacciones en ese rango.

    En los márgenes del gráfico, se incluyen histogramas que muestran cómo se distribuyen los valores de cada variable individualmente.

    #### ¿Qué se puede observar?
    - Los puntos de mayor densidad están alineados en diagonal ascendente, indica una relación directa: a mayor costo, mayor ganancia bruta.
    - Esto quiere decir que los productos con un costo más alto tienden a generar un ingreso bruto mayor, sin embargo, existe una mayor concentración de ventas en productos con un costo bajo.
    - En general (considerando todos los datos sin filtrar): se le puede ***recocmendar a la tienda que ofrezca productos de costo variado***, ya que los productos de costo bajo son los más vendidos, pero los de costo alto generan un ingreso bruto mayor.
    ---
    """
    st.markdown(md)
    plot_quantity_vs_gross_income(df_filt)
    st.markdown("---")

# 6. Métodos de Pago Preferidos
def plot_payment_methods(df):
    payment_counts = df["Payment"].value_counts().reset_index()
    payment_counts.columns = ["Método de Pago", "Cantidad"]
    fig = px.pie(
        payment_counts,
        names="Método de Pago",
        values="Cantidad",
        title="Métodos de Pago Preferidos",
        hole=0.3
    )
    fig.update_layout(
        template="simple_white",
        height=500,
        margin=dict(l=40, r=40, t=60, b=40)
    )
    st.plotly_chart(fig, use_container_width=True)


with tabs[5]:
    st.subheader("6. Métodos de Pago Preferidos")
    md = """
    Analiza cuáles son los métodos de pago más utilizados por los clientes.

    #### ¿Cómo leer el gráfico?
    Este gráfico de tipo **pastel** muestra la proporción de cada método de pago en el total de transacciones realizadas.

    - Cada segmento representa un tipo de pago.
    - El tamaño de cada segmento es proporcional al número de veces que se utilizó ese método.

    #### ¿Qué se puede observar?
    - El método de pago más grande indica la **preferencia predominante** de los clientes.
    - Permite a la tienda optimizar procesos de caja o incluso evaluar promociones asociadas a ciertos métodos de pago más utilizados.
    ---
    """
    st.markdown(md)
    plot_payment_methods(df_filt)
    st.markdown("---")

# 7. Mapa de Calor de Correlaciones
def plot_correlation_heatmap(df):
    num_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross margin percentage", "gross income", "Rating"]
    corr = df[num_cols].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", title="Mapa de Calor de Correlaciones")
    st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
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

with tabs[7]:
    st.subheader("8. Composición del Ingreso Bruto por Sucursal y Línea de Producto")
    st.markdown("Muestra la contribución de cada línea de producto al ingreso bruto dentro de cada sucursal.")
    plot_gross_income_by_branch_and_line(df_filt)
    st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.info("Dashboard desarrollado para el análisis visual de ventas de una tienda de conveniencia. Selecciona filtros para explorar los datos de interés.")