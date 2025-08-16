import sqlite3
import os
from flask import jsonify , current_app

def get_db_path():
    """Retourne le chemin absolu vers la base de données"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'gestion_vehicule.db')




        
def get_vehicules():
    try:
        conn = sqlite3.connect(get_db_path())  #Connexion à la base de données
        conn.row_factory = sqlite3.Row  #Permet de récupérer les lignes sous forme de dictionnaire
        
        query = '''
            SELECT 
                id,
                type,
                marque,
                model,
                immatriculation,
                annee,
                capacite ,
                kilometrage,
                image ,
                status
            FROM Vehicule
            WHERE 1=1  
        '''
        
        cursor = conn.cursor()
        cursor.execute(query)  #Exécution de la requête
        
        vehicules = [dict(row) for row in cursor.fetchall()] #Transformation des résultats en liste de dictionnaires
        conn.close()  #Fermeture de la connexion
        
        return vehicules  #Retourne la liste des véhicules
    
    except sqlite3.Error as e:
        print(f"[ERREUR DB] {str(e)}")  #Affiche l'erreur de la base de données
        return None  #Retourne None en cas d'erreur

 
def get_showOneVehicule(vehicule_id, vehicule_type):
    try:
        # Liste blanche des tables autorisées
        ALLOWED_TABLES = {
            "Voiture": "Voiture",
            "Camion": "Camion",
            "Moto": "Moto"
        }
        
        if vehicule_type not in ALLOWED_TABLES:
            return None
            
        table_name = ALLOWED_TABLES[vehicule_type]
        
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        
        # Utilisation de paramètres nommés pour plus de clarté
        query = """
            SELECT V.*, T.* 
            FROM Vehicule V
            JOIN :table_name T ON V.id = T.vehicule_id
            WHERE T.vehicule_id = :vehicule_id;
        """
        
        # SQLite ne supporte pas les paramètres nommés pour les noms de tables,
        # donc nous devons utiliser une autre approche sécurisée
        query = query.replace(":table_name", table_name)
        
        cursor = conn.cursor()
        cursor.execute(query, {"vehicule_id": vehicule_id})
        vehicule = cursor.fetchone()
        
        if vehicule:
            vehicule = dict(vehicule)
        
        conn.close()
        return vehicule
    
    except sqlite3.Error as e:
        return None
    

def filtre_vehicules(type_vehicule, marque):
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row 
    cursor = conn.cursor()

    query = "SELECT * FROM Vehicule WHERE 1=1"
    params = []

    # Filtre par type (seulement si spécifié)
    if type_vehicule:  # S'active uniquement si type_vehicule n'est pas vide
        query += " AND type = ?"
        params.append(type_vehicule)

    # Filtre par marque (recherche partielle)
    if marque:
        query += " AND marque LIKE ?"
        params.append(f"%{marque}%")

    cursor.execute(query, params)
    resultats = cursor.fetchall()
    conn.close()

    return resultats


def get_carburants():
    conn = None
    try:
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row
        
        query = '''
            SELECT 
                c.carburant_id,
                c.vehicule_id,
                c.litre,
                c.prix_litre,
                c.km_parcours,
                c.consomation,
                c.date_ajout ,
                v.type,
                v.marque,
                v.modele,
                v.immatriculation
            FROM carburant c
            JOIN vehicule v ON c.vehicule_id = v.vehicule_id 
            ORDER BY c.date_ajout DESC
        '''  # Removed WHERE 1=1 inutile
        
        cursor = conn.cursor()
        cursor.execute(query)
        
        results = cursor.fetchall()
            
        carburants = [dict(row) for row in results]

        return carburants
        
    except sqlite3.Error as e:
        print(f"[ERREUR DB DÉTAILLÉE] {str(e)}")  # Message d'erreur plus visible
        raise  # Relance l'exception pour ne pas la cacher
    finally:
        if conn:
            conn.close()
 
def add_vehicule(type, marque, modele, immatriculation, annee, capacite, kilometrage, image_path, nb_place=None, cylindre=None):
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(get_db_path())
        conn.row_factory = sqlite3.Row  # Permet de récupérer les lignes sous forme de dictionnaire
        
        # Insertion dans la table Vehicule
        query = ''' 
            INSERT INTO Vehicule (type, marque, model, immatriculation, annee, capacite, kilometrage , image) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?) 
        '''
        params = (type, marque, modele, immatriculation, annee, capacite, kilometrage , image_path)
        
        cursor = conn.cursor()
        cursor.execute(query, params)  # Exécution de la requête
        
        vehicule_id = cursor.lastrowid  # Récupération de l'ID du véhicule inséré
        
        # Insertion dans les tables spécifiques selon le type de véhicule
        if type == "Voiture":
            query = ''' 
                INSERT INTO Voiture (vehicule_id, nb_places) 
                VALUES (?, ?) 
            '''
            params = (vehicule_id, nb_place)
            cursor.execute(query, params)
        
        elif type == "Camion":
            query = ''' 
                INSERT INTO Camion (vehicule_id, nb_places) 
                VALUES (?, ?) 
            '''
            params = (vehicule_id, nb_place)
            cursor.execute(query, params)
        
        elif type == "Moto":
            query = ''' 
                INSERT INTO Moto (vehicule_id, cylindree) 
                VALUES (?, ?) 
            '''
            params = (vehicule_id, cylindre)
            cursor.execute(query, params)

        # Commit des changements
        conn.commit()
    
    except sqlite3.Error as e:
        print(f"[ERREUR DB] {str(e)}")  # Affiche l'erreur de la base de données
        return None  # Retourne None en cas d'erreur
    
    finally:
        # Assurez-vous que la connexion est fermée
        if conn:
            conn.close()

    return True 


def get_totalVehicule():
    try:
        conn = sqlite3.connect(get_db_path())  #Connexion à la base de données
        conn.row_factory = sqlite3.Row  #Permet de récupérer les lignes sous forme de dictionnaire
        
        query = '''
            SELECT COUNT(*) AS total FROM Vehicule WHERE 1=1  
        '''
        
        cursor = conn.cursor()
        cursor.execute(query)  #Exécution de la requête
        
        vehicules = cursor.fetchone() #Transformation des résultats en liste de dictionnaires
        conn.close()  #Fermeture de la connexion
        
        return vehicules["total"]  #Retourne la liste des véhicules
    
    except sqlite3.Error as e:
        print(f"[ERREUR DB] {str(e)}")  #Affiche l'erreur de la base de données
        return None  #Retourne None en cas d'erreur

  