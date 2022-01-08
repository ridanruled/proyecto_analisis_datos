import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter 

# Función para el menú principal
def menu():
    # Solicita la entrada de una opción para el menu
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

# Función que imprime el encabezado del nombre de la empresa.
def header():
    print("""
|||| ||||  ||   || ||||| |||||| |||||| ||    ||    ||   |||||| |||||| ||    || |||| |||| |||| |||| ||||     |||||||||||||
||    ||   |||  || ||	 ||  || ||      ||  ||     ||   ||  || ||      ||  ||  ||    ||   ||  ||   ||       ||||||||||||| |||||||
||||  ||   || | || ||||  |||||| || |||   ||||      ||   ||  || || |||   ||||   ||||  ||   ||  ||   ||||     ||||||||||||| |||||||
  ||  ||   ||  ||| ||	 || ||  ||  ||    ||       ||   ||  || ||  ||    ||      ||  ||   ||  ||     ||     ||||||||||||| |||||||
|||| ||||  ||   || ||||| ||  || ||||||    ||       |||| |||||| ||||||    ||    ||||  ||  |||| |||| ||||      (__)           (__)
""")

# Función que determina las rutas de exportación e importación más demandadas que recibe la ruta del archivo.
def rutas_mas_demandadas(path):
    contador_rutas_exportacion = {}
    contador_rutas_importacion = {}

    # Abre el archivo csv en mode lectura.
    with open(path,'r') as archivo:
        # Crea el objeto lector que transforma las filas del csv en diccionarios.
        lector = csv.DictReader(archivo)
        #Permite contar la frecuencia de cada ruta a través de un diccionario y controles de flujo.
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

    # Ordena de mayor a menor las rutas con su frecuencia
    contador_rutas_exportacion_ordenado = sorted(contador_rutas_exportacion.items(), key = lambda tupla: tupla[1], reverse= True)
    contador_rutas_importacion_ordenado = sorted(contador_rutas_importacion.items(), key = lambda tupla: tupla[1], reverse= True)
    
    # Selecciona las 10 primeras rutas.
    diez_rutas_mas_demandadas_exportacion = contador_rutas_exportacion_ordenado[:10]
    diez_rutas_mas_demandadas_importacion = contador_rutas_importacion_ordenado[:10]

    # Regresa las 10 rutas más demandas de exportación y las 10 rutas más demandas de importación.
    return diez_rutas_mas_demandadas_exportacion,diez_rutas_mas_demandadas_importacion

# Función que determina las rutas de exportación e importación que generan un mayor valor.
def rutas_mas_total_valor(path):
    # Diccionarios para guardar las rutas con sus valores.
    ruta_valor_total_exportaciones = {}
    ruta_valor_total_importaciones = {}

    # Abre el archivo csv en mode lectura.
    with open(path,'r') as archivo:
        lector = csv.DictReader(archivo)
        #Permite contar la frecuencia de cada ruta a través de un diccionario y controles de flujo.
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
    
    # Creación de diccionario que guardará la suma de los valores de cada ruta.
    ruta_valor_suma_total_exportaciones = {}

    # Ciclo for que permite iterar en cada elemento del diccionario para realizar la suma de los elementos de la lista en el valor de cada clave.
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
    
    # Ordena los diccionarios de mayor a menor de acuerdo con el valor.
    sorted_ruta_valor_suma_total_exportaciones = sorted(ruta_valor_suma_total_exportaciones.items(), key = lambda tupla: tupla[1], reverse= True)
    sorted_ruta_valor_suma_total_importaciones = sorted(ruta_valor_suma_total_importaciones.items(), key = lambda tupla: tupla[1], reverse= True)

    # Regresa las 10 rutas de exportación y las 10 rutas de importación con mayor valor.
    return sorted_ruta_valor_suma_total_exportaciones[:10], sorted_ruta_valor_suma_total_importaciones[:10]

# Función que determina el valor generado por cada medio de transporte
def medios_transporte(path):
    #Creación del diccionario que permite guardar cada medio de transporte con sus valores totales.
    medios_de_transporte_valores = {}

    # Abre el archivo csv en mode lectura.
    with open(path,'r') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            if(fila['transport_mode'] in medios_de_transporte_valores):
                medios_de_transporte_valores[fila['transport_mode']].append(fila['total_value'])
            else:
                medios_de_transporte_valores[fila['transport_mode']] = [fila['total_value']]

    # Creación de diccionario para guardar la suma de los valores de cada medio de transporte.
    medio_transporte_total = {}
    for clave, lista in medios_de_transporte_valores.items():
        contador = 0
        for elemento in lista:
            contador += int(elemento)

        medio_transporte_total[clave] = contador

    # Ordena el diccionario de acuerdo con sus valores.
    sorted_medio_transporte_total = sorted(medio_transporte_total.items(), key = lambda tupla: tupla[1], reverse= True)
    #Regresa los medios de transporte con sus valores.
    return sorted_medio_transporte_total

# Función que permite determinar el valor total generado por país.
def pais_valores_totales(path):
    #Crea diccionario que guardará los paises y una lista de los valores de cada país.
    paises_valores = {}
    # variable que sirve para sumar el valor total de todas las exportaciones e importaciones.
    suma_total_valores = 0

    # Abre el archivo csv en mode lectura.
    with open(path, 'r') as archivo:
        lector = csv.DictReader(archivo)
        #Permite contar el valor de cada país a través de un diccionario y controles de flujo.
        for fila in lector:
            # Se determina el valor de un país si este lo exportó o si este lo importó, ya que es el encargado de los costos.
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
        
        #Diccionario para guardar la suma de todos los valores de cada país.
        valores_por_pais = {}
        # Ciclo flor que permite sumar los valores de la lista de cada clave.
        for clave, lista in paises_valores.items():
            contador = 0
            for elemento in lista:
                contador += int(elemento)

            valores_por_pais[clave] = contador
        
        # Ordena el diccionario de mayor a menor de acuerdo con el valor de cada clave.
        sorted_valores_por_pais = sorted(valores_por_pais.items(), key = lambda tupla: tupla[1], reverse=True)
        
        # Regresa los valores de cada país y la suma de todos los valores.
        return sorted_valores_por_pais, suma_total_valores


