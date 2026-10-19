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

df_raw_2019 = pd.read_csv('registre-national-installation-production-stockage-electricite-2019.csv', sep=';', encoding='utf-8')
df_raw_2020 = pd.read_csv('registre-national-installation-production-stockage-electricite-2020.csv', sep=';', encoding='utf-8')
df_raw_2021 = pd.read_csv('registre-national-installation-production-stockage-electricite-2021.csv', sep=';', encoding='utf-8')

