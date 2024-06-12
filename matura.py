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
    wendepunkt_index = argrelextrema(ableitung, np.less)[0]

    # Überprüfe, ob Wendepunkte gefunden wurden
    if len(wendepunkt_index) == 0:
        print("Keine Wendepunkte gefunden.")
    else:
        # Wendepunkte und zugehörige pH-Werte
        wendepunkt_verbrauch = verbrauch_naoh[wendepunkt_index]
        wendepunkt_pH = ph_werte[wendepunkt_index]

        # Durchschnitt der x-Koordinaten der Wendepunkte für den Neutralpunkt
        neutralpunkt_x = 10

        # Äquivalenzpunkt(e) finden
        aequivalenzpunkt_index = argrelextrema(ableitung, np.greater)[0]
        aequivalenzpunkt_verbrauch = verbrauch_naoh[aequivalenzpunkt_index]
        aequivalenzpunkt_pH = ph_werte[aequivalenzpunkt_index]
        # Titrationskurve erstellen und darstellen
        plt.plot(verbrauch_naoh, ph_werte, marker='*', label='Titrationskurve')
        plt.scatter([neutralpunkt_x], [neutralpunkt], color='green', marker='o', label='Neutralpunkt')
        plt.scatter(wendepunkt_verbrauch, wendepunkt_pH, color='red', label='Wendepunkt', zorder=5)
        plt.scatter(aequivalenzpunkt_verbrauch, aequivalenzpunkt_pH, color='blue', label='Äquivalenzpunkt', zorder=5)
        plt.fill_between(verbrauch_naoh, puff_bereich[0], puff_bereich[1], color='gray', alpha=0.2, label='Puff-Bereich')

        # Erweitern Sie die Achsenskalen
        plt.xlim([0, max(verbrauch_naoh)])
        plt.ylim([min(ph_werte) - 1, max(ph_werte) + 1])
        plt.xlabel("Verbrauch an Natronlauge [mL]")
        plt.ylabel("pH-Wert")
        plt.title("Titrationsdiagramm")
        plt.legend()

        # Texte mit Werten und Namen neben den Punkten hinzufügen
        plt.annotate(f'Neutralpunkt pH = {neutralpunkt:.2f}', (neutralpunkt_x, neutralpunkt),
                     textcoords="offset points", xytext=(10,-20), ha='center')
        plt.annotate(f'Äquivalenzpunkt pH = {aequivalenzpunkt_pH.iloc[0]:.2f}', (aequivalenzpunkt_verbrauch.iloc[0], aequivalenzpunkt_pH.iloc[0]),
             textcoords="offset points", xytext=(10,0), ha='center')

        # Ausgabe von Wendepunkt, Äquivalenzpunkt und anderen Informationen
        print("Wendepunkte (Volumen):", wendepunkt_verbrauch.tolist())
        print("Wendepunkte (pH):", wendepunkt_pH.tolist())
        print("Äquivalenzpunkte (Volumen):", aequivalenzpunkt_verbrauch.tolist())
        print("Äquivalenzpunkte (pH):", aequivalenzpunkt_pH.tolist())
        print("Neutralpunkt:", neutralpunkt)
        print("Puff-Bereich:", puff_bereich)

        # Beispiel für die Berechnung von pKs oder pKb (ersetzen Sie dies durch die tatsächlichen Werte)
        saeure_konstante = 1e-3  # Beispiel für die Säurekonstante
        base_konstante = 1e-5   # Beispiel für die Basenkonstante

        pKs = -np.log10(saeure_konstante)
        pKb = -np.log10(base_konstante)

        print("pKs:", pKs)
        print("pKb:", pKb)

        plt.show()