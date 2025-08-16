Création d'une base de données SQLite3 pour le modèle de véhicules
Voici comment créer cette structure de classes en utilisant SQLite3 avec Python :

python
import sqlite3

# Connexion à la base de données (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('vehicules.db')
cursor = conn.cursor()

# Création de la table parente (abstraite) Vehicule
cursor.execute('''
CREATE TABLE IF NOT EXISTS Vehicule (
    id TEXT PRIMARY KEY,
    marque TEXT NOT NULL,
    modele TEXT NOT NULL,
    annee INTEGER NOT NULL,
    immatriculation TEXT UNIQUE NOT NULL,
    km INTEGER NOT NULL,
    atatur TEXT NOT NULL,
    type_vehicule TEXT NOT NULL CHECK(type_vehicule IN ('Voiture', 'Camion', 'Moto'))
)
''')

# Création de la table Voiture qui hérite de Vehicule
cursor.execute('''
CREATE TABLE IF NOT EXISTS Voiture (
    vehicule_id TEXT PRIMARY KEY,
    nb_places INTEGER NOT NULL,
    FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id) ON DELETE CASCADE
)
''')

# Création de la table Camion qui hérite de Vehicule
cursor.execute('''
CREATE TABLE IF NOT EXISTS Camion (
    vehicule_id TEXT PRIMARY KEY,
    capacite TEXT NOT NULL,
    FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id) ON DELETE CASCADE
)
''')

# Création de la table Moto qui hérite de Vehicule
cursor.execute('''
CREATE TABLE IF NOT EXISTS Moto (
    vehicule_id TEXT PRIMARY KEY,
    cylindree TEXT NOT NULL,
    FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id) ON DELETE CASCADE
)
''')

# Validation des changements
conn.commit()

# Fermeture de la connexion
conn.close()
Explication de l'implémentation
Modélisation de l'héritage : J'ai utilisé l'approche "Table par sous-classe" qui est adaptée à SQL pour représenter l'héritage :

Une table parente Vehicule avec tous les attributs communs

Des tables enfants (Voiture, Camion, Moto) avec leurs attributs spécifiques

Champ type_vehicule : J'ai ajouté ce champ pour identifier le type de véhicule et j'ai utilisé une contrainte CHECK pour limiter les valeurs possibles.

Clés étrangères : Les tables enfants ont une clé primaire qui est aussi une clé étrangère vers la table parente.

Exemple d'utilisation
Voici comment vous pourriez insérer et lire des données :

python
def ajouter_voiture():
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    # Insertion dans la table parente
    cursor.execute('''
    INSERT INTO Vehicule (id, marque, modele, annee, immatriculation, km, atatur, type_vehicule)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('v1', 'Renault', 'Clio', 2020, 'AB-123-CD', 15000, 'neuf', 'Voiture'))
    
    # Insertion dans la table enfant
    cursor.execute('''
    INSERT INTO Voiture (vehicule_id, nb_places)
    VALUES (?, ?)
    ''', ('v1', 5))
    
    conn.commit()
    conn.close()

def afficher_voitures():
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT v.*, vo.nb_places 
    FROM Vehicule v
    JOIN Voiture vo ON v.id = vo.vehicule_id
    ''')
    
    for row in cursor.fetchall():
        print(row)
    
    conn.close()
Cette implémentation respecte le modèle objet tout en utilisant les capacités relationnelles de SQLite.

maitenant ajouter une table location , entretien et consomation de carburant pour caque model de vehicule et les vehicules sont tous disponible par default et si on ajoute une location a un vehicule son status change en "en location " et de meme pour l'entretien et pour la location ajouter les information du client qui loue
Modèle complet de gestion de véhicules avec SQLite3
Je vais étendre la structure pour inclure les tables de location, entretien et consommation de carburant, avec la gestion de disponibilité des véhicules.

Schéma de base de données complet
python
import sqlite3

