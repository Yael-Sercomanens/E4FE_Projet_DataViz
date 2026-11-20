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
from shapely.geometry import Polygon

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

    st.header("Évolution dans le temps des installations en fonction de la région et du département")

    st.markdown("Ce graphe linéaire permet de voir l'évolution des installations de production exploitées en fonction de la région et du département.")
    
    # Opérations
    
    operation = st.selectbox(
        "Choisir l'opération :",
        ["Somme", "Somme cumulée", "Nombre d'installations", "Nombre d'installations cumulé"]
    )
    
    if operation == "Somme":
        pd_operation = "sum"
        y_title = "maxPuis"
        y_label = "Puissance maximale installée (kW)"
    elif operation == "Somme cumulée":
        pd_operation = "sum"
        y_title = "maxPuis"
        y_label = "Puissance maximale cumulée (kW)"
    elif operation == "Nombre d'installations":
        pd_operation = "count"
        y_title = "nombre"
        y_label = "Nombre d'installations"
    elif operation == "Nombre d'installations cumulé":
        pd_operation = "count"
        y_title = "nombre"
        y_label = "Nombre d'installations cumulé"
    
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
    
    dfFig1 = df[(df["region"].isin(regions)) & (df["departement"].isin(departements))].groupby("dateMiseEnService")["maxPuis"].agg(pd_operation).reset_index()
    
    if operation == "Nombre d'installations":
        dfFig1 = dfFig1.rename(columns={"maxPuis": "nombre"})
    elif operation == "Somme cumulée":
        dfFig1["maxPuis"] = dfFig1.sort_values("dateMiseEnService")["maxPuis"].cumsum()
    elif operation == "Nombre d'installations cumulé":
        dfFig1 = dfFig1.rename(columns={"maxPuis": "nombre"})
        dfFig1["nombre"] = dfFig1.sort_values("dateMiseEnService")["nombre"].cumsum()


    # Figure plotly
    
    fig1 = px.line(
        dfFig1,
        x="dateMiseEnService",
        y=y_title,
        labels={
            "dateMiseEnService": "Année mise en service",
            y_title: y_label
        }
    )
    
    fig1.update_layout(
        xaxis_rangeslider_visible=True,
        separators=",",
    )
    
    st.plotly_chart(fig1)
    
