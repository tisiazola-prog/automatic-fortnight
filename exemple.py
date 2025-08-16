# Sauvegarder des données dans une base de données SQLite3 avec Python

SQLite3 est une bibliothèque intégrée à Python qui permet de gérer des bases de données SQL légères et embarquées. Voici comment sauvegarder des données :

## 1. Connexion à la base de données

```python
import sqlite3

# Se connecter à la base (elle sera créée si elle n'existe pas)
conn = sqlite3.connect('ma_base.db')

# Créer un curseur pour exécuter des commandes SQL
cursor = conn.cursor()
```

## 2. Création d'une table (si elle n'existe pas)

```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS utilisateurs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )
''')
conn.commit()  # Valider la création de la table
```

## 3. Insertion de données

### Insertion simple
```python
cursor.execute("INSERT INTO utilisateurs (nom, email, age) VALUES (?, ?, ?)", 
               ('Jean Dupont', 'jean@example.com', 30))
conn.commit()
```

### Insertion multiple
```python
donnees = [
    ('Marie Martin', 'marie@example.com', 25),
    ('Pierre Durand', 'pierre@example.com', 40),
    ('Sophie Lambert', 'sophie@example.com', 35)
]

cursor.executemany("INSERT INTO utilisateurs (nom, email, age) VALUES (?, ?, ?)", donnees)
conn.commit()
```

## 4. Fermeture de la connexion

```python
conn.close()
```

## Exemple complet

```python
import sqlite3

def sauvegarder_donnees():
    try:
        conn = sqlite3.connect('ma_base.db')
        cursor = conn.cursor()
        
        # Création de la table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prix REAL,
                quantite INTEGER
            )
        ''')
        
        # Insertion de données
        produits = [
            ('Ordinateur', 899.99, 10),
            ('Smartphone', 599.50, 25),
            ('Tablette', 349.99, 15)
        ]
        
        cursor.executemany("INSERT INTO produits (nom, prix, quantite) VALUES (?, ?, ?)", produits)
        
        # Validation des changements
        conn.commit()
        print("Données sauvegardées avec succès!")
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
    finally:
        if conn:
            conn.close()

sauvegarder_donnees()
```

## Bonnes pratiques

1. Toujours utiliser `commit()` pour valider les changements
2. Fermer la connexion avec `close()` quand vous avez terminé
3. Utiliser les paramètres (?) pour éviter les injections SQL
4. Gérer les erreurs avec des blocs try/except
5. Pour des opérations complexes, utilisez les transactions

Vous pouvez ensuite interroger ces données avec des requêtes SELECT, les mettre à jour avec UPDATE, ou les supprimer avec DELETE.


# Requêtes SELECT, UPDATE et DELETE avec SQLite3 en Python

Voici comment effectuer les opérations de base pour interagir avec une base de données SQLite3 en Python.

## 1. Requête SELECT (Lire des données)

### Sélectionner tous les enregistrements
```python
import sqlite3

conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

# Sélectionner tous les utilisateurs
cursor.execute("SELECT * FROM utilisateurs")
resultats = cursor.fetchall()  # Récupère tous les enregistrements

for row in resultats:
    print(row)  # Chaque row est un tuple représentant une ligne

conn.close()
```

### Sélectionner avec des conditions
```python
# Sélectionner les utilisateurs de plus de 30 ans
cursor.execute("SELECT * FROM utilisateurs WHERE age > ?", (30,))
resultats = cursor.fetchall()

# Sélectionner seulement certains champs
cursor.execute("SELECT nom, email FROM utilisateurs WHERE nom LIKE ?", ('J%',))
```

### Récupérer un seul enregistrement
```python
cursor.execute("SELECT * FROM utilisateurs WHERE id = ?", (1,))
utilisateur = cursor.fetchone()  # Récupère un seul enregistrement
print(utilisateur)
```

## 2. Requête UPDATE (Modifier des données)

```python
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

# Mettre à jour l'âge d'un utilisateur
cursor.execute("UPDATE utilisateurs SET age = ? WHERE id = ?", (35, 1))

# Mettre à jour plusieurs champs
cursor.execute("""
    UPDATE utilisateurs 
    SET nom = ?, email = ? 
    WHERE id = ?
""", ('Jean Dupont Modifié', 'jean.modifie@example.com', 1))

conn.commit()  # Ne pas oublier de valider les modifications
conn.close()
```

