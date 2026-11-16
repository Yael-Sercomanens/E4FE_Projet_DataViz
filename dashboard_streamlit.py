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

    st.header("Évolution dans le temps des installations au niveau National, régional et départemental.")
    
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
    
    dfSommeMaxPuisParAnnee = df[(df["region"].isin(regions)) & (df["departement"].isin(departements))].groupby("dateMiseEnService")["maxPuis"].agg(pd_operation).reset_index()
    
    dfSommeMaxPuisParAnnee["dateMiseEnService"] = dfSommeMaxPuisParAnnee["dateMiseEnService"].astype(str)
    
    if operation == "Nombre d'installations":
        dfSommeMaxPuisParAnnee = dfSommeMaxPuisParAnnee.rename(columns={"maxPuis": "nombre"})
    
    # Figure plotly
    
    fig1 = px.line(dfSommeMaxPuisParAnnee, x="dateMiseEnService", y=y_title)
    
    fig1.update_layout(
        xaxis_rangeslider_visible=True
    )
    
    st.plotly_chart(fig1)
    
