import csv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter 


def menu():
    try:
        opcion = int(input("""
        Menu principal.
        Selecciona una de las opciones.
        1. Análisis de estrategia por rutas de importacion y exportacion.
        2. Análisis de estrategia de medios de transporte utilizados.
        3. Análisis de estrategia de Valores generados por cada país.
        """))
    except:
        print("Selecciona una opción válida.")
        main()   
    if(opcion > 0 and opcion < 4):
        return opcion
    else:
        print("Entrada no válida")
        main()

def header():
    print("""
|||| ||||  ||   || ||||| |||||| |||||| ||    ||    ||   |||||| |||||| ||    || |||| |||| |||| |||| ||||     |||||||||||||
||    ||   |||  || ||	 ||  || ||      ||  ||     ||   ||  || ||      ||  ||  ||    ||   ||  ||   ||       ||||||||||||| |||||||
||||  ||   || | || ||||  |||||| || |||   ||||      ||   ||  || || |||   ||||   ||||  ||   ||  ||   ||||     ||||||||||||| |||||||
  ||  ||   ||  ||| ||	 || ||  ||  ||    ||       ||   ||  || ||  ||    ||      ||  ||   ||  ||     ||     ||||||||||||| |||||||
|||| ||||  ||   || ||||| ||  || ||||||    ||       |||| |||||| ||||||    ||    ||||  ||  |||| |||| ||||      (__)           (__)
""")