## 3. Requête DELETE (Supprimer des données)

```python
conn = sqlite3.connect('ma_base.db')
cursor = conn.cursor()

# Supprimer un utilisateur spécifique
cursor.execute("DELETE FROM utilisateurs WHERE id = ?", (2,))

# Supprimer avec une condition
cursor.execute("DELETE FROM utilisateurs WHERE age < ?", (18,))

conn.commit()  # Validation nécessaire pour les suppressions
conn.close()
```

## Exemple Complet avec Gestion des Erreurs

```python
import sqlite3

def manipuler_donnees():
    try:
        conn = sqlite3.connect('ma_base.db')
        cursor = conn.cursor()
        
        # SELECT - Lire avant modification
        print("Avant modification:")
        cursor.execute("SELECT * FROM utilisateurs")
        for row in cursor.fetchall():
            print(row)
        
        # UPDATE - Modifier un enregistrement
        cursor.execute("UPDATE utilisateurs SET age = ? WHERE nom = ?", 
                      (45, 'Jean Dupont'))
        
        # DELETE - Supprimer un enregistrement
        cursor.execute("DELETE FROM utilisateurs WHERE email = ?", 
                      ('pierre@example.com',))
        
        # SELECT - Voir les changements
        print("\nAprès modification:")
        cursor.execute("SELECT * FROM utilisateurs")
        for row in cursor.fetchall():
            print(row)
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"Erreur SQLite: {e}")
        conn.rollback()  # Annuler les changements en cas d'erreur
    finally:
        if conn:
            conn.close()

manipuler_donnees()
```

## Bonnes Pratiques

1. **Paramètres**: Toujours utiliser les paramètres (`?`) pour éviter les injections SQL
2. **Transactions**: Utilisez `commit()` pour valider et `rollback()` en cas d'erreur
3. **Ressources**: Fermez toujours la connexion avec `close()`
4. **SELECT**: 
   - `fetchall()` pour tous les résultats
   - `fetchone()` pour un seul enregistrement
   - `fetchmany(size)` pour un nombre spécifique d'enregistrements
5. **WHERE**: Soyez précis dans vos conditions pour éviter des modifications/suppressions involontaires

Ces opérations couvrent l'essentiel des interactions CRUD (Create, Read, Update, Delete) avec une base SQLite3 en Python.


# Recherche Automatique avec Flask et SQLite

Voici comment implémenter une recherche en temps réel avec Flask qui filtre les résultats au fur et à mesure que l'utilisateur tape :

## Structure du projet
```
/projet_flask
   /static
      script.js
      style.css
   /templates
      index.html
   app.py
   boutique.db
```

## 1. Fichier principal (app.py)

```python
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Fonction pour se connecter à la base de données
def get_db_connection():
    conn = sqlite3.connect('boutique.db')
    conn.row_factory = sqlite3.Row  # Pour avoir des dictionnaires plutôt que des tuples
    return conn

# Route pour la page principale
@app.route('/')
def index():
    return render_template('index.html')

# Route API pour la recherche
@app.route('/recherche')
def recherche():
    terme = request.args.get('terme', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if terme:
        cursor.execute("SELECT * FROM produits WHERE nom LIKE ?", (f'%{terme}%',))
    else:
        cursor.execute("SELECT * FROM produits")
    
    produits = cursor.fetchall()
    conn.close()
    
    # Convertir les Row en dictionnaires
    produits_list = [dict(produit) for produit in produits]
    return jsonify(produits_list)

if __name__ == '__main__':
    app.run(debug=True)
```

## 2. Template HTML (templates/index.html)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recherche en temps réel</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Recherche de produits</h1>
        
        <input type="text" id="searchInput" placeholder="Tapez pour rechercher...">
        
        <div id="results">
            <!-- Les résultats s'afficheront ici -->
        </div>
    </div>

    <script src="{{ url_for('static', filename='script.js') }}"></script>