def creer_base_de_donnees():
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()

    # Suppression des tables existantes (pour le développement)
    cursor.executescript('''
    DROP TABLE IF EXISTS Consommation;
    DROP TABLE IF EXISTS Entretien;
    DROP TABLE IF EXISTS Location;
    DROP TABLE IF EXISTS Client;
    DROP TABLE IF EXISTS Moto;
    DROP TABLE IF EXISTS Camion;
    DROP TABLE IF EXISTS Voiture;
    DROP TABLE IF EXISTS Vehicule;
    ''')

    # Table Vehicule (parente)
    cursor.execute('''
    CREATE TABLE Vehicule (
        id TEXT PRIMARY KEY,
        marque TEXT NOT NULL,
        modele TEXT NOT NULL,
        annee INTEGER NOT NULL,
        immatriculation TEXT UNIQUE NOT NULL,
        km INTEGER NOT NULL,
        etat TEXT NOT NULL DEFAULT 'disponible' CHECK(etat IN ('disponible', 'en location', 'en entretien')),
        type_vehicule TEXT NOT NULL CHECK(type_vehicule IN ('Voiture', 'Camion', 'Moto'))
    )
    ''')

    # Tables enfants pour les types de véhicules
    cursor.execute('''
    CREATE TABLE Voiture (
        vehicule_id TEXT PRIMARY KEY,
        nb_places INTEGER NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE Camion (
        vehicule_id TEXT PRIMARY KEY,
        capacite TEXT NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id) ON DELETE CASCADE
    )
    ''')

    cursor.execute('''
    CREATE TABLE Moto (
        vehicule_id TEXT PRIMARY KEY,
        cylindree TEXT NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id) ON DELETE CASCADE
    )
    ''')

    # Table Client
    cursor.execute('''
    CREATE TABLE Client (
        id TEXT PRIMARY KEY,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        telephone TEXT NOT NULL,
        adresse TEXT,
        permis TEXT NOT NULL
    )
    ''')

    # Table Location
    cursor.execute('''
    CREATE TABLE Location (
        id TEXT PRIMARY KEY,
        vehicule_id TEXT NOT NULL,
        client_id TEXT NOT NULL,
        date_debut TEXT NOT NULL,  -- DATE ISO format (YYYY-MM-DD)
        date_fin TEXT NOT NULL,
        prix_total REAL NOT NULL,
        statut TEXT NOT NULL DEFAULT 'active' CHECK(statut IN ('active', 'terminee', 'annulee')),
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id),
        FOREIGN KEY (client_id) REFERENCES Client(id)
    )
    ''')

    # Table Entretien
    cursor.execute('''
    CREATE TABLE Entretien (
        id TEXT PRIMARY KEY,
        vehicule_id TEXT NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        cout REAL NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id)
    )
    ''')

    # Table Consommation
    cursor.execute('''
    CREATE TABLE Consommation (
        id TEXT PRIMARY KEY,
        vehicule_id TEXT NOT NULL,
        date TEXT NOT NULL,
        litres REAL NOT NULL,
        km_parcourus INTEGER NOT NULL,
        cout_total REAL NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id)
    )
    ''')

    conn.commit()
    conn.close()