def rutas_mas_demandadas(path):
    contador_rutas_exportacion = {}
    contador_rutas_importacion = {}

    with open(path,'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if(fila['direction'] == 'Exports'):
                clave = fila['origin'] + '-' + fila['destination']
                if(clave in contador_rutas_exportacion):
                    contador_rutas_exportacion[clave] += 1
                else:
                    contador_rutas_exportacion[clave] = 1
            if(fila['direction'] == 'Imports'):
                clave = fila['origin'] + '-' + fila['destination']
                if(clave in contador_rutas_importacion):
                    contador_rutas_importacion[clave] += 1
                else:
                    contador_rutas_importacion[clave] = 1


    contador_rutas_exportacion_ordenado = sorted(contador_rutas_exportacion.items(), key = lambda tupla: tupla[1], reverse= True)
    contador_rutas_importacion_ordenado = sorted(contador_rutas_importacion.items(), key = lambda tupla: tupla[1], reverse= True)
    diez_rutas_mas_demandadas_exportacion = contador_rutas_exportacion_ordenado[:10]
    diez_rutas_mas_demandadas_importacion = contador_rutas_importacion_ordenado[:10]

    return diez_rutas_mas_demandadas_exportacion,diez_rutas_mas_demandadas_importacion

def rutas_mas_total_valor(path):
    ruta_valor_total_exportaciones = {}
    ruta_valor_total_importaciones = {}
    with open(path,'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if(fila['direction'] == 'Exports'):
                clave = fila['origin'] + '-' + fila['destination']
                if(clave in ruta_valor_total_exportaciones):
                    ruta_valor_total_exportaciones[clave].append(fila['total_value'])
                else:
                     ruta_valor_total_exportaciones[clave] = [fila['total_value']]
            if(fila['direction'] == 'Imports'):
                clave = fila['origin'] + '-' + fila['destination']
                if(clave in ruta_valor_total_importaciones):
                    ruta_valor_total_importaciones[clave].append(fila['total_value'])
                else:
                     ruta_valor_total_importaciones[clave] = [fila['total_value']]

    ruta_valor_suma_total_exportaciones = {}
    for clave, lista in ruta_valor_total_exportaciones.items():
        contador = 0
        for elemento in lista:
            contador += int(elemento)
        ruta_valor_suma_total_exportaciones[clave] = contador
    ruta_valor_suma_total_importaciones = {}
    for clave, lista in ruta_valor_total_importaciones.items():
        contador = 0
        for elemento in lista:
            contador += int(elemento)
        ruta_valor_suma_total_importaciones[clave] = contador
    
    sorted_ruta_valor_suma_total_exportaciones = sorted(ruta_valor_suma_total_exportaciones.items(), key = lambda tupla: tupla[1], reverse= True)
    sorted_ruta_valor_suma_total_importaciones = sorted(ruta_valor_suma_total_importaciones.items(), key = lambda tupla: tupla[1], reverse= True)

    return sorted_ruta_valor_suma_total_exportaciones[:10], sorted_ruta_valor_suma_total_importaciones[:10]

def medios_transporte(path):
    medios_de_transporte_valores = {}

    with open(path,'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if(fila['transport_mode'] in medios_de_transporte_valores):
                medios_de_transporte_valores[fila['transport_mode']].append(fila['total_value'])
            else:
                medios_de_transporte_valores[fila['transport_mode']] = [fila['total_value']]

    medio_transporte_total = {}
    for clave, lista in medios_de_transporte_valores.items():
        contador = 0
        for elemento in lista:
            contador += int(elemento)

        medio_transporte_total[clave] = contador

    sorted_medio_transporte_total = sorted(medio_transporte_total.items(), key = lambda tupla: tupla[1], reverse= True)
    return sorted_medio_transporte_total

def pais_valores_totales(path):
    with open(path, 'r') as archivo:
        suma_total_valores = 0
        paises_valores = {}
        lector = csv.DictReader(archivo)
        for fila in lector:
            if(fila['direction'] == 'Exports'):
                suma_total_valores += int(fila['total_value'])
                if(fila['origin'] in paises_valores):
                    paises_valores[fila['origin']].append(fila['total_value'])
                else:
                    paises_valores[fila['origin']] = [fila['total_value']]
            if(fila['direction'] == 'Imports'):
                suma_total_valores += int(fila['total_value'])
                if(fila['destination'] in paises_valores):
                    paises_valores[fila['destination']].append(fila['total_value'])
                else:
                    paises_valores[fila['destination']] = [fila['total_value']]
        
        valores_por_pais = {}
        for clave, lista in paises_valores.items():
            contador = 0
            for elemento in lista:
                contador += int(elemento)

            valores_por_pais[clave] = contador
        
        sorted_valores_por_pais = sorted(valores_por_pais.items(), key = lambda tupla: tupla[1], reverse=True)
        
        return sorted_valores_por_pais, suma_total_valores



def main():
    header()
    opcion = menu()
    if(opcion == 1):
        rutas_mayor_demanda_exportacion, rutas_mayor_demanda_importacion = rutas_mas_demandadas('./synergy_logistics_database.csv')

        header()
        print("""
        Las diez rutas de exportación con mayor demanda.
        """)

        for ruta in rutas_mayor_demanda_exportacion:
            print(f'Ruta: {ruta[0]}, Frecuencia: {ruta[1]}')
        
        print("""
        Las diez rutas de importación con mayor demanda.
        """)
        for ruta in rutas_mayor_demanda_importacion:
            print(f'Ruta: {ruta[0]}, Frecuencia: {ruta[1]}')
        
        plt.rcParams.update({'font.size': 8})
        fig, ax = plt.subplots(2)
        ax[0].bar([pais for pais,frecuencia in rutas_mayor_demanda_exportacion], [frecuencia for pais,frecuencia in rutas_mayor_demanda_exportacion], color = "blue")
        ax[0].tick_params(labelrotation=90)
        ax[0].set_title("Las 10 rutas de exportación más demandadas (del año 2015 al año 2020)")
        ax[0].set_xlabel("Rutas")
        ax[0].set_ylabel("Frecuencia")
        ax[1].bar([pais for pais,frecuencia in rutas_mayor_demanda_importacion], [frecuencia for pais,frecuencia in rutas_mayor_demanda_importacion], color = "orange")
        ax[1].set_title("Las 10 rutas de importación más demandadas (del año 2015 al año 2020)")
        ax[1].set_xlabel("Rutas")
        ax[1].set_ylabel("Frecuencia")
        ax[1].tick_params(labelrotation=90)
        plt.subplots_adjust(hspace = 2)
        plt.show()

        rutas_exportacion_mayor_valor, rutas_importacion_mayor_valor = rutas_mas_total_valor('./synergy_logistics_database.csv')
        header()
        print("""
        Las diez rutas de exportación que han generado mayor valor.
        """)

        for ruta in rutas_exportacion_mayor_valor:
            print(f'Ruta: {ruta[0]}, Valor: ${ruta[1]}')
    

        fig, ax_2 = plt.subplots(2)
        ax_2[0].bar([pais for pais,valor in rutas_exportacion_mayor_valor], [valor for pais,valor in rutas_exportacion_mayor_valor], color = "blue")
        ax_2[0].tick_params(labelrotation=90)
        plt.subplots_adjust(hspace=0.5)
        ax_2[0].set_title("Las 10 rutas de exportación con mayor valor.")
        ax_2[0].set_xlabel("Rutas")
        ax_2[0].set_ylabel("Valor")

        print("""
        Las diez rutas de importación que han generado mayor valor.
        """)

        for ruta in rutas_importacion_mayor_valor:
            print(f'Ruta: {ruta[0]}, Valor: ${ruta[1]}')
        
        ax_2[1].bar([pais for pais,frecuencia in rutas_importacion_mayor_valor], [valor for pais,valor in rutas_importacion_mayor_valor], color = "orange")
        ax_2[1].set_title("Las 10 rutas de importación con mayor valor")
        ax_2[1].set_xlabel("Rutas")
        ax_2[1].set_ylabel("Valor")
        ax_2[1].tick_params(labelrotation=90)
        plt.show()

    if(opcion == 2):
        medios_transporte_por_valores_totales = medios_transporte('./synergy_logistics_database.csv')
        header()
        print("""
        Importe total por medios de transporte (del año 2015 al año 2020).
        """)
        for medio in medios_transporte_por_valores_totales:
            print(f'Medio de transporte: {medio[0]}, importe total: ${medio[1]}')

        plt.bar([medio for medio,valor in medios_transporte_por_valores_totales], [valor for medio,valor in medios_transporte_por_valores_totales] )
        plt.title("Importe total por medios de transporte (del año 2015 al año 2020).")
        plt.xlabel("Medio de transporte")
        plt.ylabel("Importe total")
        plt.show()
    
    if(opcion == 3):

        valores_paises, suma_total_valores = pais_valores_totales('./synergy_logistics_database.csv')
        
        proporcion = 0
        paises_80_porciento = []
        ojiva = []
        for pais, valor in valores_paises:
            if(proporcion < 80):
                paises_80_porciento.append(pais)
                proporcion += (valor / suma_total_valores) * 100
            if(len(ojiva) == 0):
                ojiva.append(((valor / suma_total_valores) * 100))
            else:
                ojiva.append(ojiva[-1] + ((valor / suma_total_valores) * 100))
                 
                
        print(ojiva)
        print(suma_total_valores)
        print(paises_80_porciento)

        header()
        print("""
        Valores generados por pais.
        """)

        for valor, porcentaje in zip(valores_paises, ojiva):
            print(f'País: {valor[0]}, Valor total: ${valor[1]}, Porcentaje acumulado: %{round(porcentaje,2)}')

        print("""
        Lista de países que generan el 80% del valor de las exportaciones e importaciones
        """)

        for i, pais in enumerate(paises_80_porciento):
            print(f'{i+1}. {pais}')

        fig, ax = plt.subplots()
        ax.bar([pais for pais,valor in valores_paises], [valor for pais,valor in valores_paises])
        ax.tick_params(labelrotation=90)
        ax_ojiva = ax.twinx()
        ax_ojiva.plot([pais for pais,valor in valores_paises], ojiva, color='orange')
        ax_ojiva.yaxis.set_major_formatter(PercentFormatter())
        ax.set_title('Diagrama de Pareto de valores totales generados por país (del año 2015 al año 2020)')
        ax.set_xlabel("País")
        ax.set_ylabel("Valor total")
        plt.show()


        
main()