</body>
</html>
```

## 3. JavaScript (static/script.js)

```javascript
document.getElementById('searchInput').addEventListener('input', function() {
    const termeRecherche = this.value;
    
    fetch(`/recherche?terme=${encodeURIComponent(termeRecherche)}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>Aucun produit trouvé</p>';
                return;
            }
            
            const ul = document.createElement('ul');
            data.forEach(produit => {
                const li = document.createElement('li');
                li.textContent = `${produit.nom} - ${produit.prix}€ (Stock: ${produit.quantite})`;
                ul.appendChild(li);
            });
            
            resultsDiv.appendChild(ul);
        })
        .catch(error => console.error('Erreur:', error));
});
```

## 4. CSS (static/style.css)

```css
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

#searchInput {
    width: 100%;
    padding: 10px;
    font-size: 16px;
    margin-bottom: 20px;
}

#results ul {
    list-style-type: none;
    padding: 0;
}

#results li {
    padding: 10px;
    border-bottom: 1px solid #ddd;
}

#results li:hover {
    background-color: #f5f5f5;
}
```

## 5. Préparation de la base de données

Avant de lancer l'application, créez une base de données SQLite avec une table produits :

```python
import sqlite3

conn = sqlite3.connect('boutique.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix REAL,
        quantite INTEGER
    )
''')

# Insérer des données de test
produits_test = [
    ('Ordinateur portable', 899.99, 10),
    ('Smartphone', 599.50, 25),
    ('Tablette', 349.99, 15),
    ('Écran 24 pouces', 199.99, 8),
    ('Clavier sans fil', 49.99, 30)
]

cursor.executemany("INSERT INTO produits (nom, prix, quantite)


$(document).ready(function() {
    $('#searchInput').on('input', function() {
        const termeRecherche = $(this).val();
        
        $.get('/recherche', { terme: termeRecherche }, function(data) {
            const resultsDiv = $('#results');
            resultsDiv.empty();
            
            if (data.length === 0) {
                resultsDiv.append('<p>Aucun produit trouvé</p>');
                return;
            }
            
            const ul = $('<ul></ul>');
            $.each(data, function(index, produit) {
                ul.append(
                    $('<li></li>').text(
                        `${produit.nom} - ${produit.prix}€ (Stock: ${produit.quantite})`
                    )
                );
            });
            
            resultsDiv.append(ul);
        }).fail(function(error) {
            console.error('Erreur:', error);
        });
    });
});


# Recherche par Date avec Flask et SQLite

Voici comment implémenter une recherche par date dans une application Flask avec SQLite.

## 1. Préparation de la base de données

D'abord, modifiez votre table pour inclure un champ date :

```python
import sqlite3
from datetime import datetime

conn = sqlite3.connect('boutique.db')
cursor = conn.cursor()

# Créer une table avec un champ date
cursor.execute('''
    CREATE TABLE IF NOT EXISTS produits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prix REAL,
        quantite INTEGER,
        date_ajout DATE  -- Nouveau champ pour la date
    )
''')

# Insérer des données de test avec dates
produits_test = [
    ('Ordinateur portable', 899.99, 10, '2023-01-15'),
    ('Smartphone', 599.50, 25, '2023-02-20'),
    ('Tablette', 349.99, 15, '2023-03-10'),
    ('Écran 24 pouces', 199.99, 8, '2023-01-25'),
    ('Clavier sans fil', 49.99, 30, '2023-03-01')
]

cursor.executemany(
    "INSERT INTO produits (nom, prix, quantite, date_ajout) VALUES (?, ?, ?, ?)", 
    produits_test
)
conn.commit()
conn.close()
```

## 2. Modification de l'API Flask (app.py)

```python
from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('boutique.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('recherche_date.html')

@app.route('/recherche_date')
def recherche_date():
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if date_debut and date_fin:
        # Recherche entre deux dates
        cursor.execute("""
            SELECT * FROM produits 
            WHERE date_ajout BETWEEN ? AND ?
            ORDER BY date_ajout
        """, (date_debut, date_fin))
    elif date_debut:
        # Recherche à partir d'une date
        cursor.execute("""
            SELECT * FROM produits 
            WHERE date_ajout >= ?
            ORDER BY date_ajout
        """, (date_debut,))
    elif date_fin:
        # Recherche jusqu'à une date
        cursor.execute("""
            SELECT * FROM produits 
            WHERE date_ajout <= ?
            ORDER BY date_ajout
        """, (date_fin,))
    else:
        # Aucune date - retourner tous les produits
        cursor.execute("SELECT * FROM produits ORDER BY date_ajout")
    
    produits = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(produit) for produit in produits])

if __name__ == '__main__':
    app.run(debug=True)
```

## 3. Template HTML (templates/recherche_date.html)

```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recherche par Date</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css">
    <style>
        .date-picker { max-width: 250px; }
        table { margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container py-4">
        <h1 class="mb-4">Recherche de produits par date</h1>
        
        <div class="row g-3">
            <div class="col-md-3">
                <label for="dateDebut" class="form-label">Date de début</label>
                <input type="date" class="form-control date-picker" id="dateDebut">
            </div>
            <div class="col-md-3">
                <label for="dateFin" class="form-label">Date de fin</label>
                <input type="date" class="form-control date-picker" id="dateFin">
            </div>
            <div class="col-md-2 d-flex align-items-end">
                <button id="btnRechercher" class="btn btn-primary">Rechercher</button>
            </div>
        </div>
        
        <div class="mt-4">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th>Nom</th>
                        <th>Prix</th>
                        <th>Quantité</th>
                        <th>Date d'ajout</th>
                    </tr>
                </thead>
                <tbody id="results">
                    <!-- Les résultats s'afficheront ici -->
                </tbody>
            </table>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            // Rechercher au clic du bouton
            $('#btnRechercher').click(function() {
                rechercherProduits();
            });
            
            // Rechercher aussi quand les dates changent
            $('#dateDebut, #dateFin').change(function() {
                rechercherProduits();
            });
            
            // Charger tous les produits au démarrage
            rechercherProduits();
        });
        
        function rechercherProduits() {
            const dateDebut = $('#dateDebut').val();
            const dateFin = $('#dateFin').val();
            
            $.get('/recherche_date', {
                date_debut: dateDebut,
                date_fin: dateFin
            }, function(data) {
                const tbody = $('#results');
                tbody.empty();
                
                if (data.length === 0) {
                    tbody.append('<tr><td colspan="4" class="text-center">Aucun produit trouvé</td></tr>');
                    return;
                }
                
                $.each(data, function(index, produit) {
                    const dateAjout = new Date(produit.date_ajout).toLocaleDateString('fr-FR');
                    
                    tbody.append(`
                        <tr>
                            <td>${produit.nom}</td>
                            <td>${produit.prix}€</td>
                            <td>${produit.quantite}</td>
                            <td>${dateAjout}</td>
                        </tr>
                    `);
                });
            }).fail(function(error) {
                console.error('Erreur:', error);
            });
        }
    </script>
</body>
</html>
```

## Fonctionnalités implémentées

1. **Recherche par plage de dates** : Entre deux dates, depuis une date, ou jusqu'à une date
2. **Affichage tabulaire** : Résultats présentés dans un tableau propre
3. **Formatage des dates** : Conversion au format local français
4. **Interface intuitive** : Avec des sélecteurs de date natifs

## Améliorations possibles

1. **Validation des dates** : Vérifier que date_debut <= date_fin
2. **Pagination** : Pour les grands ensembles de résultats
3. **Tri des colonnes** : Permettre de trier par nom, prix, etc.
4. **Export des résultats** : En CSV ou PDF

Pour utiliser cette application :
1. Placez les fichiers dans la structure décrite précédemment
2. Exécutez `python app.py`
3. Accédez à `http://localhost:5000` dans votre navigateur
4. Sélectionnez des dates et cliquez sur "Rechercher"




Voici une conception POO complète pour votre système de gestion de véhicules avec héritage et gestion des différentes fonctionnalités :

1. Structure de base (Fichier models.py)
python
from datetime import datetime
import sqlite3
from abc import ABC, abstractmethod

class DatabaseManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect('vehicules.db')
            cls._instance.create_tables()
        return cls._instance
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Table Véhicules
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS vehicules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            marque TEXT NOT NULL,
            modele TEXT NOT NULL,
            immatriculation TEXT UNIQUE NOT NULL,
            annee INTEGER,
            kilometrage INTEGER DEFAULT 0,
            disponible BOOLEAN DEFAULT 1,
            specifics TEXT  # JSON pour les spécifiques par type
        )
        ''')
        
        # Tables autres (entretiens, locations, etc.)
        # ... (voir structures précédentes)
        
        self.conn.commit()
    
    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
    
    def close(self):
        self.conn.close()

class Vehicule(ABC):
    def __init__(self, marque: str, modele: str, immatriculation: str, annee: int, kilometrage: int = 0):
        self.marque = marque
        self.modele = modele
        self.immatriculation = immatriculation
        self.annee = annee
        self.kilometrage = kilometrage
        self.disponible = True
        self.db = DatabaseManager()
    
    @abstractmethod
    def get_type(self):
        pass
    
    def save(self):
        specifics = self.get_specifics()
        query = '''
        INSERT INTO vehicules 
        (type, marque, modele, immatriculation, annee, kilometrage, disponible, specifics)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            self.get_type(),
            self.marque,
            self.modele,
            self.immatriculation,
            self.annee,
            self.kilometrage,
            self.disponible,
            specifics
        )
        cursor = self.db.execute_query(query, params)
        return cursor.lastrowid
    
    @abstractmethod
    def get_specifics(self):
        pass
    
    def generer_fiche_technique(self):
        return {
            "Marque": self.marque,
            "Modèle": self.modele,
            "Immatriculation": self.immatriculation,
            "Année": self.annee,
            "Kilométrage": self.kilometrage,
            "Type": self.get_type(),
            **self.get_specifics()
        }

