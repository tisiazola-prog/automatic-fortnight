
import sqlite3 

conn = sqlite3.connect('gestion_vehicule.db')
cursor = conn.cursor()



cursor.execute('''
    CREATE TABLE "Vehicule" (
        vehicule_id	INTEGER NOT NULL,
        type_vehicule TEXT NOT NULL CHECK(type_vehicule IN ('Voiture', 'Camion', 'Moto')),
        marque TEXT NOT NULL,
        modele TEXT  NOT NULL,
        immatriculation TEXT NOT NULL,
        kilometrage	REAL NOT NULL,
        annee TEXT NOT NULL,
        image TEXT,
        status TEXT NOT NULL DEFAULT 'disponible' CHECK(status IN ('disponible', 'en location', 'en entretien')),
        date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
        PRIMARY KEY("vehicule_id" AUTOINCREMENT)
        
    )
    ''')



# Validation des changements
conn.commit()

# Fermeture de la connexion
conn.close()


























    