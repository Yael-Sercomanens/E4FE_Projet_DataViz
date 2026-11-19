# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 13:07:40 2026

@author: sercomay
"""

import pandas as pd
df = pd.read_csv("Donnees/df_final.csv", sep=';', encoding='utf-8')

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

import geopandas as gpd
from shapely.affinity import translate, scale

# Configurations Streamlit

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .st-key-header_block {
        text-align: center;
    }
    .st-key-header_block blockquote {
        display: inline-block;
        text-align: left;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Infos au début


with st.container(key="header_block"):

    st.title('Tableau de bord - Installations Enedis en France')
    
    st.write("Notre étude se repose sur les installations Enedis de production d'énergie < 36 kW sur toute la France entre 1904 et 2025.")
    
    st.markdown("> NB : Les années entre 1904 et 1974 sont assez vides, les donnees commencent à etre intéressantes entre 1975 et 2025.")

# Configurations colonnes

col1, col2 =st.columns(2)

# Première colonne

with col1 :

    st.header("Évolution dans le temps des installations en fonction de la région et du département.")
    
    # Opérations
    
    operation = st.selectbox(
        "Choisir l'opération :",
        ["Somme", "Moyenne", "Nombre d'installations"]
    )
    
    if operation == "Somme":
      pd_operation = "sum"
      y_title = "maxPuis"
    elif operation == "Moyenne":
      pd_operation = "mean"
      y_title = "maxPuis"
    elif operation == "Nombre d'installations":
      pd_operation = "count"
      y_title = "nombre"
    
    # Configurations régions
    
    liste_regions = df["region"].unique().tolist()
    options_regions = ["Toutes"] + liste_regions
    
    selection_region  = st.multiselect(
        "Choisir la / les régions :",
        options_regions,
        default = ["Toutes"]
    )
    
    if "Toutes" in selection_region:
        regions = liste_regions
    else:
        regions = selection_region
    
    # Configurations départements
    
    liste_departements = df[((df["region"].isin(regions)))]["departement"].unique().tolist()
    options_departements = ["Tous"] + liste_departements
    
    selection_departement  = st.multiselect(
        "Choisir le / les départements :",
        options_departements,
        default = ["Tous"]
    )
    
    if "Tous" in selection_departement:
        departements = liste_departements
    else:
        departements = selection_departement
    
    # Tri du df en fonction des configurations
    
    dfSommeMaxPuisParAnnee = df[(df["region"].isin(regions)) & (df["departement"].isin(departements))].groupby("dateMiseEnService")[["maxPuis"]].agg(pd_operation).reset_index()
    
    if operation == "Nombre d'installations":
        dfSommeMaxPuisParAnnee = dfSommeMaxPuisParAnnee.rename(columns={"maxPuis": "nombre"})
    
    # Figure plotly
    
    fig1 = px.line(dfSommeMaxPuisParAnnee, x="dateMiseEnService", y=y_title)
    
    fig1.update_layout(
        xaxis_rangeslider_visible=True
    )
    
    st.plotly_chart(fig1)
    
with col2 :

    st.header("Évolution dans le temps des installations en fonction de la filière et de la technologie.")
    
    # Opérations
    
    operation2 = st.selectbox(
        "Choisir l'opération :",
        ["Somme", "Moyenne", "Nombre d'installations"],
        key="operation_2"
    )
    
    if operation2 == "Somme":
      pd_operation = "sum"
      y_title = "maxPuis"
    elif operation2 == "Moyenne":
      pd_operation = "mean"
      y_title = "maxPuis"
    elif operation2 == "Nombre d'installations":
      pd_operation = "count"
      y_title = "nombre"
    
    # Configurations filières
    
    liste_filieres = df["filiere"].unique().tolist()
    options_filieres = ["Toutes"] + liste_filieres
    
    selection_filiere  = st.multiselect(
        "Choisir la / les filières :",
        options_filieres,
        default = ["Toutes"]
    )
    
    if "Toutes" in selection_filiere:
        filires = liste_filieres
    else:
        filires = selection_filiere
    
    # Configurations technologies
    
    liste_technologies = df[((df["filiere"].isin(filires)))]["technologie"].unique().tolist()
    options_technologies = ["Toutes"] + liste_technologies
    
    selection_technologie  = st.multiselect(
        "Choisir la / les technologies :",
        options_technologies,
        default = ["Toutes"]
    )
    
    if "Toutes" in selection_technologie:
        technologies = liste_technologies
    else:
        technologies = selection_technologie
    
    # Tri du df en fonction des configurations
    
    dfMaxPuisParAnnee = df[(df["filiere"].isin(filires)) & (df["technologie"].isin(technologies))].groupby(["dateMiseEnService", "filiere", "technologie"])["maxPuis"].agg(pd_operation).reset_index()
    
    if operation2 == "Nombre d'installations":
        dfMaxPuisParAnnee = dfMaxPuisParAnnee.rename(columns={"maxPuis": "nombre"})
    
    # Figure plotly
    
    fig2 = px.area(dfMaxPuisParAnnee, x="dateMiseEnService", y=y_title, color="filiere", pattern_shape="technologie")
    
    fig2.update_layout(
        xaxis_rangeslider_visible=True,
        legend=dict(
            orientation="h",
            maxheight=0.15,
        )
    )
    
    st.plotly_chart(fig2, key="chart_2")

gdf = gpd.read_file("Donnees/departements-avec-outre-mer.geojson")

drom_layout = {
    "971": {"target": (-7.5, 49.0), "scale": 1},   # Guadeloupe
    "972": {"target": (-7.5, 48.0), "scale": 1},   # Martinique
    "973": {"target": (-6.5, 44.0), "scale": 1},   # Guyane
    "974": {"target": (-7.5, 47.0), "scale": 1},   # La Réunion
    # nous n'avons aucune données sur la mayotte donc inutile de la déplacée
}

def rapprocher_drom(row):
    cfg = drom_layout.get(row["code"])
    if cfg:
        geom = scale(row.geometry, xfact=cfg["scale"], yfact=cfg["scale"], origin="centroid")
        c = geom.centroid
        return translate(geom, xoff=cfg["target"][0] - c.x, yoff=cfg["target"][1] - c.y)
    return row.geometry

gdf["geometry"] = gdf.apply(rapprocher_drom, axis=1)

gdf["lon"] = gdf.geometry.centroid.x
gdf["lat"] = gdf.geometry.centroid.y

dfSommeMaxPuisToutesAnnees = df.groupby("departement")[["maxPuis"]].agg("sum").reset_index()

df_map = dfSommeMaxPuisToutesAnnees.merge(
    gdf[["nom", "lat", "lon"]],
    left_on="departement",
    right_on="nom",
    how="inner",
)

fig = px.choropleth(
    df_map,
    geojson=gdf.__geo_interface__,
    locations="nom",
    featureidkey="properties.nom",
    color="maxPuis",
    hover_name="nom",
    hover_data={"nom": False, "maxPuis": ":,.2f"},
    labels={"maxPuis": "Puissance cumulée (kWh)"},
    color_continuous_scale="Viridis",
    projection="mercator",
    title="Puissance Maximale Cumulée (1904–2025) par Département",
)

fig.add_trace(
    go.Choropleth(
        geojson=gdf.__geo_interface__,
        locations=gdf["nom"],
        z=[0] * len(gdf),
        featureidkey="properties.nom",
        colorscale=[[0, "#f5f5f5"], [1, "#f5f5f5"]],
        showscale=False,
        marker_line_color="rgba(0, 0, 0, 0.45)",
        marker_line_width=1,
        hoverinfo="skip",
    )
)

fig.data = (fig.data[1], fig.data[0])

fig.update_geos(
    visible=False,
    lonaxis_range=[-9.0, 10.5],
    lataxis_range=[41.0, 51.5],
)

fig.update_layout(
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
)

st.plotly_chart(fig, use_container_width=True)