with col2 :

    st.header("Évolution dans le temps des installations en fonction de la filière et de la technologie")

    st.markdown("Ce graphique à aires empilées permet de voir l'évolution des installations de production exploitées en fonction de la filière énergétique et de la technologie.")
    
    # Opérations
    
    operation2 = st.selectbox(
        "Choisir l'opération :",
        ["Somme", "Somme cumulée", "Nombre d'installations", "Nombre d'installations cumulé"],
        key="operation_2"
    )
    
    if operation2 == "Somme":
        pd_operation = "sum"
        y_title = "maxPuis"
        y_label = "Puissance maximale installée (kW)"
    elif operation2 == "Somme cumulée":
        pd_operation = "sum"
        y_title = "maxPuis"
        y_label = "Puissance maximale cumulée (kW)"
    elif operation2 == "Nombre d'installations":
        pd_operation = "count"
        y_title = "nombre"
        y_label = "Nombre d'installations"
    elif operation2 == "Nombre d'installations cumulé":
        pd_operation = "count"
        y_title = "nombre"
        y_label = "Nombre d'installations cumulé"
    
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
    
    une_seule_filiere = len(selection_filiere) == 1 and "Toutes" not in selection_filiere

    # 1. Préparation du filtre (remplacement des NaN pour ne pas perdre de lignes au groupby)
    df_filtre = df[
        (df["filiere"].isin(filires)) & (df["technologie"].isin(technologies))
    ].copy()
    df_filtre["technologie"] = df_filtre["technologie"].fillna("Non renseignée")

    # 2. Colonnes de regroupement selon le mode choisi
    cols_groupe = (
        ["dateMiseEnService", "filiere", "technologie"]
        if une_seule_filiere
        else ["dateMiseEnService", "filiere"]
    )
    cols_serie = ["filiere", "technologie"] if une_seule_filiere else ["filiere"]

    dfFig2 = (
        df_filtre
        .groupby(cols_groupe)["maxPuis"]
        .agg(pd_operation)
        .reset_index()
    )

    # 3. Gestion du renommage et du cumul (avec complétion des années vides)
    est_cumul = operation2 in ["Somme cumulée", "Nombre d'installations cumulé"]
    est_nombre = operation2 in ["Nombre d'installations", "Nombre d'installations cumulé"]

    if est_nombre:
        dfFig2 = dfFig2.rename(columns={"maxPuis": "nombre"})

    col_cible = "nombre" if est_nombre else "maxPuis"

    if est_cumul and not dfFig2.empty:
        annees = sorted(dfFig2["dateMiseEnService"].unique())
        series = dfFig2[cols_serie].drop_duplicates()
        grille = pd.DataFrame({"dateMiseEnService": annees}).merge(series, how="cross")

        dfFig2 = (
            grille
            .merge(dfFig2, on=cols_groupe, how="left")
            .fillna({col_cible: 0})
            .sort_values(cols_serie + ["dateMiseEnService"])
        )
        dfFig2[col_cible] = dfFig2.groupby(cols_serie)[col_cible].cumsum()
    else:
        dfFig2 = dfFig2.sort_values("dateMiseEnService")

    # 4. Figure Plotly
    if une_seule_filiere:
        fig2 = px.area(
            dfFig2,
            x="dateMiseEnService",
            y=y_title,
            color="filiere",
            pattern_shape="technologie",
            labels={
                "dateMiseEnService": "Année mise en service",
                y_title: y_label,
            },
        )
    else:
        fig2 = px.area(
            dfFig2,
            x="dateMiseEnService",
            y=y_title,
            color="filiere",
            labels={
                "dateMiseEnService": "Année mise en service",
                y_title: y_label,
            },
        )
    
    fig2.update_layout(
        xaxis_rangeslider_visible=True,
        legend=dict(
            orientation="h",
            maxheight=0.15,
        ),
        separators=",",
    )
    
    st.plotly_chart(fig2, key="chart_2")

#Partie Carte Choropleth

# Lecture fichier geojson
gdf = gpd.read_file("Donnees/departements-avec-outre-mer.geojson")

# Ajout du polygone Saint-Martin
poly_saint_martin = Polygon([
    (-63.1285, 18.0535),
    (-63.1360, 18.0555),
    (-63.1455, 18.0600),
    (-63.1535, 18.0645),
    (-63.1510, 18.0685),
    (-63.1400, 18.0715),
    (-63.1260, 18.0730),
    (-63.1165, 18.0705),
    (-63.1120, 18.0725),
    (-63.1030, 18.0680),
    (-63.0910, 18.0665),
    (-63.0845, 18.0685),
    (-63.0865, 18.0745),
    (-63.0815, 18.0825),
    (-63.0770, 18.0910),
    (-63.0695, 18.0975),
    (-63.0595, 18.1015),
    (-63.0525, 18.1080),
    (-63.0460, 18.1165),
    (-63.0385, 18.1245),
    (-63.0285, 18.1255),
    (-63.0210, 18.1210),
    (-63.0155, 18.1135),
    (-63.0195, 18.1070),
    (-63.0145, 18.1015),
    (-63.0165, 18.0920),
    (-63.0120, 18.0835),
    (-63.0145, 18.0755),
    (-63.0125, 18.0650),
    (-63.0165, 18.0575),
    (-63.0280, 18.0590),
    (-63.0410, 18.0615),
    (-63.0545, 18.0625),
    (-63.0675, 18.0580),
    (-63.0810, 18.0545),
    (-63.0950, 18.0560),
    (-63.1065, 18.0595),
    (-63.1160, 18.0550),
    (-63.1285, 18.0535),
])

gdf_sm = gpd.GeoDataFrame(
    {"code": ["978"], "nom": ["Saint-Martin"], "geometry": [poly_saint_martin]},
    crs=gdf.crs,
)
gdf = pd.concat([gdf, gdf_sm], ignore_index=True)

