##
## Importación de librerías
##
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

##
## Configuración de la página
##
st.set_page_config(
    page_title="Análisis Visual de Ventas de Tienda de Conveniencia",
    layout="wide",
    initial_sidebar_state="expanded"
)

##
## Carga de datos
##
@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=False)
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M').dt.time
    return df

df = load_data()

##
## Sidebar para filtros globales
##
st.sidebar.header("Filtros")
branches = st.sidebar.multiselect("Sucursal (Branch)", options=sorted(df["Branch"].unique()), default=list(df["Branch"].unique()))
product_lines = st.sidebar.multiselect("Línea de Producto", options=sorted(df["Product line"].unique()), default=list(df["Product line"].unique()))
date_min, date_max = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input("Rango de Fechas", [date_min, date_max], min_value=date_min, max_value=date_max)

##
## Aplicación de filtros
##
df_filt = df[
    (df["Branch"].isin(branches)) &
    (df["Product line"].isin(product_lines)) &
    (df["Date"] >= pd.to_datetime(date_range[0])) &
    (df["Date"] <= pd.to_datetime(date_range[1]))
]

##
## Título y texto de la página
##
st.title("Análisis Visual de Ventas de Tienda de Conveniencia")
st.text("Selecciona una tabla para ver los diferentes análisis disponibles:")

tab_names = [ f"Análisis {i+1}" for i in range(8) ]

tabs = st.tabs(tab_names)

##
## Análisis 1: Evolución de las Ventas Totales - Gráfico de Líneas
##
def plot_sales_evolution(df):
    sales_by_date = df.groupby("Date")["Total"].sum().reset_index()
    fig = px.line(sales_by_date, x="Date", y="Total", title="Evolución de las Ventas Totales")
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Ventas Totales")
    st.plotly_chart(fig, use_container_width=True)

with tabs[0]:
    st.subheader("1. Evolución de las Ventas Totales")
    st.markdown("""
    Este gráfico permite observar cómo han variado las ventas totales a lo largo del tiempo en las fechas seleccionadas.

    #### ¿Qué muestra?
    - La evolución y variación de las ventas totales para el periodo registrado en los datos.
    - El eje x muestra las fechas seleccionadas.
    - El eje y muestra el monto total de las ventas.
    
    #### ¿Qué observamos?
    - Para las 3 sucursales, el día con mayor registro de ventas corresponde al día 9 de marzo del 2019.
    - Para las 3 sucursales, el día con menor registro de ventas corresponde al día 1 de marzo del 2019.
    ---
    """)
    plot_sales_evolution(df_filt)
    st.markdown("---")

##
## Análisis 2: Ingresos por Línea de Producto - Gráfico de Barras
##
def plot_income_by_product_line(df):
    income_by_line = df.groupby("Product line")["Total"].sum().sort_values().reset_index()
    fig = px.bar(income_by_line, x="Total", y="Product line", orientation="h", title="Ingresos por Línea de Producto")
    fig.update_layout(xaxis_title="Ingreso Total", yaxis_title="Línea de Producto")
    st.plotly_chart(fig, use_container_width=True)

with tabs[1]:
    st.subheader("2. Ingresos por Línea de Producto")
    st.markdown("""
    Este gráfico permite observar el ingreso total generado por cada línea de productos vendido en las sucursales.

    #### ¿Qué muestra?
    - Un gráfico de barras horizontal que muestra el ingreso total por cada línea de productos.
    - El eje x muestra el ingreso total.
    - El eje y muestra la línea de productos reportada.
    
    #### ¿Qué observamos?
    ##### Sucursales A, B y C
    - La línea de productos "Food and beverages" es la que genera el mayor ingreso total para todas las sucursales.
    - La línea de productos "Health and beauty" es la que genera el menor ingreso total para todas las sucursales.
    ##### Sucursal A
    - Para el caso de la sucursal "A", se observa que la línea de productos "Home and lifestyle" es la que genera el mayor ingreso total.
    - Por otro lado, la línea de productos "Health and beauty" es la que genera el menor ingreso total para la sucursal "A".
    ##### Sucursal B
    - Para el caso de la sucursal "B", se observa que la línea de productos "Sports and Travel" es la que genera el mayor ingreso total seguido muy de cerca por
    la línea de productos "Health and Beauty"
    - Mientras que la línea de productos "Food and beverages" es la que genera el menor ingreso total para la sucursal "B".
    ##### Sucursal C
    - Para el caso de la sucursal "C", se observa que la línea de productos "Food and beverages" es la que genera el mayor ingreso total.
    - Por otro lado, la línea de productos "Home and lifestyle" es la que genera el menor ingreso total para la sucursal "C".
    ---
    """)
    plot_income_by_product_line(df_filt)
    st.markdown("---")

