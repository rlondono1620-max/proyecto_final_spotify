import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("Spotify_Youtube.csv")
df = df[['Views', 'Likes', 'Comments', 'Stream']].dropna()

media_streams = df['Stream'].mean()
df['Popularidad'] = df['Stream'].apply(lambda x: 'Alta' if x > media_streams else 'Baja')

fig_scatter = px.scatter(
    df, x='Views', y='Stream',
    color='Popularidad',
    title="Relación entre Vistas y Streams según Popularidad",
    labels={'Views': 'Vistas en YouTube', 'Stream': 'Reproducciones en Spotify'},
    template='plotly_dark'
)

fig_hist = px.histogram(
    df, x='Stream', nbins=50, color='Popularidad',
    title="Distribución de Reproducciones en Spotify",
    template='plotly_dark'
)

fig_box = px.box(
    df, x='Popularidad', y='Likes',
    title="Distribución de Likes por Nivel de Popularidad",
    labels={'Likes': 'Likes en YouTube', 'Popularidad': 'Popularidad'},
    template='plotly_dark'
)

corr = df[['Views', 'Likes', 'Comments', 'Stream']].corr()
fig_corr = go.Figure(data=go.Heatmap(
    z=corr.values,
    x=corr.columns,
    y=corr.columns,
    colorscale='Blues'))
fig_corr.update_layout(title="Mapa de Calor de Correlaciones")

app = Dash(__name__)
app.title = "Dashboard Spotify & YouTube"

app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'padding': '20px'}, children=[
    html.H1("Dashboard Final – Spotify y YouTube", style={'textAlign': 'center', 'color': '#003366'}),
    html.Hr(),

    html.Div([
        html.P("Este dashboard presenta los resultados del análisis estadístico realizado para explorar la relación entre la interacción en YouTube (vistas, likes y comentarios) y la popularidad en Spotify (streams)."),
        html.P("Se aplicaron métodos de regresión lineal y logística, así como contrastes de hipótesis para validar relaciones significativas entre las variables."),
        html.P("El objetivo es comprender cómo el desempeño en YouTube influye en el éxito musical medido por los streams en Spotify.")
    ], style={'textAlign': 'justify', 'fontSize': '16px'}),

    html.Br(),
    html.H2("Visualizaciones", style={'color': '#003366'}),

    html.Div([
        dcc.Graph(figure=fig_scatter),
        dcc.Graph(figure=fig_hist),
        dcc.Graph(figure=fig_box),
        dcc.Graph(figure=fig_corr),
    ]),

    html.Br(),
    html.H2("Conclusiones del Análisis", style={'color': '#003366'}),

    html.Ul(style={'fontSize': '16px'}, children=[
        html.Li("Existe una relación significativa entre las vistas en YouTube y las reproducciones en Spotify, respaldada por un contraste de hipótesis con p-valor < 0.05."),
        html.Li("Las canciones con mayor número de likes y comentarios tienden a tener más streams."),
        html.Li("La regresión lineal mostró un R² ≈ 0.44, indicando que casi la mitad de la variación en streams puede explicarse por las métricas de YouTube."),
        html.Li("El modelo de regresión logística permitió clasificar canciones populares con una exactitud ≈ 0.23, mostrando margen de mejora."),
        html.Li("Se recomienda incorporar más características, balancear clases y explorar modelos no lineales para mejorar la predicción."),
        html.Li("Los resultados confirman la relevancia de la visibilidad en YouTube como factor clave para el éxito musical en plataformas de streaming.")
    ]),

    html.Br(),
    html.P("Autor: Rafael Estiven Londoño Camacho", style={'textAlign': 'right', 'fontStyle': 'italic', 'color': '#333'}),
    html.P("Proyecto Final – Métodos Estadísticos Computacionales", style={'textAlign': 'right', 'color': '#555'})
])

if __name__ == "__main__":
    app.run(debug=True)