class Voiture(Vehicule):
    def __init__(self, marque: str, modele: str, immatriculation: str, annee: int, 
                 nb_portes: int, carburant: str, kilometrage: int = 0):
        super().__init__(marque, modele, immatriculation, annee, kilometrage)
        self.nb_portes = nb_portes
        self.carburant = carburant
    
    def get_type(self):
        return "voiture"
    
    def get_specifics(self):
        return {
            "nb_portes": self.nb_portes,
            "carburant": self.carburant
        }

class Camion(Vehicule):
    def __init__(self, marque: str, modele: str, immatriculation: str, annee: int, 
                 ptac: float, volume_cargo: float, kilometrage: int = 0):
        super().__init__(marque, modele, immatriculation, annee, kilometrage)
        self.ptac = ptac  # Poids Total Autorisé en Charge
        self.volume_cargo = volume_cargo
    
    def get_type(self):
        return "camion"
    
    def get_specifics(self):
        return {
            "ptac": self.ptac,
            "volume_cargo": self.volume_cargo
        }

class Moto(Vehicule):
    def __init__(self, marque: str, modele: str, immatriculation: str, annee: int, 
                 cylindree: int, type_moto: str, kilometrage: int = 0):
        super().__init__(marque, modele, immatriculation, annee, kilometrage)
        self.cylindree = cylindree
        self.type_moto = type_moto
    
    def get_type(self):
        return "moto"
    
    def get_specifics(self):
        return {
            "cylindree": self.cylindree,
            "type_moto": self.type_moto
        }

