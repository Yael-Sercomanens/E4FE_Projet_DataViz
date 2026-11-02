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
print("---------- Fin de df.dtypes() ----------")

# V1 - raw

print("\n\n\n ---------- Debut v1 ----------")

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v1")
plt.show()

# V2 - on enleve les colonnes avec bcp de valeurs nan

print("\n\n\n ---------- Debut v2 ----------")

print(len(df[df["dateDeraccordement"].notna()].index.tolist()))
df.drop(df[df["dateDeraccordement"].notna()].index.tolist(), axis = 0, inplace = True)
df.drop(["energieAnnuelleGlissanteSoutiree", "puisMaxCharge", "puisMaxRacCharge", "combustible", "codeCombustible", "dateDeraccordement", "nbGroupes", "codeS3RENR", "typeStockage", "puisMaxInstalleeDisCharge"], axis = 1, inplace = True)

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v2")
plt.show()

# V3 - on enleve les colonnes qui ne concernent pas notre etude

print("\n\n\n ---------- Debut v3 ----------")

df.drop(["codeEICResourceObject", "codeIRIS", "codeINSEECommune", "commune", "codeEPCI", "EPCI", "codeINSEECommuneImplantation", "dateDebutVersion", "posteSource", "modeRaccordement", "codeFiliere", "codeTechnologie", "regime", "energieStockable", "capaciteReservoir", "hauteurChute", "productible", "debitMaximal", "codeGestionnaire", "gestionnaire", "energieAnnuelleGlissanteInjectee", "puisMaxInstallee", "puisMaxRac", "dateRaccordement"], axis = 1, inplace = True)

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v3")
plt.show()

print(len(df.index.tolist()))

print("\n\n\n ---------- Debut v4 ----------")

# V4 - data cleansing

df.drop(df[(df["departement"].isna()) & (df["filiere"] == "Autre")].index.tolist(), axis = 0, inplace = True)

print(len(df.index.tolist()))


df.loc[df["codeDepartement"] == "978", "departement"] = "Saint-Martin"
df.loc[df["codeDepartement"] == "978", "region"] = "Saint-Martin"

# on eleve les departements nan car il n'y en a seulement 50 sur une echelle de 115 000

df.drop(df[df["departement"].isna()].index.tolist(), axis = 0, inplace = True)

print(len(df.index.tolist()))

# on eleve maintenant les codes departement et region

df.drop(["codeDepartement", "codeRegion"], axis = 1, inplace = True)

print("\n---------- Affichage de df.isna().sum() ----------")
print(df.isna().sum())
print("---------- Fin de df.isna().sum() ----------")