import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

data = pd.read_excel("Werte Titrationskurve Sifat.xlsx")
ph_werte = data["pH"]
verbrauch_naoh = data["Vn"]

# Ableitung der pH-Werte nach dem Volumen der Natronlauge berechnen
ableitung = np.diff(ph_werte) / np.diff(verbrauch_naoh)

# Überprüfe, ob genügend Datenpunkte vorhanden sind
if len(ableitung) < 2:
    print("Nicht genügend Datenpunkte für die Ableitung.")
else:
    # Index des Wendepunkts (Maximum oder Minimum der Ableitung) finden
    wendepunkt_indices = argrelextrema(ableitung, np.less)[0]

    # Überprüfe, ob Wendepunkte gefunden wurden
    if len(wendepunkt_indices) == 0:
        print("Keine Wendepunkte gefunden.")
    else:
        # Wendepunkte und zugehörige pH-Werte
        wendepunkt_verbrauch = verbrauch_naoh[wendepunkt_indices[0]]
        wendepunkt_pH = ph_werte[wendepunkt_indices[0]]

        # Titrationskurve erstellen und Wendepunkte markieren
        plt.plot(verbrauch_naoh, ph_werte, marker='o', label='Titrationskurve')
        plt.scatter([wendepunkt_verbrauch], [wendepunkt_pH], color='red', label='Wendepunkt')
        plt.xlabel("Verbrauch an Natronlauge [mL]")
        plt.ylabel("pH-Wert")
        plt.title("Titrationsdiagramm mit Wendepunkt")
        plt.legend()
        plt.show()

        # Ausgabe von Wendepunkten und anderen Informationen
        print("Wendepunkt (Volumen):", wendepunkt_verbrauch)
        print("Wendepunkt (pH):", wendepunkt_pH)