# Función principal donde se lleva a cabo el programa.
def main():
    # Llama la función de header para imprimir nombre y logo de la empresa.
    header()
    # Llama la función menú para imprimir las opciones y que el usuario seleccione una opción.
    opcion = menu()
    # Ifs que permiten realizar las diferentes opciones disponibles en el menú.
    if(opcion == 1):
        # Llamado de la función que regresa las rutas más demandadas.
        rutas_mayor_demanda_exportacion, rutas_mayor_demanda_importacion = rutas_mas_demandadas('./synergy_logistics_database.csv')

        header()
        print("""
        Las diez rutas de exportación con mayor demanda.
        """)
        # Impresión de las rutas más demandadas.
        for ruta in rutas_mayor_demanda_exportacion:
            print(f'Ruta: {ruta[0]}, Frecuencia: {ruta[1]}')
        
        print("""
        Las diez rutas de importación con mayor demanda.
        """)
        for ruta in rutas_mayor_demanda_importacion:
            print(f'Ruta: {ruta[0]}, Frecuencia: {ruta[1]}')
        #Creación de la gráfica de barras de las rutas más demandadas.
        #Ajusta el tamaño de la letra de los titulos y etiquetas de los gráficos.
        plt.rcParams.update({'font.size': 8})

        # Permite generar un espacio de 2 elementos para colocar una gráfica en cada uno.
        fig, ax = plt.subplots(2)

        # Creación del gráfico de barras.
        ax[0].bar([pais for pais,frecuencia in rutas_mayor_demanda_exportacion], [frecuencia for pais,frecuencia in rutas_mayor_demanda_exportacion], color = "blue")
        # Ángulo de las etiquetas del eje x.
        ax[0].tick_params(labelrotation=90)
        # Titulo del gráfico
        ax[0].set_title("Las 10 rutas de exportación más demandadas (del año 2015 al año 2020)")
        #etiqueta eje x
        ax[0].set_xlabel("Rutas")
        # etiqueta eje y
        ax[0].set_ylabel("Frecuencia")
        ax[1].bar([pais for pais,frecuencia in rutas_mayor_demanda_importacion], [frecuencia for pais,frecuencia in rutas_mayor_demanda_importacion], color = "orange")
        ax[1].set_title("Las 10 rutas de importación más demandadas (del año 2015 al año 2020)")
        ax[1].set_xlabel("Rutas")
        ax[1].set_ylabel("Frecuencia")
        ax[1].tick_params(labelrotation=90)
        plt.subplots_adjust(hspace = 2)
        plt.show()

        # Impresión de las rutas con mayor valor.
        rutas_exportacion_mayor_valor, rutas_importacion_mayor_valor = rutas_mas_total_valor('./synergy_logistics_database.csv')
        header()
        print("""
        Las diez rutas de exportación que han generado mayor valor.
        """)

        for ruta in rutas_exportacion_mayor_valor:
            print(f'Ruta: {ruta[0]}, Valor: ${ruta[1]}')
    
        # Creación de las gráficas de barras de las rutas con mayor valor.
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
        # Llamado de la función que regresa los medios de transporte y sus importes totales
        medios_transporte_por_valores_totales = medios_transporte('./synergy_logistics_database.csv')
        # Llamado de la función para la impresión del nombre y logo de la empresa.
        header()

        # Impresión de los medios de transporte y su importe total.
        print("""
        Importe total por medios de transporte (del año 2015 al año 2020).
        """)
        for medio in medios_transporte_por_valores_totales:
            print(f'Medio de transporte: {medio[0]}, importe total: ${medio[1]}')

        # Creación de gráfico de barras de los medios de transporte y su importe total.
        plt.bar([medio for medio,valor in medios_transporte_por_valores_totales], [valor for medio,valor in medios_transporte_por_valores_totales] )
        plt.title("Importe total por medios de transporte (del año 2015 al año 2020).")
        plt.xlabel("Medio de transporte")
        plt.ylabel("Importe total")
        plt.show()
    
    if(opcion == 3):

        # Llamado de la función que regresa los valores totales por país.
        valores_paises, suma_total_valores = pais_valores_totales('./synergy_logistics_database.csv')
        

        proporcion = 0
        paises_80_porciento = []
        ojiva = []
        # Permite identificar los países que generan el 80% de exportaciones e importaciones.
        # Crea la ojiva porcentual para el diagrama de Pareto.

        for pais, valor in valores_paises:
            if(proporcion < 80):
                paises_80_porciento.append(pais)
                proporcion += (valor / suma_total_valores) * 100
            if(len(ojiva) == 0):
                ojiva.append(((valor / suma_total_valores) * 100))
            else:
                ojiva.append(ojiva[-1] + ((valor / suma_total_valores) * 100))
                 
        # Llamado de la función que imprime nombre y logo de la empresa
        header()

        # Imprime los valores generados por cada país y la lista de los países que generaron el 80% de los valores
        # exportación e importación.

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

        # Crea el diagrama de Pareto.
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