##
## Análisis 3: Distribución de la Calificación de Clientes (mejorado) - Gráfico de Histograma
##
def plot_rating_distribution(df):
    fig = px.histogram(
        df,
        x="Rating",
        nbins=20,
        title="Distribución de la Calificación de Clientes",
        color_discrete_sequence=["#4e79a7"]
    )
    fig.update_layout(
        xaxis_title="Calificación (Rating)",
        yaxis_title="Frecuencia de Clientes",
        template="plotly_white",
        bargap=0.05
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.subheader("3. Distribución de la Calificación de Clientes")
    st.markdown("""
    Este gráfico permite observar cómo se distribuyen las calificaciones entregadas por los clientes.

    #### ¿Qué muestra?
    - Un histograma con 20 divisiones (bins) para mayor detalle.
    - Permite ver si hay una tendencia general hacia calificaciones positivas o negativas.

    #### ¿Qué observamos?
    - La mayoría de las calificaciones se concentran entre 6 y 9, indicando satisfacción general positiva.
    - Pocas calificaciones extremas (muy bajas o muy altas).
    - Útil para evaluar la percepción global de la experiencia del cliente.
    """)
    plot_rating_distribution(df_filt)
    st.markdown("---")

##
## Análisis 4: Comparación del Gasto por Tipo de Cliente (mejorado) - Gráfico de Boxplot
##
def plot_spending_by_customer_type(df):
    fig = px.box(
        df,
        x="Customer type",
        y="Total",
        color="Customer type",
        points="all",
        title="Comparación del Gasto por Tipo de Cliente",
        color_discrete_map={"Member": "#59a14f", "Normal": "#edc948"}
    )
    fig.update_traces(jitter=0.3, marker_opacity=0.5)
    fig.update_layout(
        xaxis_title="Tipo de Cliente",
        yaxis_title="Monto Total de Compra",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.subheader("4. Comparación del Gasto por Tipo de Cliente")
    st.markdown("""
    Este gráfico boxplot compara cómo varía el monto de compra entre clientes miembros (Member) y normales (Normal).

    #### ¿Qué muestra?
    - Distribución estadística completa del gasto total por cliente según su tipo.
    - Se incluyen todos los puntos individuales para observar la dispersión.

    #### ¿Qué observamos?
    - Los clientes "Member" tienden a tener un gasto levemente más alto en promedio.
    - Hay valores atípicos en ambos grupos, pero mayor dispersión en clientes normales.
    - Esto sugiere que los miembros podrían estar más comprometidos o compran productos de mayor valor.
    """)
    plot_spending_by_customer_type(df_filt)
    st.markdown("---")

##
## Análisis 5: Relación entre Bienes Vendidos e Ingreso Bruto - Gráfico de Mapa de Densidad
##
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
    - En general (considerando todos los datos sin filtrar): se le puede ***recomendar a la tienda que ofrezca productos de costo variado***, ya que los productos de costo bajo son los más vendidos, pero los de costo alto generan un ingreso bruto mayor.
    ---
    """
    st.markdown(md)
    plot_quantity_vs_gross_income(df_filt)
    st.markdown("---")

##
## Análisis 6: Métodos de Pago Preferidos - Gráfico de Pastel
##
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

##
## Análisis 7: Mapa de Calor de Correlaciones - Gráfico de Calor
##
def plot_correlation_heatmap(df):
    num_cols = ["Unit price", "Quantity", "Tax 5%", "Total", "cogs", "gross income", "Rating"]
    corr = df[num_cols].corr()
    fig = px.imshow(corr, text_auto=True, color_continuous_scale="BuRd", title="Mapa de Calor de Correlaciones",width=1000,height=600)
    st.plotly_chart(fig, use_container_width=True)

with tabs[6]:
    st.subheader("7. Mapa de Calor de Correlaciones")
    st.markdown("""
    Este gráfico heatmap nos permite obtener una representacion visual de las correlaciones entre las variables.

    #### ¿Qué muestra?
    - El índice de correlacion entre las variables cuantitativas de las ventas
    - Los valores mientras más cercanos a 1 mayor correlación y se representa con colores mas cálidos, valores mas alejados de 1 colores mas fríos
    - Tanto el eje y como el x representan a las variables analizadas
    
    #### ¿Qué observamos?
    - La calificacion de los clientes no esta correlacionada con ninguna variable del set de datos por lo que la satisfación es independiente del monto gastado.
    - Las variables ventas, costo, ingresos brutos e impuestos estan perfectamente correlacionadas, por lo que cualquier variacion en alguna de aquellas variables se reflejara en las demás con la misma proporción.
    """)
    plot_correlation_heatmap(df_filt)
    st.markdown("---")

##
## Análisis 8: Composición del Ingreso Bruto por Sucursal y Línea de Producto
##
def plot_gross_income_by_branch_and_line(df):
    grouped = df.groupby(["Branch", "Product line"])['gross income'].sum().reset_index()
    fig = px.bar(grouped, x="Branch", y="gross income", color="Product line", barmode="stack", title="Ingreso Bruto por Sucursal y Línea de Producto")
    fig.update_layout(xaxis_title="Sucursal", yaxis_title="Ingreso Bruto")
    st.plotly_chart(fig, use_container_width=True)

with tabs[7]:
    st.subheader("8. Composición del Ingreso Bruto por Sucursal y Línea de Producto")
    st.markdown("""
    Este gráfico de barras apilado nos permite ver como se componen las ventas de las tiendas por las líneas de producto.

    #### ¿Qué muestra?
    - Muestra las sucursales A, B y C y como se dividen los Ingresos Brutos segun la linea de producto
    - El eje x muestra las sucursales
    - El eje y muestra el monto de los Ingresos
    
    #### ¿Qué observamos?
    - La Sucursal C es la que tiene un ingreso bruto mayor
    - Las lineas que generan mas dinero en cada sucursal son: Hogar y estilo de vida en la Sucursal A, en sucursal a es Deporte y viaje y salud y belleza, en la sucursal c es bebidas y alimentos.
    - Todas las Sucursales tienen una linea diferente como la que mas aporta al Ingreso Bruto
    - La linea de electronicos es la que cuenta con los ingresos brutos mas equilibrados entre sucursales
    """)
    plot_gross_income_by_branch_and_line(df_filt)
    st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.info("Dashboard desarrollado por el Grupo 48 para el Módulo 5 del diplomado Big Data and Machine Learning UAutónoma, Mayo 2025.")