# Créer la base de données
creer_base_de_donnees()
Fonctions pour gérer les opérations
python
def louer_vehicule(vehicule_id, client_id, date_debut, date_fin, prix_total, km_depart):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    try:
        # Vérifier si le véhicule est disponible
        cursor.execute('SELECT etat FROM Vehicule WHERE id = ?', (vehicule_id,))
        etat = cursor.fetchone()[0]
        
        if etat != 'disponible':
            print(f"Le véhicule {vehicule_id} n'est pas disponible (état: {etat})")
            return False
        
        # Créer la location
        location_id = f"loc_{vehicule_id}_{date_debut.replace('-', '')}"
        cursor.execute('''
        INSERT INTO Location (id, vehicule_id, client_id, date_debut, date_fin, prix_total, km_depart)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (location_id, vehicule_id, client_id, date_debut, date_fin, prix_total, km_depart))
        
        # Mettre à jour l'état du véhicule
        cursor.execute('''
        UPDATE Vehicule SET etat = 'en location' WHERE id = ?
        ''', (vehicule_id,))
        
        conn.commit()
        print(f"Location {location_id} créée avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la location: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def retourner_vehicule(location_id, km_retour):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    try:
        # Récupérer l'ID du véhicule
        cursor.execute('SELECT vehicule_id FROM Location WHERE id = ?', (location_id,))
        vehicule_id = cursor.fetchone()[0]
        
        # Mettre à jour la location
        cursor.execute('''
        UPDATE Location 
        SET km_retour = ?, statut = 'terminee'
        WHERE id = ?
        ''', (km_retour, location_id))
        
        # Mettre à jour les km du véhicule
        cursor.execute('''
        UPDATE Vehicule 
        SET km = ?, etat = 'disponible'
        WHERE id = ?
        ''', (km_retour, vehicule_id))
        
        conn.commit()
        print(f"Véhicule {vehicule_id} retourné avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors du retour: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def ajouter_entretien(vehicule_id, date, type_entretien, description, cout):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    try:
        # Vérifier si le véhicule est disponible
        cursor.execute('SELECT etat FROM Vehicule WHERE id = ?', (vehicule_id,))
        etat = cursor.fetchone()[0]
        
        if etat == 'en location':
            print(f"Le véhicule {vehicule_id} est actuellement en location")
            return False
        
        # Créer l'entretien
        entretien_id = f"ent_{vehicule_id}_{date.replace('-', '')}"
        cursor.execute('''
        INSERT INTO Entretien (id, vehicule_id, date, type, description, cout)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (entretien_id, vehicule_id, date, type_entretien, description, cout))
        
        # Mettre à jour l'état du véhicule si nécessaire
        if etat == 'disponible':
            cursor.execute('''
            UPDATE Vehicule SET etat = 'en entretien' WHERE id = ?
            ''', (vehicule_id,))
        
        conn.commit()
        print(f"Entretien {entretien_id} ajouté avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout d'entretien: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def terminer_entretien(entretien_id):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    try:
        # Récupérer l'ID du véhicule
        cursor.execute('SELECT vehicule_id FROM Entretien WHERE id = ?', (entretien_id,))
        vehicule_id = cursor.fetchone()[0]
        
        # Mettre à jour l'état du véhicule
        cursor.execute('''
        UPDATE Vehicule SET etat = 'disponible' WHERE id = ?
        ''', (vehicule_id,))
        
        conn.commit()
        print(f"Entretien {entretien_id} terminé, véhicule {vehicule_id} disponible")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de la fin d'entretien: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def ajouter_consommation(vehicule_id, date, litres, km_parcourus, cout_total):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    try:
        consommation_id = f"con_{vehicule_id}_{date.replace('-', '')}"
        cursor.execute('''
        INSERT INTO Consommation (id, vehicule_id, date, litres, km_parcourus, cout_total)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (consommation_id, vehicule_id, date, litres, km_parcourus, cout_total))
        
        # Mettre à jour les km du véhicule
        cursor.execute('''
        UPDATE Vehicule SET km = km + ? WHERE id = ?
        ''', (km_parcourus, vehicule_id))
        
        conn.commit()
        print(f"Consommation {consommation_id} ajoutée avec succès")
        return True
    except sqlite3.Error as e:
        print(f"Erreur lors de l'ajout de consommation: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()
Exemple d'utilisation complet
python
# Ajouter un client
def ajouter_client(id, nom, prenom, email, telephone, adresse, permis):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Client (id, nom, prenom, email, telephone, adresse, permis)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id, nom, prenom, email, telephone, adresse, permis))
    conn.commit()
    conn.close()

# Ajouter un véhicule
def ajouter_voiture(id, marque, modele, annee, immatriculation, km, nb_places):
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    # Ajouter à la table Vehicule
    cursor.execute('''
    INSERT INTO Vehicule (id, marque, modele, annee, immatriculation, km, type_vehicule)
    VALUES (?, ?, ?, ?, ?, ?, 'Voiture')
    ''', (id, marque, modele, annee, immatriculation, km))
    
    # Ajouter à la table Voiture
    cursor.execute('''
    INSERT INTO Voiture (vehicule_id, nb_places)
    VALUES (?, ?)
    ''', (id, nb_places))
    
    conn.commit()
    conn.close()

# Exemple d'utilisation
if __name__ == "__main__":
    # Créer la base de données
    creer_base_de_donnees()
    
    # Ajouter des clients
    ajouter_client("cli1", "Dupont", "Jean", "jean.dupont@email.com", "0612345678", "1 rue de Paris", "B123456789")
    ajouter_client("cli2", "Martin", "Sophie", "sophie.martin@email.com", "0698765432", "5 avenue des Champs", "B987654321")
    
    # Ajouter des véhicules
    ajouter_voiture("v1", "Renault", "Clio", 2020, "AB-123-CD", 15000, 5)
    ajouter_voiture("v2", "Peugeot", "308", 2019, "EF-456-GH", 25000, 5)
    
    # Louer un véhicule
    louer_vehicule("v1", "cli1", "2023-06-01", "2023-06-10", 450.0, 15000)
    
    # Ajouter une consommation
    ajouter_consommation("v1", "2023-06-05", 35.5, 450, 65.25)
    
    # Retourner le véhicule
    retourner_vehicule("loc_v1_20230601", 15450)
    
    # Ajouter un entretien
    ajouter_entretien("v1", "2023-06-15", "vidange", "Vidange et filtre à huile", 89.90)
    
    # Terminer l'entretien
    terminer_entretien("ent_v1_20230615")
Ce modèle complet permet de:

Gérer les différents types de véhicules avec leur spécificités

Suivre l'état de disponibilité des véhicules

Gérer les locations avec les informations clients

Enregistrer les entretiens et les consommations de carburant

Mettre à jour automatiquement l'état des véhicules selon les opérations

Les contraintes de clé étrangère assurent l'intégrité des données et les triggers implicites (via les fonctions) maintiennent la cohérence de l'état des véhicules.