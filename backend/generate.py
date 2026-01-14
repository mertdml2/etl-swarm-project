import csv
import time
import os

# Crée le dossier /data si inexistant
os.makedirs("/data", exist_ok=True)

# Ouvre (ou crée) un fichier CSV pour écriture
with open("/data/data.csv", "w") as f:
    writer = csv.writer(f)

    # Écrit la ligne d’en-tête : noms des colonnes
    writer.writerow(["id", "value"])

    # Écrit 10 lignes simulées (données de test)
    for i in range(10):
        writer.writerow([i, i * 2])  
        time.sleep(1)  # pause d’une seconde (simulateur de flux progressif)
