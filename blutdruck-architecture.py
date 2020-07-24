class Messwert:
    def __init__(dia, sys, puls, datum):
        self.dia = dia
        self.sys = sys
        self.puls = puls
        self.datum = datum

class BlutdruckGui:
    def __init__():
    
    def MesswertEingabe():
        return Messwert(125, 80, 55, "2020-07-24")

class BlutdruckStorage:
    def __init__():
    def save(messwert):
    def loadMonthAverage():

class BlutdruckApp:
    def __init__():
        self.gui = BlutdruckGui
        self.storage = BlutdruckStorage
        messwert = self.gui.MesswertEingabe()
        self.storage.save(messwert)


app = BlutdruckApp()