class Entretien:
    def __init__(self, vehicule_id: int, date: str, type_entretien: str, 
                 description: str, cout: float, kilometrage: int, statut: str = "programme"):
        self.vehicule_id = vehicule_id
        self.date = date
        self.type_entretien = type_entretien
        self.description = description
        self.cout = cout
        self.kilometrage = kilometrage
        self.statut = statut
        self.db = DatabaseManager()
    
    def save(self):
        query = '''
        INSERT INTO entretiens 
        (vehicule_id, date, type, description, cout, kilometrage, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            self.vehicule_id,
            self.date,
            self.type_entretien,
            self.description,
            self.cout,
            self.kilometrage,
            self.statut
        )
        cursor = self.db.execute_query(query, params)
        return cursor.lastrowid

class Carburant:
    def __init__(self, vehicule_id: int, date: str, litres: float, prix_litre: float, 
                 km_parcourus: int, km_compteur: int):
        self.vehicule_id = vehicule_id
        self.date = date
        self.litres = litres
        self.prix_litre = prix_litre
        self.km_parcourus = km_parcourus
        self.km_compteur = km_compteur
        self.db = DatabaseManager()
    
    def save(self):
        query = '''
        INSERT INTO carburant 
        (vehicule_id, date, litres, prix_litre, km_parcourus, km_compteur)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        params = (
            self.vehicule_id,
            self.date,
            self.litres,
            self.prix_litre,
            self.km_parcourus,
            self.km_compteur
        )
        cursor = self.db.execute_query(query, params)
        return cursor.lastrowid
    
    def calcul_consommation(self):
        return (self.litres / self.km_parcourus) * 100 if self.km_parcourus > 0 else 0

