import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

data = pd.read_excel("Werte Titrationskurve Sifat.xlsx")
ph_werte = data["pH"]
verbrauch_naoh = data["Vn"]

# Automatische Anpassung von Neutralpunkt und Puff-Bereich
neutralpunkt = np.mean(ph_werte)  # Mittelwert der pH-Werte als Neutralpunkt
puff_bereich = [np.min(ph_werte), np.max(ph_werte)]  # pH-Werte als Puff-Bereich

# Ableitung der pH-Werte nach dem Volumen der Natronlauge berechnen
ableitung = np.diff(ph_werte) / np.diff(verbrauch_naoh)

# Überprüfe, ob genügend Datenpunkte vorhanden sind
if len(ableitung) < 1:
    print("Nicht genügend Datenpunkte für die Ableitung.")
else:
    # Index des Wendepunkts (Maximum oder Minimum der Ableitung) finden
    wendepunkt_indices = argrelextrema(ableitung, np.less)[0]

    # Überprüfe, ob Wendepunkte gefunden wurden
    if len(wendepunkt_indices) == 0:
        print("Keine Wendepunkte gefunden.")
    else:
        # Wendepunkte und zugehörige pH-Werte
        wendepunkt_verbrauch = verbrauch_naoh[wendepunkt_indices]
        wendepunkt_pH = ph_werte[wendepunkt_indices]

        # Titrationskurve erstellen und darstellen
        plt.plot(verbrauch_naoh, ph_werte, marker='o', label='Titrationskurve')
        plt.scatter([wendepunkt_verbrauch], [wendepunkt_pH], color='red', label='Wendepunkt')
        plt.axhline(neutralpunkt, color='green', linestyle='--', label='Neutralpunkt')
        plt.fill_between(verbrauch_naoh, puff_bereich[0], puff_bereich[1], color='gray', alpha=0.2, label='Puff-Bereich', )
        plt.xlabel("Verbrauch an Natronlauge [mL]")
        plt.ylabel("pH-Wert")
        plt.title("Titrationsdiagramm")
        plt.legend()
        plt.show()
        
        # Ausgabe von Wendepunkt und anderen Informationen
        print("Wendepunkt (Volumen):", wendepunkt_verbrauch)
        print("Wendepunkt (pH):", wendepunkt_pH)
        print("Neutralpunkt:", neutralpunkt)
        print("Puff-Bereich:", puff_bereich)
