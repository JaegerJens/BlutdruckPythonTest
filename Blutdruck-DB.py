#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 12:16:54 2020

@author: jochen

Grundlage GUI+OO:
    https://sebsauvage.net/python/gui/
"""

import tkinter as tk
from tkinter import messagebox
import time, os, sys, sqlite3

class blutdruck_tk(tk.Tk):
    def __init__(self,parent):
        tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()
    
    def initialize(self):
        self.grid()
        
        #Datum
        datum = time.localtime()
        jahr, monat, tag = datum[0:3]
        stunde, minute = datum[3:5]
        #print("Es ist der {0:02d}.{1:02d}.{2:4}".format(tag, monat, jahr))
        #print("Um {0:02d}:{1:02d}".format(stunde, minute))

        #Überschrift
        self.labelHeader = tk.StringVar()
        self.labelHeader.set(u"Blutdruckwert Erfassen")
        lblHeader = tk.Label(self, textvariable=self.labelHeader, anchor="w")
        lblHeader.grid(column=0, row=0, columnspan=2, sticky='EW')
        
        #Bezeichner Dia
        self.labelDia = tk.StringVar()
        lblDia = tk.Label(self, textvariable=self.labelDia, anchor="e")
        lblDia.grid(column=0, row=1, sticky='EW')
        self.labelDia.set(u"Dia (mm/hg)")

        #Eingabe Dia
        self.entryDia = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entryDia, width=3)
        self.entry.grid(column=1, row=1, sticky='E')
        self.entryDia.set(u"")
        
        #Bezeichner Sys
        self.labelSys = tk.StringVar()
        lblSys = tk.Label(self, textvariable=self.labelSys, anchor="e")
        lblSys.grid(column=0, row=2, sticky='EW')
        self.labelSys.set(u"Sys (mm/hg)")

        #Eingabe Sys
        self.entrySys = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entrySys, width=3)
        self.entry.grid(column=1, row=2, sticky='E')
        self.entrySys.set(u"")
        
        #Bezeichner Puls
        self.labelPuls = tk.StringVar()
        lblPuls = tk.Label(self, textvariable=self.labelPuls, anchor="e")
        lblPuls.grid(column=0, row=3, sticky='EW')
        self.labelPuls.set(u"Puls (1/min)")

        #Eingabe Puls
        self.entryPuls = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entryPuls, width=3)
        self.entry.grid(column=1, row=3, sticky='E')
        self.entryPuls.set(u"")

        #Bezeichner Datum+Uhrzeit
        self.labelDatum = tk.StringVar()
        lblDatum = tk.Label(self, textvariable=self.labelDatum, anchor="e")
        lblDatum.grid(column=0, row=4, sticky='EW')
        self.labelDatum.set(u"Datum + Zeit:")

        #Eingabe Datum+Uhrzeit
        self.entryDatum = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.entryDatum, width=10)
        self.entry.grid(column=1, row=4, sticky='EW')
        self.entryDatum.set("{0:02d}.{1:02d}.{2:4}".format(tag, monat, jahr))

        #Eingabe zurücksetzen
        btnReset = tk.Button(self, text=u"Neu", command=self.reset)
        btnReset.grid(column=0, row=5)
        
        #Eingabeknopf
        btnEintrag = tk.Button(self, text=u"Eintragen", command=self.writeData)
        btnEintrag.grid(column=1, row=5)
                
        self.grid_columnconfigure(0, weight=1)
        self.resizable(True, False)
        self.update()
        self.geometry(self.geometry())


    def reset(self):
        self.entryDia.set(u"")
        self.entrySys.set(u"")
        self.entryPuls.set(u"")

        #aktuelles Datum und Uhrzeit ermitteln
        datum = time.localtime()
        jahr, monat, tag = datum[0:3]
        stunde, minute = datum[3:5]
        self.entryDatum.set("{0:02d}.{1:02d}.{2:4}".format(tag, monat, jahr))
        #print("Es ist der {0:02d}.{1:02d}.{2:4}".format(tag, monat, jahr))
        #print("Um {0:02d}:{1:02d}".format(stunde, minute))
    
  
    def writeData(self):
        #Eingabewerte in Zahlen umwandeln
        try:
            self.wertDia = int(self.entryDia.get())
        except:
            messagebox.showwarning("Eingabefehler", "Dia ist keine Zahl")
        try:
            self.wertSys = int(self.entrySys.get())
        except:
            messagebox.showwarning("Eingabefehler", "Sys ist keine Zahl")
        try:
            self.wertPuls = int(self.entryPuls.get())
        except:
            messagebox.showwarning("Eingabefehler", "Puls ist keine Zahl")
        #Daten in DB schreiben
        self.db()
        #Felder leeren
        self.reset()

    def db(self):
        try:
            # in init
            conn = sqlite3.connect('Blutdruck.db')
            sql_query = '''CREATE TABLE IF NOT EXISTS Blutdruck (\
                     Id INT PRIMARY KEY NOT NULL, \
                     dia INT, \
                     sys INT, \
                     puls INT, \
                     datum DATE);'''
            cursor = conn.cursor()
            print("Verbindung zur Datenbank hergestellt")
            cursor.execute(sql_query)
            conn.commit()
            print("SQL Tabelle erstellt")
            cursor.close()
            
            # hier nur zum Schreiben
            cursor = conn.cursor()
            sql_query = '''INSERT INTO Blutdruck (dia, sys, puls, datum) \
                        VALUES (125, 80, 55, ?)'''
            cursor.execute(sql_query)
            conn.commit()
            print(u"Daten ergänzt")
            
        except sqlite3.Error as error:
            print("Fehler beim verarbeiten", error)
        finally:
            if (conn):
                conn.close()
                print("Verbindung zur Datenbank geschlossen")


if __name__ == "__main__":
    app = blutdruck_tk(None)
    app.title('Blutdruckwerte')
    app.mainloop()