# Déplacement des outre-mers
drom_layout = {
    "978": {"target": (-7.5, 49.8), "scale": 1},   # Saint-Martin
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

# Sliders

st.header("Évolution dans le temps des installations par département en fonction de la filière et de la technologie")

st.markdown("""La carte permet de contextualiser géographiquement les informations que nous avons extraites. Nous pouvons y afficher au choix, en fonction de la période étudiée :
- La somme des puissances installées par département 
- Le nombre d’installations par département
""")

# Opérations

operation3 = st.selectbox(
    "Choisir l'opération :",
    ["Somme", "Nombre d'installations"],
    key="operation_3"
)

if operation3 == "Somme":
    pd_operation = "sum"
    y_title = "maxPuis"
    label_dict = {"maxPuis": "Puissance cumulée (kW)"}
elif operation3 == "Nombre d'installations":
    pd_operation = "count"
    y_title = "nombre"
    label_dict = {"maxPuis": "Nombre d'installations cumulé"}

# Configurations filières

liste_filieres2 = df["filiere"].unique().tolist()
options_filieres2 = ["Toutes"] + liste_filieres2

selection_filiere2  = st.multiselect(
    "Choisir la / les filières :",
    options_filieres2,
    default = ["Toutes"],
    key="selection_filiere2"
)

if "Toutes" in selection_filiere2:
    filires2 = liste_filieres2
else:
    filires2 = selection_filiere2

# Configurations technologies

liste_technologies2 = df[((df["filiere"].isin(filires2)))]["technologie"].unique().tolist()
options_technologies2 = ["Toutes"] + liste_technologies2

selection_technologie2  = st.multiselect(
    "Choisir la / les technologies :",
    options_technologies2,
    default = ["Toutes"],
    key="selection_technologie2"
)

if "Toutes" in selection_technologie2:
    technologies2 = liste_technologies2
else:
    technologies2 = selection_technologie2

# Tri du df en fonction des configurations

dfFig3_inter = df[(df["filiere"].isin(filires2)) & (df["technologie"].isin(technologies2))]

if(len(dfFig3_inter["dateMiseEnService"]) != 0) :
    annee_min = int(dfFig3_inter["dateMiseEnService"].min())
    annee_max = int(dfFig3_inter["dateMiseEnService"].max())
else:
    annee_min = 1904
    annee_max = 2025

plage_annees = st.slider(
    "Période de mise en service :",
    min_value=annee_min,
    max_value=annee_max,
    value=(annee_min, annee_max),
)

dfFig3 = dfFig3_inter[((dfFig3_inter["dateMiseEnService"]).astype(int) >= plage_annees[0]) & ((dfFig3_inter["dateMiseEnService"]).astype(int) <= plage_annees[1])].groupby("departement")["maxPuis"].agg(pd_operation).reset_index()

df_map = dfFig3.merge(
    gdf[["nom", "lat", "lon"]],
    left_on="departement",
    right_on="nom",
    how="inner",
)

len_all_dep = df_map["maxPuis"].sum()

fig = px.choropleth(
    df_map,
    geojson=gdf.__geo_interface__,
    locations="nom",
    featureidkey="properties.nom",
    color="maxPuis",
    hover_name="nom",
    hover_data={"nom": False, "maxPuis": ":.2f"},
    labels=label_dict,
    color_continuous_scale="Viridis",
    projection="mercator",
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

raw_label = label_dict["maxPuis"]
formatted_label = raw_label[:1].lower() + raw_label[1:]
total_txt = f"{len_all_dep:,.2f}".replace(",", "\u00a0").replace(".", ",")

fig.update_layout(
    title=dict(
        text=f"Somme {formatted_label} : {total_txt}",
        x=0.02,
        y=0.97,
        xanchor="left",
        yanchor="top",
        font=dict(size=18),
    ),
    margin={"r": 0, "t": 40, "l": 0, "b": 0},
    separators=",",
)

st.plotly_chart(fig, use_container_width=True)