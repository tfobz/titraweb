import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema

data = pd.read_excel("Werte Titrationskurve Sifat.xlsx")
ph_werte = data["pH"]
verbrauch_naoh = data["Vn"]

# Ableitung der pH-Werte nach dem Volumen der Natronlauge berechnen
ableitung = np.diff(ph_werte) / np.diff(verbrauch_naoh)

# Index des Äquivalenzpunkts (Maximum oder Minimum der Ableitung) finden
aequivalenzpunkt_index = argrelextrema(ableitung, np.greater)[0]

# Äquivalenzpunkt und zugehöriger pH-Wert
aequivalenzpunkt_verbrauch = verbrauch_naoh[aequivalenzpunkt_index]
aequivalenzpunkt_pH = ph_werte[aequivalenzpunkt_index]

# Titrationskurve erstellen und darstellen
plt.plot(verbrauch_naoh, ph_werte, marker='o', label='Titrationskurve')
plt.scatter(aequivalenzpunkt_verbrauch, aequivalenzpunkt_pH, color='blue', label='Äquivalenzpunkt', zorder=5)

# Erweitern Sie die Achsenskalen und andere Anpassungen
plt.xlim([0, max(verbrauch_naoh)])
plt.ylim([min(ph_werte) - 1, max(ph_werte) + 1])
plt.xlabel("Verbrauch an Natronlauge [mL]")
plt.ylabel("pH-Wert")
plt.title("Titrationsdiagramm")
plt.legend()

# Text mit Wert und Name neben dem Punkt hinzufügen
plt.annotate(f'Äquivalenzpunkt\n pH: {aequivalenzpunkt_pH.iloc[0]:.2f}', (aequivalenzpunkt_verbrauch.iloc[0], aequivalenzpunkt_pH.iloc[0]),
             textcoords="offset points", xytext=(10,0), ha='center')

plt.show()
