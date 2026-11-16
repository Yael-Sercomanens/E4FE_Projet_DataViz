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

print("\n ---------- Debut v1 ----------")

sns.heatmap(df.isnull(), cbar=False)                    # Tracé la heatmap pour visualiser v1
plt.title("Valeurs manquantes v1")
plt.show()

print("V1 - Nombre d'éléments nuls restants\n")
print(df.isna().sum())  #Afficher le nombre d'éléments nuls restants

print("\n ---------- Fin v1 ----------")

############################ Fin V1 - Raw ############################


############################ V2 - Retirer colonnes manquants valeurs ############################

print("\n ---------- Debut v2 ----------")

print("\nNombre de lignes avec date de déraccordement : " + str(len(df[df["dateDeraccordement"].notna()].index.tolist())))     #Afficher le nombre d'éléments déraccordé
df.drop(df[df["dateDeraccordement"].notna()].index.tolist(), axis = 0, inplace = True)                                  #Drop les lignes avec une date deraccordement

print("\nNombre de lignes avec un type de stockage : " + str(len(df[df["typeStockage"].notna()].index.tolist())))           #Afficher le nombre d'éléments de stockage
df.drop(df[df["typeStockage"].notna()].index.tolist(), axis = 0, inplace = True)                                        #Drop les lignes concernant des éléments de stockage

df.drop(df[df["maxPuis"] == 0].index.tolist(), axis = 0, inplace = True)                                                #Drop les lignes avec maxPuis = 0 car ne contribue pas à prod
df["dateMiseEnService"] = pd.to_datetime(df["dateMiseEnService"]).dt.year                                               #Homogénéiser pour uniquement garder les années
df.drop(df[df["dateMiseEnService"] == 1900].index.tolist(), axis = 0, inplace = True)                                   #Drop les lignes done l'année est 1900 car sont des valeurs par défaut étrange

# Drop les colonnes non pertinentes avec ce que nous voulons montrer
df.drop(["energieAnnuelleGlissanteSoutiree", "puisMaxCharge", "puisMaxRacCharge", "combustible", "codeCombustible", "dateDeraccordement", "nbGroupes", "codeS3RENR", "typeStockage", "puisMaxInstalleeDisCharge"], axis = 1, inplace = True)

print("V2 - Nombre d'éléments nuls restants\n")
print(df.isna().sum())                                                          #Afficher le nombre d'éléments nuls restants

sns.heatmap(df.isnull(), cbar=False)                                            #Tracé de la heatmap après suppression de valeurs et de colonnes v2
plt.title("Valeurs manquantes v2")
plt.show()

print("\nV2 - Nombre de lignes restantes")
print(len(df.index.tolist()))           
print("\n ---------- Fin v2 ----------")

############################ Fin V2 - Retirer colonnes manquants valeurs ############################

############################ V3 - Retirer les colonnes non pertinentes ############################

print("\n ---------- Debut v3 ----------")

#Drop les colonnes qui ne permettent pas d'afficher les informations de façon claire
df.drop(["codeEICResourceObject", "codeIRIS", "codeINSEECommune", "commune", "codeEPCI", "EPCI", "codeINSEECommuneImplantation", "dateDebutVersion", "posteSource", "modeRaccordement", "codeFiliere", "codeTechnologie", "regime", "energieStockable", "capaciteReservoir", "hauteurChute", "productible", "debitMaximal", "codeGestionnaire", "gestionnaire", "energieAnnuelleGlissanteInjectee", "puisMaxInstallee", "puisMaxRac", "dateRaccordement","nomInstallation","dateMiseEnservice (format date)"], axis = 1, inplace = True)

print("V3 - Nombre d'éléments nuls restants\n")
print(df.isna().sum())                                                          #Afficher le nombre d'éléments nuls restants

sns.heatmap(df.isnull(), cbar=False)                                            #Tracé de la heatmap v3
plt.title("Valeurs manquantes v3")
plt.show()

print("\nV3 - Nombre de lignes restantes")
print(len(df.index.tolist()))            
print("\n ---------- Fin v3 ----------")

############################ Fin V3 - Retirer les colonnes non pertinentes ############################

############################ V4 - Derniers petits ajustements ############################

print("\n ---------- Debut v4 ----------")

df.drop(df[(df["departement"].isna()) & (df["filiere"] == "Autre")].index.tolist(), axis = 0, inplace = True)   # Drop les lignes dont le département est manquant et que la filière est autre
    
df.loc[df["codeDepartement"] == "978", "departement"] = "Saint-Martin" 
df.loc[df["codeDepartement"] == "978", "region"] = "Saint-Martin"               # Set la région et le département si le code est 978 (quelques valeurs précises)

df.drop(df[df["departement"].isna()].index.tolist(), axis = 0, inplace = True)  # Suppression des lignes sans département car information importante ET petit nombre de lignes                          


df.drop(["codeDepartement", "codeRegion"], axis = 1, inplace = True)            #Enlever les codes de département car moins parlant que leur nom

df["technologie"] = df["technologie"].fillna("Inconnu")                         # Information importante, remplace les manquantes par "Inconnu"

print("V4 - Nombre d'éléments nuls restants\n")
print(df.isna().sum())                                                          #Afficher le nombre d'éléments nuls restants

sns.boxplot(y=df['maxPuis'])                                                    # Tracé du boxplot pour voir les valeurs aberrantes

print("\nV4 - Nombre de lignes restantes")
print(len(df.index.tolist()))
print("\n ---------- Fin v4 ----------")

############################ V4 - Derniers petits ajustements ############################