class Location:
    def __init__(self, vehicule_id: int, client_id: int, date_debut: str, date_fin: str, 
                 prix_journalier: float, caution: float, statut: str = "reservation"):
        self.vehicule_id = vehicule_id
        self.client_id = client_id
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.prix_journalier = prix_journalier
        self.caution = caution
        self.statut = statut
        self.db = DatabaseManager()
    
    def save(self):
        prix_total = self.calcul_prix_total()
        query = '''
        INSERT INTO locations 
        (vehicule_id, client_id, date_debut, date_fin, prix_total, caution, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            self.vehicule_id,
            self.client_id,
            self.date_debut,
            self.date_fin,
            prix_total,
            self.caution,
            self.statut
        )
        cursor = self.db.execute_query(query, params)
        
        # Mettre à jour la disponibilité du véhicule
        if self.statut in ("active", "reservation"):
            self.db.execute_query(
                "UPDATE vehicules SET disponible = 0 WHERE id = ?", 
                (self.vehicule_id,)
            )
        
        return cursor.lastrowid
    
    def calcul_prix_total(self):
        debut = datetime.strptime(self.date_debut, '%Y-%m-%d')
        fin = datetime.strptime(self.date_fin, '%Y-%m-%d')
        jours = (fin - debut).days + 1
        return jours * self.prix_journalier

class FicheTechnique:
    @staticmethod
    def generer(vehicule_id: int):
        db = DatabaseManager()
        cursor = db.execute_query(
            "SELECT * FROM vehicules WHERE id = ?", 
            (vehicule_id,)
        )
        vehicule_data = cursor.fetchone()
        
        if not vehicule_data:
            return None
        
        # Créer le bon type de véhicule
        vehicule_class = {
            "voiture": Voiture,
            "camion": Camion,
            "moto": Moto
        }.get(vehicule_data["type"])
        
        if not vehicule_class:
            return None
        
        specifics = eval(vehicule_data["specifics"]) if vehicule_data["specifics"] else {}
        
        vehicule = vehicule_class(
            marque=vehicule_data["marque"],
            modele=vehicule_data["modele"],
            immatriculation=vehicule_data["immatriculation"],
            annee=vehicule_data["annee"],
            kilometrage=vehicule_data["kilometrage"],
            **specifics
        )
        
        return vehicule.generer_fiche_technique()
2. Utilisation des classes
Ajout d'un véhicule :

python
# Création d'une voiture
ma_voiture = Voiture(
    marque="Toyota",
    modele="Corolla",
    immatriculation="AB-123-CD",
    annee=2020,
    nb_portes=5,
    carburant="diesel",
    kilometrage=15000
)
voiture_id = ma_voiture.save()

# Création d'un camion
mon_camion = Camion(
    marque="Renault",
    modele="Master",
    immatriculation="EF-456-GH",
    annee=2019,
    ptac=3.5,
    volume_cargo=12.5
)
camion_id = mon_camion.save()
Ajout d'un entretien :

python
entretien = Entretien(
    vehicule_id=voiture_id,
    date="2023-06-15",
    type_entretien="vidange",
    description="Vidange complète avec filtre à huile",
    cout=89.90,
    kilometrage=15000
)
entretien_id = entretien.save()
Ajout d'une consommation de carburant :

python
carburant = Carburant(
    vehicule_id=voiture_id,
    date="2023-06-10",
    litres=45.2,
    prix_litre=1.65,
    km_parcourus=320,
    km_compteur=15000
)
carburant_id = carburant.save()
print(f"Consommation: {carburant.calcul_consommation():.1f} L/100km")
Gestion d'une location :

python
location = Location(
    vehicule_id=voiture_id,
    client_id=1,
    date_debut="2023-07-01",
    date_fin="2023-07-10",
    prix_journalier=50.0,
    caution=500.0
)
location_id = location.save()
Génération d'une fiche technique :

python
fiche = FicheTechnique.generer(voiture_id)
print("Fiche technique:", fiche)
3. Avantages de cette architecture
Héritage et polymorphisme :

Types de véhicules spécifiques avec attributs propres

Méthodes communes dans la classe parente Vehicule

Encapsulation :

Logique métier encapsulée dans les classes

Gestion de la base de données centralisée

Extensibilité :

Facile d'ajouter de nouveaux types de véhicules

Méthodes spécifiques par type de véhicule

Réutilisabilité :

Classes utilisables dans différentes parties de l'application

Logique de calcul centralisée (consommation, prix location, etc.)

Gestion des données techniques :

Fiches techniques générées dynamiquement

Spécificités stockées en JSON dans la base de données

Cette structure permet une séparation claire des responsabilités et une bonne maintenabilité du code. Vous pouvez facilement étendre le système avec de nouvelles fonctionnalités en ajoutant des méthodes aux classes existantes ou en créant de nouvelles classes.

Pour générer et écrire dans un fichier PDF avec des titres, des listes simples et des paragraphes en Python, vous pouvez utiliser la bibliothèque reportlab. Voici un exemple simple et commenté :

Installation
Si vous ne l'avez pas déjà installé :

bash
pip install reportlab
Exemple de code
python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# Créer un fichier PDF
doc = SimpleDocTemplate("exemple.pdf", pagesize=letter)

# Liste pour contenir les éléments du PDF
elements = []

# Obtenir les styles par défaut
styles = getSampleStyleSheet()

# Ajouter un style personnalisé pour le titre principal
styles.add(ParagraphStyle(
    name="TitrePrincipal",
    fontSize=20,
    alignment=TA_CENTER,
    spaceAfter=20
))

# Ajouter un style pour les sous-titres
styles.add(ParagraphStyle(
    name="SousTitre",
    fontSize=14,
    spaceBefore=15,
    spaceAfter=10
))

# Ajouter un style pour les paragraphes
styles.add(ParagraphStyle(
    name="Paragraphe",
    fontSize=12,
    spaceAfter=12,
    leading=14  # Interligne
))

# Titre principal
titre_principal = Paragraph("Mon Document PDF", styles["TitrePrincipal"])
elements.append(titre_principal)

# Sous-titre 1
sous_titre1 = Paragraph("1. Introduction", styles["SousTitre"])
elements.append(sous_titre1)

# Paragraphe
paragraphe1 = Paragraph(
    "Ceci est un paragraphe d'introduction. ReportLab permet de générer des PDF facilement en Python. "
    "Vous pouvez ajouter du texte formaté, des listes et des images.",
    styles["Paragraphe"]
)
elements.append(paragraphe1)

# Sous-titre 2
sous_titre2 = Paragraph("2. Liste Simple", styles["SousTitre"])
elements.append(sous_titre2)

# Liste à puces (simulée avec des paragraphes)
liste_items = [
    "Premier élément de la liste",
    "Deuxième élément",
    "Troisième élément"
]

for item in liste_items:
    elements.append(Paragraph(f"• {item}", styles["Paragraphe"]))

# Ajouter un espace
elements.append(Spacer(1, 20))

# Sous-titre 3
sous_titre3 = Paragraph("3. Conclusion", styles["SousTitre"])
elements.append(sous_titre3)

# Dernier paragraphe
paragraphe_final = Paragraph(
    "Voilà un exemple simple de création de PDF avec Python et ReportLab. "
    "Vous pouvez personnaliser les styles, les polices et la mise en page.",
    styles["Paragraphe"]
)
elements.append(paragraphe_final)

# Générer le PDF
doc.build(elements)

print("PDF généré avec succès !")
Explications :
SimpleDocTemplate : Structure de base du PDF.

Paragraph : Pour insérer du texte formaté (titres, paragraphes).

Spacer : Pour ajouter des espaces entre les éléments.

Styles :

TitrePrincipal : Style centré en gros.

SousTitre : Style pour les sections.

Paragraphe : Style pour le texte normal.

Liste à puces : Simulée avec • devant chaque élément.

Résultat :
Le PDF généré contiendra :

Un titre principal centré.

Des sections avec sous-titres.

Des paragraphes justifiés.

Une liste simple.

Alternatives :
Pour des tableaux : Utiliser Table de reportlab.platypus.

Pour des images : Image de reportlab.platypus.

Pour plus de flexibilité : PyPDF2 (manipulation de PDF existants) ou fpdf2 (une autre bibliothèque de génération PDF).

Si vous avez besoin d'une solution plus avancée (comme des en-têtes/pieds de page), dites-le-moi !

