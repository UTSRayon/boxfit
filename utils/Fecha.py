from datetime import datetime

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

