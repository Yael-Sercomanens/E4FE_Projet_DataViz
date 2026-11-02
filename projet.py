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

df_raw_2019 = pd.read_csv('Donnees/registre-national-installation-production-stockage-electricite-2019.csv', sep=';', encoding='utf-8')
df_raw_2020 = pd.read_csv('Donnees/registre-national-installation-production-stockage-electricite-2020.csv', sep=';', encoding='utf-8')
df_raw_2021 = pd.read_csv('Donnees/registre-national-installation-production-stockage-electricite-2021.csv', sep=';', encoding='utf-8')

df_2019 = df_raw_2019.copy()
df_2019.insert(0, "Annee", 2019)
df_2019.rename(columns={"energieAnnuelleInjectee": "energieAnnuelleGlissanteInjectee"}, inplace = True)
df_2019.rename(columns={"energieAnnuelleSoutiree": "energieAnnuelleGlissanteSoutiree"}, inplace = True)

df_2020 = df_raw_2020.copy()
df_2020.insert(0, "Annee", 2020)

df_2021 = df_raw_2021.copy()
df_2021.insert(0, "Annee", 2021)
df_2021.drop(["puisMaxInstalleeDisCharge", "typeStockage"], axis = 1, inplace = True)

df = pd.concat([df_2019, df_2020, df_2021], ignore_index=True)

print(df.info())
print(df.dtypes)
print(df.isna().sum())

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v1")
plt.show()

print(len(df[df["dateDeraccordement"].notna()].index.tolist()))
df.drop(df[df["dateDeraccordement"].notna()].index.tolist(), axis = 0, inplace = True)
df.drop(["energieAnnuelleGlissanteSoutiree", "puisMaxCharge", "puisMaxRacCharge", "combustible", "codeCombustible", "dateDeraccordement", "nbGroupes", "codeS3RENR"], axis = 1, inplace = True)

sns.heatmap(df.isnull(), cbar=False)
plt.title("Valeurs manquantes v2")
plt.show()