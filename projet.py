# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 13:40:23 2026

@author: sercomay
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as io
import re
io.renderers.default = 'browser'
#io.renderers.default = 'svg'

import os
#os.chdir()

df_raw_2025 = pd.read_csv('Donnees/registre-national-installation-production-stockage-electricite-2025.csv', sep=';', encoding='utf-8')

df = df_raw_2025.copy()

print("---------- Affichage de df.infos() ----------")
print(df.info())
print("---------- Fin de df.infos() ----------")

print("\n---------- Affichage de df.dtypes() ----------")
print(df.dtypes)
print("---------- Fin de df.dtypes() ----------")   # Afficher les premières infos du dataset

############################ V1 - Raw ############################

print("\n\n\n ---------- Debut v1 ----------")

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")   # Afficher nombre d'éléments nul par colonne

sns.heatmap(df.isnull(), cbar=False)                    # Tracer la heatmap
plt.title("Valeurs manquantes v1")
plt.show()
############################ Fin V1 - Raw ############################


############################ V2 - Retirer colonnes manquants valeurs ############################

print("\n\n\n ---------- Debut v2 ----------")

print(len(df[df["dateDeraccordement"].notna()].index.tolist()))
df.drop(df[df["dateDeraccordement"].notna()].index.tolist(), axis = 0, inplace = True)  #drop lignes avec date de deraccordement
df.drop(df[df["maxPuis"] == 0].index.tolist(), axis = 0, inplace = True)  # drop lignes avec maxPuis = 0 car ne contribue pas à prod
df.drop(["energieAnnuelleGlissanteSoutiree", "puisMaxCharge", "puisMaxRacCharge", "combustible", "codeCombustible", "dateDeraccordement", "nbGroupes", "codeS3RENR", "typeStockage", "puisMaxInstalleeDisCharge"], axis = 1, inplace = True)
df["dateMiseEnService"] = pd.to_datetime(df["dateMiseEnService"]).dt.year # juste garder les années
df.drop(df[df["dateMiseEnService"] == 1900].index.tolist(), axis = 0, inplace = True)  # drop lignes avec maxPuis = 0 car ne contribue pas à prod



print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v2")
plt.show()

############################ Fin V2 - Retirer colonnes manquants valeurs ############################

############################ V3 - Retirer les colonnes non pertinentes ############################

print("\n\n\n ---------- Debut v3 ----------")

df.drop(["codeEICResourceObject", "codeIRIS", "codeINSEECommune", "commune", "codeEPCI", "EPCI", "codeINSEECommuneImplantation", "dateDebutVersion", "posteSource", "modeRaccordement", "codeFiliere", "codeTechnologie", "regime", "energieStockable", "capaciteReservoir", "hauteurChute", "productible", "debitMaximal", "codeGestionnaire", "gestionnaire", "energieAnnuelleGlissanteInjectee", "puisMaxInstallee", "puisMaxRac", "dateRaccordement","nomInstallation","dateMiseEnservice (format date)"], axis = 1, inplace = True)

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v3")
plt.show()

print(len(df.index.tolist()))

print("\n\n\n ---------- Debut v4 ----------")

############################ Fin V3 - Retirer les colonnes non pertinentes ############################

############################ V4 - Derniers petits ajustements ############################

df.drop(df[(df["departement"].isna()) & (df["filiere"] == "Autre")].index.tolist(), axis = 0, inplace = True)

print(len(df.index.tolist()))


df.loc[df["codeDepartement"] == "978", "departement"] = "Saint-Martin"
df.loc[df["codeDepartement"] == "978", "region"] = "Saint-Martin"

# on enleve les departements nan car il n'y en a seulement 50 sur une echelle de 115 000

df.drop(df[df["departement"].isna()].index.tolist(), axis = 0, inplace = True)

print(len(df.index.tolist()))

# on enleve maintenant les codes departement et region

df.drop(["codeDepartement", "codeRegion"], axis = 1, inplace = True)

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")

print(df[(df["filiere"]=="Bioénergies")]["technologie"].unique())
print(df[(df["filiere"]=="Solaire")]["technologie"].unique())
print(df[(df["filiere"]=="Thermique non renouvelable")]["technologie"].unique())


# Evaluation valeurs aberrantes pour maxPuissance

print(df["maxPuis"].unique())
sns.boxplot(y=df['maxPuis'])

############################ V4 - Derniers petits ajustements ############################
