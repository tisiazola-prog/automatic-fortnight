import sqlite3 
import os

def get_db_path():
    """Retourne le chemin absolu vers la base de données"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, 'gestion_vehicule.db')



conn = sqlite3.connect(get_db_path())
cursor = conn.cursor()

# Vérification complète
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Tables existantes:", tables)

# Vérification spécifique
cursor.execute("PRAGMA table_info(Vehicules)")
columns = cursor.fetchall()
print("Structure de la table Vehicules:", columns)

conn.close()

