#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 08:15:11 2022

@author: hugoarellano
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import xlrd
import plotly.graph_objects as go
import gspread
import df2gspread as d2g
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image

#Configurando nombre e incono en pestaña
st.set_page_config(page_title= 'Procesador de datos test financiero',
                    page_icon= 'https://lh3.googleusercontent.com/a-/AFdZucprIXKIX0aMFJAJ8ut_Sfc-CbDMnF-9jP2doxkA=s83-c-mo')

image = Image.open('fint_logo_amplio.png')

#Título y próposito de la aplicación
st.image(image)
st.title('Procesador de datos test financiero')
st.markdown('#### Esta aplicación tiene como propósito obtener los puntajes generales y por área del test financiero')



#llamando los datos a procesar
#cargando secrets
gc = gspread.service_account('testfint-secrets.json')

spreadsheet = gc.open('copy_fint_test_130922')
worksheet1 = spreadsheet.get_worksheet(0)

df = pd.DataFrame(worksheet1.get_all_records())

#La columna dependientes tiene tipos de dato mixtos, convertimos todos a texto para evitar errores 
df['Dependientes'] = df['Dependientes'].astype(str)


# #Llamando los datos a procesar
# url = "https://docs.google.com/spreadsheets/d/1stCoEqffrsHMmFqvqPVYxGGTksG4Q-YHvaFIR2HIO6I/gviz/tq?tqx=out:csv&sheet=Respuestas"
# df = pd.read_csv(url)

#Ver los datos antes del procesamiento
st.markdown('#### Aquí puedes observar los datos antes de ser procesados')
if st.checkbox('Datos sin procesar'):
    st.write(df)


#Procesando los datos
#importando funciones diseñadas por el usuario
from finT_score_processingv2 import preprocesamiento, asignacion_clave_valor, pts_area

df_preprocesado = preprocesamiento(df)
df_clave_valor = asignacion_clave_valor(df_preprocesado)
df_puntos = pts_area(df_clave_valor)
df_puntos = df_puntos.round(2)

#Mostrando los datos procesados 
st.markdown('#### Selecciona la casilla y procesa los datos')
if st.checkbox('Procesar datos'):
    st.write(df_puntos)


#Ultimando detalles para enviar los datos procesados a google drive
scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

credentials = Credentials.from_service_account_file('testfint-secrets.json', scopes=scopes)
gc = gspread.authorize(credentials)

gauth = GoogleAuth()
drive = GoogleDrive(gauth)

# open a google sheet
gs = gc.open_by_key('1bDq0wGZ4TTW0txw3O6evXcoMSYIkGh-QrvMjyWKfUhw')
worksheet_datos_pro = gs.worksheet('Sheet1')


#write dataframe
#worksheet_datos_pro.clear()

st.markdown('#### Envíar datos a google sheets')
st.write('Haz click en el siguiente botón para envíar los datos a google sheets')

if st.button('Subir datos'):
    worksheet_datos_pro.clear()
    set_with_dataframe(worksheet=worksheet_datos_pro, dataframe=df_puntos,
                        include_index=False, 
                        include_column_header=True, resize=True)
    st.write('¡Los datos han sido actualizados satisfactoriamente!')



