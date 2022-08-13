from datetime import datetime
import calendar

class Fecha:



    @staticmethod
    def obtenerFechaConHora():
        fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return fecha


    @staticmethod
    def obtenerFechaSinHora():
        fecha=datetime.now().strftime('%Y-%m-%d')

        return fecha

    @staticmethod
    def obtenerSoloHora():
        fecha=datetime.now().strftime('%H:%M:%S')
        return fecha


    @staticmethod
    def calcularPagos(fecha_ingreso,lista_pagos,primera_colegiatura:float):
        lista_resultados = []
        #bandera para ver si es abono de tabla abonos o solo la primer colegiatura
        bandera=lista_pagos[0]["importe"]
        print("Abono bandera: ",bandera)

        #lista_pagos[0]["importe"]=lista_pagos[0]["importe"]*-1

        fecha_actual = Fecha().obtenerFechaSinHora()
        fecha_mes_actual = int(fecha_actual.split("-")[1])
        fecha_anio_actual = int(fecha_actual.split("-")[0])
        fecha_mes_ingreso = int(fecha_ingreso.split("-")[1])
        fecha_anio_ingreso = int(fecha_ingreso.split("-")[0])
        fecha_dia_actual = int(fecha_actual.split("-")[2])
        fecha_dia_ingreso = int(fecha_ingreso.split("-")[2])

        if lista_pagos: #La lista tiene elementos
            print("full")
           # validar que el año de ingreso sea mayor
#            dias_faltantes_de_pago = Fecha().validar_dias_transcurridos(fecha_dia_actual, fecha_dia_ingreso)

            if fecha_anio_actual > fecha_anio_ingreso:
                print("año mayor")
                meses_anuales = 12 - fecha_mes_ingreso
                meses_anuales = meses_anuales + fecha_mes_ingreso  # total de meses transcurridos


            elif fecha_anio_actual == fecha_anio_ingreso:
                cantidad_meses = fecha_mes_actual - fecha_mes_ingreso
                print("cantidad  Meses: ",cantidad_meses)
                if cantidad_meses == 0:
                    cantidad_meses = 1

                if cantidad_meses==1 and int(fecha_dia_actual-fecha_dia_ingreso)>0:
                    cantidad_meses=2

                resultados = Fecha().contarMesesPagos(lista_pagos)


                if float(bandera)<0 and int(fecha_dia_actual-fecha_dia_ingreso)>0:
                    cantidad_meses=2

                print("Can mes: ",cantidad_meses)
                #ver si es un abono al nodo abono o su primer colegiatura
                #si el valor es negativo, no es registro del nodo abono


                #validar si la lista viene con solo un pago
                print("Longitud",len(lista_pagos))
                print("bandera",bandera)
                if len(lista_pagos) >1 or float(bandera)>0:
                    print("Vivo")
                    numero_abonos = int(resultados[0]) + 1
                    total_abonos = float(resultados[1]) + float(primera_colegiatura)

                else:
                    print("muerto")
                    numero_abonos=int(resultados[0])
                    total_abonos = float(resultados[1])*-1


                print("Numero de abonos ", numero_abonos)
                print("Total de abonos", total_abonos)
                print("Cantidad Meses trans ", cantidad_meses)
                print("Saldo total ", primera_colegiatura * cantidad_meses)


                deuda=(primera_colegiatura*cantidad_meses)-total_abonos
                print("deuda",deuda)
                if cantidad_meses == numero_abonos:
                    lista_resultados = Fecha().validar_pagos_saldo(float(primera_colegiatura * cantidad_meses),
                                                                   total_abonos,
                                                                   fecha_dia_actual,
                                                                   fecha_dia_ingreso, "Pagos realizados",fecha_anio_actual,fecha_mes_actual)

                elif cantidad_meses < numero_abonos:
                    lista_resultados = Fecha().validar_pagos_saldo(float(primera_colegiatura * cantidad_meses),
                                                                   total_abonos,
                                                                   fecha_dia_actual,
                                                                   fecha_dia_ingreso, "Pagos realizados",fecha_anio_actual,fecha_mes_actual)

                elif cantidad_meses > numero_abonos:
                    print("No ha hecho todos los abonos")
                    lista_resultados = Fecha().validar_pagos_saldo(float(primera_colegiatura * cantidad_meses),
                                                                   total_abonos,
                                                                   fecha_dia_actual,
                                                                   fecha_dia_ingreso, "Pagos pendientes",fecha_anio_actual,fecha_mes_actual)



            else:
                print("No aplica")
        else:
            print("empty")

        lista_resultados.append(deuda)

        print("Final",lista_resultados)
        return  lista_resultados

    #Método para validar si estan hechos todos los pagos y si hay saldo deudor
    @staticmethod
    def validar_pagos_saldo(saldo_total_deudor:float, total_abonos:float,dia_actual:int ,dia_ingreso:int,estatus:str,anio:int,mes:int):
        lista_historico=["Sin datos",1986,"null"]
        lista_historico[2]=estatus
        if saldo_total_deudor == total_abonos:
            lista_historico[0]=1 #"Pagos al corriente"
        elif saldo_total_deudor < total_abonos:
            print("Pagos hecho y con saldo a favor")
            lista_historico[0]=2 #"Presenta un saldo a favor"
        elif saldo_total_deudor > total_abonos:
            lista_historico[0]=3 #Presenta un saldo deudor
        else:
            print("Error")

        #resultado_dia=Fecha().validar_dias_transcurridos(dia_actual,dia_ingreso)
        resultado_dia=dia_ingreso-dia_actual
        dias_mes_actual=calendar.monthrange(anio,mes)
        print("dias meses: ",dias_mes_actual[1])
        if resultado_dia<0:
            resultado_dia=dias_mes_actual[1]-(resultado_dia*(-1))

        lista_historico[1]=resultado_dia

        return lista_historico




    #Método para validar cuantos dias faltan para el pago
    """"@staticmethod
    def validar_dias_transcurridos(dia_actual:int ,dia_ingreso:int):
        if dia_actual>=dia_ingreso:
            dias_restantes=dia_actual-dia_ingreso
        elif dia_actual<dia_ingreso:
            dias_restantes=(dia_ingreso-dia_actual)*-1
        else:
            print("error al consultar dias")
        #Si los dias son negativos es por que falta la fecha de pago
        return int(dias_restantes)"""




    @staticmethod
    def contarMesesPagos(lista_pagos):
        print("Meses pago",lista_pagos)
        contador=0
        total_pagos=0
        lista_resultado=[]


        try:
            for i in lista_pagos:
                #print(i)
                contador=contador+1
                total_pagos=total_pagos+float(i["importe"])
            lista_resultado.append(contador)
            lista_resultado.append(total_pagos)
        except:
            print("sin pagos")
        #print("Total de pagos: ",contador)
        #print("total de abonos: ",total_pagos)
        return lista_resultado



    @staticmethod
    def calcularSaldosPendientesFavor(lista_encontrada):
        lista_resuelta=[0.0,0.0]  #posición CERO=encontra posicion UNO=favor
        saldo_favor=0.0
        saldo_encontra=0.0
        for i in lista_encontrada:
            print("ll",i)
            if i[0]==3: #saldo deudor
                saldo_encontra=saldo_encontra+float(i[3])
            elif i[0]==2: #saldo a favor
                saldo_encontrado=(float(i[3]))*-1
                saldo_favor=saldo_favor+saldo_encontrado
            else:
                print("error al leer datos")
        lista_resuelta[0]=saldo_encontra
        lista_resuelta[1]=saldo_favor
        return lista_resuelta




