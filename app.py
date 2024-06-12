from flask import Flask, jsonify, render_template, request, send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
from io import BytesIO
import base64

app = Flask(__name__)

plt.switch_backend('Agg')


@app.route('/')
def send_index():
    return send_from_directory('ui-react/build', 'index.html')
@app.route('/<path:path>')
def send_ui(path):
    return send_from_directory('ui-react/build', path)

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('ui-react/build/static/css', path)

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('ui-react/build/static/js', path)

@app.route('/titration_diagram')
def titration_diagram():
    data = pd.read_excel("Werte Titrationskurve Sifat.xlsx")
    ph_werte = data["pH"]
    verbrauch_naoh = data["Vn"]

    neutralpunkt = np.mean(ph_werte)
    puff_bereich = [np.min(ph_werte), np.max(ph_werte)]

    ableitung = np.diff(ph_werte) / np.diff(verbrauch_naoh)

    if len(ableitung) < 1:
        error_message = "Nicht genügend Datenpunkte für die Ableitung."
        return render_template('error.html', error_message=error_message)

    wendepunkt_index = argrelextrema(ableitung, np.less)[0]

    if len(wendepunkt_index) == 0:
        error_message = "Keine Wendepunkte gefunden."
        return render_template('error.html', error_message=error_message)

    wendepunkt_verbrauch = verbrauch_naoh[wendepunkt_index]
    wendepunkt_pH = ph_werte[wendepunkt_index]

    neutralpunkt_x = 10

    aequivalenzpunkt_index = argrelextrema(ableitung, np.greater)[0]
    aequivalenzpunkt_verbrauch = verbrauch_naoh[aequivalenzpunkt_index]
    aequivalenzpunkt_pH = ph_werte[aequivalenzpunkt_index]

    # Plot erstellen
    plt.figure()
    plt.plot(verbrauch_naoh, ph_werte, marker='*', label='Titrationskurve')
    plt.scatter([neutralpunkt_x], [neutralpunkt], color='green', marker='o', label='Neutralpunkt')
    plt.scatter(wendepunkt_verbrauch, wendepunkt_pH, color='red', label='Wendepunkt', zorder=5)
    plt.scatter(aequivalenzpunkt_verbrauch, aequivalenzpunkt_pH, color='blue', label='Äquivalenzpunkt', zorder=5)
    plt.fill_between(verbrauch_naoh, puff_bereich[0], puff_bereich[1], color='gray', alpha=0.2, label='Puff-Bereich')

    plt.xlim([0, max(verbrauch_naoh)])
    plt.ylim([min(ph_werte) - 1, max(ph_werte) + 1])
    plt.xlabel("Verbrauch an Natronlauge [mL]")
    plt.ylabel("pH-Wert")
    plt.title("Titrationsdiagramm")
    plt.legend()

    plt.annotate(f'Neutralpunkt pH = {neutralpunkt:.2f}', (neutralpunkt_x, neutralpunkt), textcoords="offset points",
                 xytext=(10, -20), ha='center')
    plt.annotate(f'Äquivalenzpunkt pH = {aequivalenzpunkt_pH.iloc[0]:.2f}',
                 (aequivalenzpunkt_verbrauch.iloc[0], aequivalenzpunkt_pH.iloc[0]), textcoords="offset points",
                 xytext=(10, 0), ha='center')

    # Plot in Byte-Objekt umwandeln und als Base64 codieren
    img_data = BytesIO()
    plt.savefig(img_data, format='png')
    img_data.seek(0)
    img_base64 = base64.b64encode(img_data.read()).decode("utf-8")

    return render_template('titration_diagram.html', img_base64=img_base64, wendepunkte_volumen=wendepunkt_verbrauch.tolist(),
                           wendepunkte_pH=wendepunkt_pH.tolist(), aequivalenzpunkte_volumen=aequivalenzpunkt_verbrauch.tolist(),
                           aequivalenzpunkte_pH=aequivalenzpunkt_pH.tolist(), neutralpunkt=neutralpunkt, puff_bereich=puff_bereich)

@app.route('/values')
def get_values():
    data = pd.read_excel("Werte Titrationskurve Sifat.xlsx")
    ph_werte = data["pH"]
    verbrauch_naoh = data["Vn"]

    neutralpunkt = np.mean(ph_werte)
    puff_bereich = [np.min(ph_werte), np.max(ph_werte)]

    ableitung = np.diff(ph_werte) / np.diff(verbrauch_naoh)

    if len(ableitung) < 1:
        return jsonify({"error": "Nicht genügend Datenpunkte für die Ableitung."})

    wendepunkt_index = argrelextrema(ableitung, np.less)[0]

    if len(wendepunkt_index) == 0:
        return jsonify({"error": "Keine Wendepunkte gefunden."})

    wendepunkt_verbrauch = verbrauch_naoh[wendepunkt_index]
    wendepunkt_pH = ph_werte[wendepunkt_index]

    aequivalenzpunkt_index = argrelextrema(ableitung, np.greater)[0]
    aequivalenzpunkt_verbrauch = verbrauch_naoh[aequivalenzpunkt_index]
    aequivalenzpunkt_pH = ph_werte[aequivalenzpunkt_index]

    return jsonify({
        "Wendepunkte (Volumen)": wendepunkt_verbrauch.tolist(),
        "Wendepunkte (pH)": wendepunkt_pH.tolist(),
        "Äquivalenzpunkte (Volumen)": aequivalenzpunkt_verbrauch.tolist(),
        "Äquivalenzpunkte (pH)": aequivalenzpunkt_pH.tolist(),
        "Neutralpunkt": neutralpunkt,
        "Puff-Bereich": puff_bereich
    })

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)