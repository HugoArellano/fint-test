# -*- coding: utf-8 -*-
"""
Spyder Editor
Created by Hugo Arellano 
This is a temporary script file.
"""

def preprocesamiento(df):
    """
    Esta función se encarga del procesamiento de datos del test financiero
    """
    import numpy as np
    #Eliminar las columnas que no se necesitan para el calculo del score
    df = df.drop(columns=['Teléfono', 'Email', 'Referido'])
    
    num_users = len(df)

    start_user = 1001

    end_user = (start_user + num_users) -1

    df['usuario'] = np.linspace(start_user, end_user, num_users).astype(int)
    
    #transformando nombres de columnas a minusculas
    df.columns = df.columns.str.lower()
    
    #asignando nuevos nombres a las columnas 
    df = df.rename(columns= {'ingreso único': 'ingreso_unico','casa propia': 'propiedad_casa', 'auto propio':'propiedad_auto', 'preocupado $$':'estres_dinero',
                   'deudas':'deuda_gen', 'pide prestado': 'deuda_def', 'compra x impulso':'ahorro_compras', 
                    'gastos mensuales': 'gasto_mes', '% pago deudas': 'deuda_dti', 'instrumentos de crédito':'deuda_instru',
                   'ingresos':'ingreso_mes', '% de ahorro':'ahorro_disciplina', 'sobrevivir':'ahorro_desempleo',
                   'ahorro p/retiro':'ahorro_retiro', 'conceptos económicos':'inversion_conceptos', 'inversiones':'inversion_fin', 
                    'otras inversiones': 'inversion_nofin' 
                   })
    
    #reordenando las columnas
    df = df.reindex(columns=['usuario','nombre', 'edad', 'dependientes', 'ingreso_mes',
                         'ingreso_unico', 'propiedad_casa','propiedad_auto','estres_dinero',
                         'deuda_gen', 'deuda_def', 'deuda_dti', 'deuda_instru', 'ahorro_compras',
                         'ahorro_disciplina', 'ahorro_desempleo', 'ahorro_retiro', 
                         'inversion_conceptos', 'inversion_fin', 'inversion_nofin', 'gasto_mes'
                        ])
    
    #Llena los valores nulos con cero (0)
    df = df.fillna(0)
    
    #selección de columnas de texto, 
    cols_cat = df.select_dtypes(['object']).columns

    #transformación a minúsculas de las respuestas
    df[cols_cat] = df[cols_cat].apply(lambda x: x.astype(str).str.lower())

    #Eliminación de acentos
    df[cols_cat] = df[cols_cat].apply(lambda x: x.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8'))

    
    return df

##################################################################33

def asignacion_clave_valor(df):
    
    """
    Esta función asigna valores númericos a las respuestas del test financiero, de conformidad 
    el diccionario de datos, se encuentra organizada por área
    """
    import numpy as np
    
    #Propiedad e ingresos
    
    
    df['propiedad_casa'] = df['propiedad_casa'].replace({'rento': 1, 'casa propia (hipotecada)': 3, 'casa propia (100% pagada)':5,
                                                     'prestada / con mis papas': 2})
    
    df['propiedad_auto'] = df['propiedad_auto'].replace({'si (100% pagado)': 3,  'lo estoy pagando': 2, 'no tengo':1})

    df['ingreso_mes'] = df['ingreso_mes'].replace({'menos de $20,000 mxn':2 , 'entre $20,000 y $40,000 mxn': 3 , 'mas de $40,000 mxn': 4})

    df['ingreso_unico'] = df['ingreso_unico'].replace({'si':1.5, 'no, mi pareja tambien aporta':2})
    
    #estres
    df['estres_dinero'] = df['estres_dinero'].replace({1:10, 2:9, 3:8, 4:7, 5:6,6:5, 7:4, 8:3, 9:2, 10:1})
    
    #Deuda
    # df['deuda_def'] = np.where(df['deuda_def'] =='',0, 
    #                                df['deuda_def']).astype(int)
    
    df['deuda_def'] = df['deuda_def'].replace({'nunca lo hago':5, 'son contadas las veces': 2.5 , 'lo hago frecuentemente':1})

    df['deuda_gen'] = df['deuda_gen'].replace({'no tengo deudas':5, 'si tengo pero estoy al corriente':3 , 'estoy super endeudado':1})

    df['deuda_dti'] = df['deuda_dti'].replace({'ninguno': 5 , 'menos del 20%': 4 , 'entre el 20 y 50%': 2.5 , 'mas del 50%': 1})

    df['deuda_instru'] = df['deuda_instru'].replace({'nunca los utilizo, siempre pago de contado': 2,
                                                    'los utilizo cuando puedo pagar a meses sin intereses': 4 ,
                                                    'los utilizo para hacer compras grandes: auto, casa, etc.': 3 , 
                                                     'los utilizo para todo y pago mucho de intereses': 1,
                                                     'los utilizo cuando puedo pagar a meses sin intereses, los utilizo para hacer compras grandes: auto, casa, etc.':3.5,
                                                     'nunca los utilizo, siempre pago de contado, los utilizo cuando puedo pagar a meses sin intereses': 3,
                                                     'los utilizo cuando puedo pagar a meses sin interes, los utilizo para todo y pago mucho de intereses': 1.5,
                                                     'los utilizo para hacer compras grandes: auto, casa, etc, los utilizo para todo y pago mucho de intereses': 1.5,
                                                     'los utilizo cuando puedo pagar a meses sin intereses, los utilizo para hacer compras grandes: auto, casa, etc, los utilizo para todo y pago mucho de intereses': 1.5,
                                                     'nunca los utilizo, siempre pago de contado, los utilizo para hacer compras grandes: auto, casa, etc., los utilizo casi para todo y pago mucho de intereses': 1.5 })
    
    #Ahorro
    df['ahorro_disciplina'] = df['ahorro_disciplina'].replace({'nada': 1, 'entre el 5 y 10%': 2 , 'entre el 10 y 20%': 3.5, 'mas del 20%': 5})

    df['ahorro_desempleo'] = df['ahorro_desempleo'].replace({'menos de 1 mes': 1 , 'entre 1 y 3 meses': 3 , 'mas de 3 meses': 5 })

    # df['ahorro_compras'] = np.where(df['ahorro_compras'] =='',0, 
    #                                 df['ahorro_compras']).astype(int)
    
    df['ahorro_compras'] = df['ahorro_compras'].replace({'nunca lo hago': 3, 'son contadas las veces':2 , 'lo hago frecuentemente': 1})
    

    # df['ahorro_retiro'] = np.where(df['ahorro_retiro'] =='',0, 
    #                                df['ahorro_retiro']).astype(int)
                                                   
    df['ahorro_retiro'] = df['ahorro_retiro'].replace({'si, tengo bastante ahorrado': 5 , 'si, pero es poco lo que tengo': 2.5 , 'todavia no empiezo':1, '':0})
    
    #Inversión
    df['inversion_conceptos'] = df['inversion_conceptos'].replace({'no se de que me estas hablando': 1 , 'los he escuchado pero no los entiendo': 1.7 ,
                                                                  'los conozco a la perfeccion': 3 })

    df['inversion_fin'] = df['inversion_fin'].replace({'nada': 1 , 'poco': 3 , 'bastante': 6 })

    df['inversion_nofin'] = df['inversion_nofin'].replace({'educacion y desarrollo personal/familiar': 2.5 ,
                                                           'negocio propio y/o propiedades': 2.5 , 'otro tipo de inversiones': 2,
                                                           'ninguna': 1, 'educacion y desarrollo personal/familiar, negocio propio y/o propiedades': 3,
                                                           'negocio propio y/o propiedades, otro tipo de inversiones': 2.2,
                                                           'educacion y desarrollo personal/familiar, otro tipo de inversiones': 2.2,
                                                           'educacion y desarrollo personal/familiar, ninguna': 1, 
                                                           'negocio propio y/o propiedades, ninguna': 1,
                                                           'otro tipo de inversiones, ninguna': 1,
                                                           'educacion y desarrollo personal/familiar, educacion y desarrollo personal/familiar, ninguna': 1,
                                                           'educacion y desarrollo personal/familiar, otro tipo de inversiones, ninguna': 1,
                                                           'educacion y desarrollo personal/familiar, negocio propio y/o propiedades, otro tipo de inversiones':3,

                                           })
    
   
    return df

#####################################################

def pts_area(df):
    
    import pandas as pd
    
    propingre_cols = ['propiedad_casa', 'propiedad_auto', 'ingreso_mes', 'ingreso_unico']
    #Area estrés es pregunta unitaria
    deuda_cols = ['deuda_gen', 'deuda_def', 'deuda_dti', 'deuda_instru']
    ahorro_cols = ['ahorro_compras','ahorro_disciplina', 'ahorro_desempleo', 'ahorro_retiro']
    inversion_cols = ['inversion_conceptos', 'inversion_fin', 'inversion_nofin']
    
    
    df[deuda_cols] = (df[deuda_cols]/20)*25
    df[propingre_cols] = (df[propingre_cols]/14)*15
    df[ahorro_cols] = (df[ahorro_cols]/18)*25
    df['pts_estres'] = df['estres_dinero']
    df[inversion_cols] = (df[inversion_cols]/12)*25
    
    dfpts = pd.DataFrame({})
    
    dfpts['usuario'] = df['usuario']
    dfpts['nombre'] = df['nombre']
    dfpts['edad'] = df['edad']
    dfpts['dependientes'] = df['dependientes']
    dfpts['pts_propingre'] = df[propingre_cols].sum(axis=1)
    dfpts['pts_estres'] = df['pts_estres']
    dfpts['pts_deuda'] = df[deuda_cols].sum(axis=1)
    dfpts['pts_ahorro'] = df[ahorro_cols].sum(axis=1)
    dfpts['pts_inversion'] = df[inversion_cols].sum(axis=1)
    
    pts_cols = ['pts_propingre','pts_estres', 'pts_deuda', 'pts_ahorro', 'pts_inversion']
    
    dfpts['pts_pretotal'] = dfpts[pts_cols].sum(axis=1)
    
    def normalizacion(df):
        return(df - 16) / (100 - 16)*100
    
    dfpts['total_score'] = normalizacion(dfpts['pts_pretotal'])
    
    propingre_min = (4/14)*15
    propingre_max = 15

    estres_min = 1
    estres_max = 10

    deuda_min = (3/20)*25
    deuda_max = 25

    ahorro_min = (4/18)*25
    ahorro_max = 25

    inversion_min = (3/12)*25
    inversion_max = 25
    
    def norm_area(df,a_min,a_max):
        return((df - a_min) / (a_max - a_min)) * 100
    
    dfpts['sco_propingre'] = norm_area(dfpts['pts_propingre'], propingre_min, propingre_max)
    dfpts['sco_estres'] = norm_area(dfpts['pts_estres'], estres_min, estres_max)
    dfpts['sco_deuda'] = norm_area(dfpts['pts_deuda'], deuda_min, deuda_max)
    dfpts['sco_ahorro'] = norm_area(dfpts['pts_ahorro'], ahorro_min, ahorro_max)
    dfpts['sco_inversion'] = norm_area(dfpts['pts_inversion'], inversion_min, inversion_max)
    
    dfpts = dfpts.reindex(columns=['usuario', 'nombre', 'edad', 'dependientes', 'pts_propingre',
                            'pts_estres', 'pts_deuda', 'pts_ahorro', 'pts_inversion',
                            'sco_propingre', 'sco_estres','sco_deuda', 'sco_ahorro', 'sco_inversion',
                            'pts_pretotal', 'total_score'
                           ])
    
    return dfpts