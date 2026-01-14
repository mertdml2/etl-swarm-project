import csv
import time
import psycopg2

# Petite pause pour s'assurer que PostgreSQL est prêt
time.sleep(5)

# Connexion à la base PostgreSQL via psycopg2
conn = psycopg2.connect(
    host="db",             # nom du service (réseau docker)
    dbname="etl",          
    user="etl",           
    password="etl"         
)

cur = conn.cursor()

# Création de la table 
cur.execute("CREATE TABLE IF NOT EXISTS data (id INT, value INT);")


with open("/data/data.csv") as f:
    next(f)  
    for row in csv.reader(f):
        # Insertion de chaque ligne dans la table PostgreSQL
        cur.execute("INSERT INTO data VALUES (%s, %s);", row)

# Validation 
conn.commit()