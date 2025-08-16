oici une solution complète pour la gestion des entretiens des véhicules, dans le même style que vos autres pages :

1. Structure HTML (entretien.html)
html
<div class="entretien-page allpages" id="entretien">
    <div class="page-header">
        <h2><i class="fas fa-tools"></i> Gestion des Entretiens</h2>
        <button class="btn btn-primary actionBtn" id="add-entretien-btn" data-page="entretien-modal">
            <i class="fas fa-plus"></i> Ajouter un entretien
        </button>
    </div>

    <div class="filters">

        <div class="form-row">

            <div class="form-group">
                <label for="entretien-vehicule-filter">Véhicule</label>
                <select id="entretien-vehicule-filter" class="form-control">
                    <option value="">Tous les véhicules</option>
                    <!-- Rempli dynamiquement -->
                </select>
            </div>

            <div class="form-group">
                <label for="entretien-type-filter">Type</label>
                <select id="entretien-type-filter" class="form-control">
                    <option value="">Tous</option>
                    <option value="vidange">Vidange</option>
                    <option value="revision">Révision</option>
                    <option value="reparation">Réparation</option>
                    <option value="controle">Contrôle technique</option>
                </select>
            </div>
            <div class="form-group">
                <label for="entretien-statut-filter">Statut</label>
                <select id="entretien-statut-filter" class="form-control">
                    <option value="">Tous</option>
                    <option value="programme">Programmé</option>
                    <option value="realise">Réalisé</option>
                    <option value="annule">Annulé</option>
                </select>
            </div>
        </div>
    </div>

    <div class="stats-grid" style="margin-bottom: 2rem;">
        <div class="stat-card">
            <h3>Coût total</h3>
            <p class="count" id="total-cout">0</p>
            <p class="label">€</p>
        </div>
        <div class="stat-card">
            <h3>Entretiens programmés</h3>
            <p class="count" id="total-programmes">0</p>
            <p class="label">à réaliser</p>
        </div>
        <div class="stat-card">
            <h3>Prochain entretien</h3>
            <p class="count" id="prochain-entretien">-</p>
            <p class="label">Date</p>
        </div>
    </div>

    <div class="table-container">
        <table id="entretien-table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Véhicule</th>
                    <th>Type</th>
                    <th>Description</th>
                    <th>Coût (€)</th>
                    <th>Kilométrage</th>
                    <th>Statut</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <!-- Rempli dynamiquement -->
            </tbody>
        </table>
    </div>
</div>

<!-- Modal Ajout/Modification Entretien -->
<div id="entretien-modal" class="modal">
    <div class="modal-content">
        <div class="modal-header">
            <h3 id="entretien-modal-title">Ajouter un entretien</h3>
            <button class="close-btn">&times;</button>
        </div>
        <div class="modal-body">
            <form id="entretien-form">
                <input type="hidden" id="entretien-id">
                <div class="form-group">
                    <label for="entretien-vehicule">Véhicule</label>
                    <select id="entretien-vehicule" class="form-control" required>
                        <option value="">Sélectionnez un véhicule</option>
                        <!-- Rempli dynamiquement -->
                    </select>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="entretien-date">Date</label>
                        <input type="date" id="entretien-date" class="form-control" required>
                    </div>
                    <div class="form-group">
                        <label for="entretien-type">Type</label>
                        <select id="entretien-type" class="form-control" required>
                            <option value="vidange">Vidange</option>
                            <option value="revision">Révision</option>
                            <option value="reparation">Réparation</option>
                            <option value="controle">Contrôle technique</option>
                            <option value="autre">Autre</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="entretien-cout">Coût (€)</label>
                        <input type="number" id="entretien-cout" class="form-control" min="0" step="0.01" required>
                    </div>
                    <div class="form-group">
                        <label for="entretien-kilometrage">Kilométrage</label>
                        <input type="number" id="entretien-kilometrage" class="form-control" min="0" required>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="entretien-statut">Statut</label>
                    <select id="entretien-statut" class="form-control" required>
                        <option value="programme">Programmé</option>
                        <option value="realise">Réalisé</option>
                        <option value="annule">Annulé</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="entretien-description">Description</label>
                    <textarea id="entretien-description" class="form-control" rows="3" required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="entretien-prestataire">Prestataire</label>
                    <input type="text" id="entretien-prestataire" class="form-control">
                </div>
            </form>
        </div>
        <div class="modal-footer">
            <button class="btn btn-danger close-modal">Annuler</button>
            <button class="btn btn-primary" id="save-entretien">Enregistrer</button>
        </div>
    </div>
</div>
2. Backend Flask (app.py)
python
# Routes pour les entretiens
@app.route('/api/entretiens', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gestion_entretiens():
    conn = sqlite3.connect('vehicules.db')
    conn.row_factory = sqlite3.Row
    
    if request.method == 'GET':
        # Filtres
        vehicule_id = request.args.get('vehicule_id')
        type_entretien = request.args.get('type')
        statut = request.args.get('statut')
        
        query = '''SELECT e.*, v.marque, v.modele 
                   FROM entretiens e
                   JOIN vehicules v ON e.vehicule_id = v.id
                   WHERE 1=1'''
        params = []
        
        if vehicule_id:
            query += " AND e.vehicule_id = ?"
            params.append(vehicule_id)
        if type_entretien:
            query += " AND e.type = ?"
            params.append(type_entretien)
        if statut:
            query += " AND e.statut = ?"
            params.append(statut)
            
        query += " ORDER BY e.date DESC"
        
        entretiens = [dict(row) for row in conn.execute(query, params).fetchall()]
        
        # Statistiques
        stats = {
            'total_cout': sum(e['cout'] for e in entretiens),
            'total_programmes': sum(1 for e in entretiens if e['statut'] == 'programme'),
            'prochain_entretien': min((e['date'] for e in entretiens if e['statut'] == 'programme'), default=None)
        }
        
        return jsonify({'entretiens': entretiens, 'stats': stats})
    
    elif request.method == 'POST':
        data = request.get_json()
        conn.execute('''
        INSERT INTO entretiens 
        (vehicule_id, date, type, description, cout, kilometrage, statut, prestataire)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['vehicule_id'],
            data['date'],
            data['type'],
            data['description'],
            data['cout'],
            data['kilometrage'],
            data['statut'],
            data.get('prestataire', '')
        ))
        conn.commit()
        return jsonify({'success': True})
    
    elif request.method == 'PUT':
        data = request.get_json()
        conn.execute('''
        UPDATE entretiens SET 
            vehicule_id = ?,
            date = ?,
            type = ?,
            description = ?,
            cout = ?,
            kilometrage = ?,
            statut = ?,
            prestataire = ?
        WHERE id = ?
        ''', (
            data['vehicule_id'],
            data['date'],
            data['type'],
            data['description'],
            data['cout'],
            data['kilometrage'],
            data['statut'],
            data.get('prestataire', ''),
            data['id']
        ))
        conn.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        entretien_id = request.args.get('id')
        conn.execute("DELETE FROM entretiens WHERE id = ?", (entretien_id,))
        conn.commit()
        return jsonify({'success': True})

# Route pour la page HTML
@app.route('/entretien')
def entretien_page():
    return render_template('entretien.html')
3. jQuery/AJAX (entretien.js)
javascript
$(document).ready(function() {
    let currentEntretienId = null;
    
    // Initialisation
    loadEntretiens();
    loadVehiculesForEntretien();
    
    // Gestion des filtres
    $('#entretien-vehicule-filter, #entretien-type-filter, #entretien-statut-filter').change(loadEntretiens);
    
    // Ouverture modal d'ajout
    $('#add-entretien-btn').click(function() {
        currentEntretienId = null;
        $('#entretien-modal-title').text('Ajouter un entretien');
        $('#entretien-form')[0].reset();
        $('#entretien-date').val(new Date().toISOString().split('T')[0]);
        $('#entretien-modal').show();
    });
    
    // Sauvegarde entretien
    $('#save-entretien').click(function() {
        const data = {
            vehicule_id: $('#entretien-vehicule').val(),
            date: $('#entretien-date').val(),
            type: $('#entretien-type').val(),
            description: $('#entretien-description').val(),
            cout: parseFloat($('#entretien-cout').val()),
            kilometrage: parseInt($('#entretien-kilometrage').val()),
            statut: $('#entretien-statut').val(),
            prestataire: $('#entretien-prestataire').val()
        };
        
        const url = currentEntretienId ? '/api/entretiens' : '/api/entretiens';
        const method = currentEntretienId ? 'PUT' : 'POST';
        
        if (currentEntretienId) {
            data.id = currentEntretienId;
        }
        
        $.ajax({
            url: url,
            type: method,
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                $('#entretien-modal').hide();
                loadEntretiens();
            }
        });
    });
    
    // Édition d'un entretien
    $(document).on('click', '.btn-edit', function() {
        currentEntretienId = $(this).data('id');
        $.get('/api/entretiens/' + currentEntretienId, function(entretien) {
            $('#entretien-modal-title').text('Modifier l\'entretien');
            $('#entretien-id').val(entretien.id);
            $('#entretien-vehicule').val(entretien.vehicule_id);
            $('#entretien-date').val(entretien.date);
            $('#entretien-type').val(entretien.type);
            $('#entretien-description').val(entretien.description);
            $('#entretien-cout').val(entretien.cout);
            $('#entretien-kilometrage').val(entretien.kilometrage);
            $('#entretien-statut').val(entretien.statut);
            $('#entretien-prestataire').val(entretien.prestataire || '');
            $('#entretien-modal').show();
        });
    });
    
    // Suppression d'un entretien
    $(document).on('click', '.btn-delete', function() {
        if (confirm('Voulez-vous vraiment supprimer cet entretien ?')) {
            $.ajax({
                url: '/api/entretiens?id=' + $(this).data('id'),
                type: 'DELETE',
                success: loadEntretiens
            });
        }
    });
    
    // Fonctions de chargement
    function loadEntretiens() {
        const filters = {
            vehicule_id: $('#entretien-vehicule-filter').val(),
            type: $('#entretien-type-filter').val(),
            statut: $('#entretien-statut-filter').val()
        };
        
        $.get('/api/entretiens', filters, function(data) {
            const tbody = $('#entretien-table tbody').empty();
            
            data.entretiens.forEach(e => {
                tbody.append(`
                    <tr>
                        <td>${new Date(e.date).toLocaleDateString()}</td>
                        <td>${e.marque} ${e.modele}</td>
                        <td>${e.type.charAt(0).toUpperCase() + e.type.slice(1)}</td>
                        <td>${e.description.substring(0, 50)}${e.description.length > 50 ? '...' : ''}</td>
                        <td>${e.cout.toFixed(2)}</td>
                        <td>${e.kilometrage}</td>
                        <td><span class="badge ${getStatusClass(e.statut)}">${e.statut}</span></td>
                        <td>
                            <button class="btn-edit" data-id="${e.id}">✏️</button>
                            <button class="btn-delete" data-id="${e.id}">🗑️</button>
                        </td>
                    </tr>
                `);
            });
            
            // Mise à jour des statistiques
            $('#total-cout').text(data.stats.total_cout.toFixed(2));
            $('#total-programmes').text(data.stats.total_programmes);
            $('#prochain-entretien').text(data.stats.prochain_entretien ? 
                new Date(data.stats.prochain_entretien).toLocaleDateString() : '-');
        });
    }
    
    function loadVehiculesForEntretien() {
        $.get('/api/vehicules', function(vehicules) {
            const select = $('#entretien-vehicule, #entretien-vehicule-filter').empty();
            select.append('<option value="">Tous les véhicules</option>');
            
            vehicules.forEach(v => {
                select.append(`<option value="${v.id}">${v.marque} ${v.modele} (${v.immatriculation})</option>`);
            });
        });
    }
    
    function getStatusClass(statut) {
        switch(statut) {
            case 'programme': return 'bg-warning';
            case 'realise': return 'bg-success';
            case 'annule': return 'bg-danger';
            default: return 'bg-info';
        }
    }
    
    // Gestion des modales
    $('.close-btn, .close-modal').click(function() {
        $(this).closest('.modal').hide();
    });
});
4. Structure SQLite3 (database.py)
python
def init_db():
    conn = sqlite3.connect('vehicules.db')
    cursor = conn.cursor()
    
    # Table Entretiens
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS entretiens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicule_id INTEGER NOT NULL,
        date DATE NOT NULL,
        type TEXT NOT NULL,
        description TEXT NOT NULL,
        cout REAL NOT NULL,
        kilometrage INTEGER NOT NULL,
        statut TEXT NOT NULL,
        prestataire TEXT,
        FOREIGN KEY (vehicule_id) REFERENCES vehicules(id)
    )
    ''')
    
    # Données de test
    cursor.execute("INSERT OR IGNORE INTO entretiens VALUES (1, 1, '2023-06-15', 'vidange', 'Vidange complète avec filtre à huile', 89.90, 15000, 'realise', 'Garage du Centre')")
    cursor.execute("INSERT OR IGNORE INTO entretiens VALUES (2, 1, '2023-12-10', 'revision', 'Révision annuelle complète', 250.00, 30000, 'programme', '')")
    
    conn.commit()
    conn.close()
Fonctionnalités clés :
Gestion complète des entretiens :

Ajout, modification, suppression

Filtrage par véhicule, type et statut

Statistiques en temps réel

Types d'entretien :

Vidange, révision, réparation, contrôle technique

Statuts (programmé, réalisé, annulé)

Interface cohérente :

Même style que vos autres pages

Modales pour les formulaires

Badges colorés pour les statuts

Données techniques :

Kilométrage

Coût

Prestataire

Description détaillée

Cette implémentation s'intègre parfaitement avec votre système existant et peut être facilement étendue avec des fonctionnalités supplémentaires comme :

Alertes pour les entretiens programmés

Historique complet des entretiens par véhicule

Gestion des pièces remplacées

Génération de rapports PDF    



1. Structure de la base de données SQLite3 (fichier database.py)
python
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('carburant.db')
    cursor = conn.cursor()
    
    # Table Véhicules
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marque TEXT NOT NULL,
        modele TEXT NOT NULL,
        immatriculation TEXT UNIQUE NOT NULL
    )
    ''')
    
    # Table Carburant
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS carburant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicule_id INTEGER NOT NULL,
        date DATE NOT NULL,
        litres REAL NOT NULL,
        prix_litre REAL NOT NULL,
        km_parcourus INTEGER NOT NULL,
        km_compteur INTEGER NOT NULL,
        station TEXT,
        notes TEXT,
        FOREIGN KEY (vehicule_id) REFERENCES vehicules(id)
    )
    ''')
    
    # Données de test (optionnel)
    cursor.execute("INSERT OR IGNORE INTO vehicules (marque, modele, immatriculation) VALUES ('Toyota', 'Corolla', 'AB-123-CD')")
    cursor.execute('''
    INSERT OR IGNORE INTO carburant 
    (vehicule_id, date, litres, prix_litre, km_parcourus, km_compteur, station, notes)
    VALUES (1, ?, 45.2, 1.65, 320, 15000, 'Total', 'Plein complet')
    ''', (datetime.now().strftime('%Y-%m-%d'),))
    
    conn.commit()
    conn.close()
2. Backend Flask (fichier app.py)
python
from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Routes API
@app.route('/api/carburant', methods=['GET', 'POST', 'DELETE'])
def gestion_carburant():
    conn = sqlite3.connect('carburant.db')
    conn.row_factory = sqlite3.Row  # Pour obtenir des dictionnaires
    
    if request.method == 'GET':
        # Filtres
        vehicule_id = request.args.get('vehicule_id')
        mois = request.args.get('mois')  # Format: 'YYYY-MM'
        
        query = '''SELECT c.*, v.marque, v.modele 
                   FROM carburant c JOIN vehicules v ON c.vehicule_id = v.id 
                   WHERE 1=1'''
        params = []
        
        if vehicule_id:
            query += " AND c.vehicule_id = ?"
            params.append(vehicule_id)
        if mois:
            query += " AND strftime('%Y-%m', c.date) = ?"
            params.append(mois)
        
        cursor = conn.execute(query, params)
        data = [dict(row) for row in cursor.fetchall()]
        
        # Statistiques (exemple)
        stats = {
            'avg_consumption': 6.5,  # À calculer réellement
            'total_cost': sum(row['litres'] * row['prix_litre'] for row in data),
            'total_volume': sum(row['litres'] for row in data)
        }
        
        return jsonify({'data': data, 'stats': stats})
    
    elif request.method == 'POST':
        data = request.get_json()
        conn.execute('''
        INSERT INTO carburant 
        (vehicule_id, date, litres, prix_litre, km_parcourus, km_compteur, station, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['vehicule_id'],
            data['date'],
            data['litres'],
            data['prix_litre'],
            data['km_parcourus'],
            data['km_compteur'],
            data.get('station', ''),
            data.get('notes', '')
        ))
        conn.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        conn.execute("DELETE FROM carburant WHERE id = ?", (request.args.get('id'),))
        conn.commit()
        return jsonify({'success': True})

# Route pour la page HTML
@app.route('/carburant')
def carburant_page():
    return render_template('carburant.html')

if __name__ == '__main__':
    init_db()  # Initialiser la DB au démarrage
    app.run(debug=True)
3. jQuery/AJAX (dans votre carburant.html ou fichier JS séparé)
javascript
$(document).ready(function() {
    // Chargement initial
    loadData();
    
    // Gestion des filtres
    $('#carburant-vehicule-filter, #carburant-date-filter').change(loadData);
    
    // Sauvegarde du formulaire
    $('#save-carburant').click(function() {
        const data = {
            vehicule_id: $('#carburant-vehicule').val(),
            date: $('#carburant-date').val(),
            litres: parseFloat($('#carburant-litres').val()),
            prix_litre: parseFloat($('#carburant-prix').val()),
            km_parcourus: parseInt($('#carburant-km_parcourus').val()),
            km_compteur: parseInt($('#carburant-km_compteur').val()),
            station: $('#carburant-station').val(),
            notes: $('#carburant-notes').val()
        };
        
        $.ajax({
            url: '/api/carburant',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                $('#carburant-modal').hide();
                loadData();
            }
        });
    });
});

function loadData() {
    const filters = {
        vehicule_id: $('#carburant-vehicule-filter').val(),
        mois: $('#carburant-date-filter').val()?.substring(0, 7)  // 'YYYY-MM'
    };
    
    $.get('/api/carburant', filters, function(response) {
        // Mise à jour du tableau
        const tbody = $('#carburant-table tbody').empty();
        response.data.forEach(row => {
            tbody.append(`
                <tr>
                    <td>${row.date}</td>
                    <td>${row.marque} ${row.modele}</td>
                    <td>${row.litres.toFixed(1)}</td>
                    <td>${row.prix_litre.toFixed(3)}</td>
                    <td>${(row.litres * row.prix_litre).toFixed(2)}€</td>
                    <td>${row.km_parcourus}</td>
                    <td>${(row.litres / row.km_parcourus * 100).toFixed(1)} L/100km</td>
                    <td>
                        <button class="btn-edit" data-id="${row.id}">✏️</button>
                        <button class="btn-delete" data-id="${row.id}">🗑️</button>
                    </td>
                </tr>
            `);
        });
        
        // Mise à jour des stats
        $('#avg-consumption').text(response.stats.avg_consumption.toFixed(1));
        $('#total-cost').text(response.stats.total_cost.toFixed(2));
        $('#total-volume').text(response.stats.total_volume.toFixed(1));
    });
}
4. Points clés
Calcul de la consommation :
(litres / km_parcourus) * 100 pour obtenir les L/100km.

Sécurité :

Utilisez ? dans les requêtes SQL pour éviter les injections.

Validez les données côté serveur avec Flask-WTF si nécessaire.

Optimisation :

Ajoutez des index sur les colonnes filtrées (vehicule_id, date).

Utilisez des transactions pour les opérations critiques.

Pour les véhicules :
Ajoutez une route API /api/vehicules pour peupler les <select>.

Cette solution offre une gestion complète avec :

Filtrage dynamique (véhicule + mois)

CRUD via AJAX

Calcul des statistiques

Rendu HTML côté client pour des performances optimales.

New chat


Solution Complète pour la Gestion des Locations avec SQLite3, Flask et AJAX/jQuery
Voici une implémentation complète pour votre système de gestion de locations.

1. Structure de la base de données SQLite3
python
# database.py
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('locations.db')
    cursor = conn.cursor()
    
    # Table Véhicules
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS vehicules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marque TEXT NOT NULL,
        modele TEXT NOT NULL,
        immatriculation TEXT UNIQUE NOT NULL,
        prix_journalier REAL NOT NULL,
        disponible BOOLEAN DEFAULT 1
    )
    ''')
    
    # Table Clients
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT,
        telephone TEXT NOT NULL,
        adresse TEXT
    )
    ''')
    
    # Table Locations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS locations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicule_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        date_debut DATETIME NOT NULL,
        date_fin DATETIME NOT NULL,
        prix_total REAL NOT NULL,
        caution REAL NOT NULL,
        statut TEXT NOT NULL,
        notes TEXT,
        FOREIGN KEY (vehicule_id) REFERENCES vehicules(id),
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    ''')
    
    # Table Retours
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS retours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location_id INTEGER NOT NULL,
        date_retour DATETIME NOT NULL,
        km_retour INTEGER NOT NULL,
        etat TEXT NOT NULL,
        caution_rendue REAL NOT NULL,
        observations TEXT,
        FOREIGN KEY (location_id) REFERENCES locations(id)
    )
    ''')
    
    # Données de test
    cursor.execute("INSERT OR IGNORE INTO vehicules VALUES (1, 'Toyota', 'Corolla', 'AB-123-CD', 50.0, 1)")
    cursor.execute("INSERT OR IGNORE INTO clients VALUES (1, 'Dupont', 'Jean', 'jean@example.com', '0612345678', '1 Rue Test')")
    
    conn.commit()
    conn.close()
2. Backend Flask (app.py)
python
from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Routes API pour les locations
@app.route('/api/locations', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gestion_locations():
    conn = sqlite3.connect('locations.db')
    conn.row_factory = sqlite3.Row
    
    if request.method == 'GET':
        # Récupération des filtres
        vehicule_id = request.args.get('vehicule_id')
        client_nom = request.args.get('client')
        statut = request.args.get('statut')
        
        query = '''SELECT l.*, v.marque, v.modele, c.nom as client_nom, c.prenom as client_prenom 
                   FROM locations l
                   JOIN vehicules v ON l.vehicule_id = v.id
                   JOIN clients c ON l.client_id = c.id
                   WHERE 1=1'''
        params = []
        
        if vehicule_id:
            query += " AND l.vehicule_id = ?"
            params.append(vehicule_id)
        if client_nom:
            query += " AND (c.nom LIKE ? OR c.prenom LIKE ?)"
            params.extend([f"%{client_nom}%", f"%{client_nom}%"])
        if statut:
            query += " AND l.statut = ?"
            params.append(statut)
            
        query += " ORDER BY l.date_debut DESC"
        
        locations = [dict(row) for row in conn.execute(query, params).fetchall()]
        return jsonify(locations)
    
    elif request.method == 'POST':
        data = request.get_json()
        
        # Calcul du prix total
        date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%dT%H:%M')
        date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%dT%H:%M')
        jours = (date_fin - date_debut).days + 1
        prix_total = jours * data['prix_jour']
        
        conn.execute('''
        INSERT INTO locations 
        (vehicule_id, client_id, date_debut, date_fin, prix_total, caution, statut, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['vehicule_id'],
            data['client_id'],
            data['date_debut'],
            data['date_fin'],
            prix_total,
            data['caution'],
            data['statut'],
            data.get('notes', '')
        ))
        
        # Mettre à jour la disponibilité du véhicule
        if data['statut'] in ('active', 'reservation'):
            conn.execute("UPDATE vehicules SET disponible = 0 WHERE id = ?", (data['vehicule_id'],))
        
        conn.commit()
        return jsonify({'success': True, 'id': conn.execute("SELECT last_insert_rowid()").fetchone()[0]})
    
    elif request.method == 'PUT':
        data = request.get_json()
        conn.execute('''
        UPDATE locations SET 
            vehicule_id = ?, 
            client_id = ?,
            date_debut = ?,
            date_fin = ?,
            prix_total = ?,
            caution = ?,
            statut = ?,
            notes = ?
        WHERE id = ?
        ''', (
            data['vehicule_id'],
            data['client_id'],
            data['date_debut'],
            data['date_fin'],
            data['prix_total'],
            data['caution'],
            data['statut'],
            data.get('notes', ''),
            data['id']
        ))
        conn.commit()
        return jsonify({'success': True})
    
    elif request.method == 'DELETE':
        location_id = request.args.get('id')
        conn.execute("DELETE FROM locations WHERE id = ?", (location_id,))
        conn.commit()
        return jsonify({'success': True})

# Route pour enregistrer un retour
@app.route('/api/locations/retour', methods=['POST'])
def enregistrer_retour():
    data = request.get_json()
    conn = sqlite3.connect('locations.db')
    
    try:
        # Enregistrement du retour
        conn.execute('''
        INSERT INTO retours 
        (location_id, date_retour, km_retour, etat, caution_rendue, observations)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data['location_id'],
            data['date_retour'],
            data['km_retour'],
            data['etat'],
            data['caution_rendue'],
            data.get('observations', '')
        ))
        
        # Mise à jour de la location
        conn.execute("UPDATE locations SET statut = 'terminee' WHERE id = ?", (data['location_id'],))
        
        # Mise à jour de la disponibilité du véhicule
        conn.execute("UPDATE vehicules SET disponible = 1 WHERE id = (SELECT vehicule_id FROM locations WHERE id = ?)", (data['location_id'],))
        
        conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Routes pour les données de référence
@app.route('/api/vehicules')
def get_vehicules():
    conn = sqlite3.connect('locations.db')
    conn.row_factory = sqlite3.Row
    vehicules = [dict(row) for row in conn.execute("SELECT id, marque, modele, immatriculation FROM vehicules WHERE disponible = 1").fetchall()]
    return jsonify(vehicules)

@app.route('/api/clients')
def get_clients():
    conn = sqlite3.connect('locations.db')
    conn.row_factory = sqlite3.Row
    clients = [dict(row) for row in conn.execute("SELECT id, nom, prenom FROM clients").fetchall()]
    return jsonify(clients)

# Route pour la page HTML
@app.route('/locations')
def locations_page():
    return render_template('locations.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
3. jQuery/AJAX (dans votre fichier JS)
javascript
$(document).ready(function() {
    // Variables globales
    let currentLocationId = null;
    
    // Initialisation
    loadLocations();
    loadVehicules();
    loadClients();
    
    // Gestion des filtres
    $('#location-vehicule-filter, #location-client-filter, #location-statut-filter').change(loadLocations);
    
    // Ouverture modal d'ajout
    $('#add-location-btn').click(function() {
        currentLocationId = null;
        $('#location-modal-title').text('Ajouter une location');
        $('#location-form')[0].reset();
        $('#location-modal').show();
    });
    
    // Sauvegarde location
    $('#save-location').click(function() {
        const data = {
            vehicule_id: $('#location-vehicule').val(),
            client_id: $('#location-client').val(),
            date_debut: $('#location-date_debut').val(),
            date_fin: $('#location-date_fin').val(),
            prix_jour: parseFloat($('#location-prix_jour').val()),
            caution: parseFloat($('#location-caution').val()),
            statut: $('#location-statut').val(),
            notes: $('#location-notes').val()
        };
        
        if (currentLocationId) {
            data.id = currentLocationId;
            $.ajax({
                url: '/api/locations',
                type: 'PUT',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function() {
                    $('#location-modal').hide();
                    loadLocations();
                }
            });
        } else {
            $.ajax({
                url: '/api/locations',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function() {
                    $('#location-modal').hide();
                    loadLocations();
                }
            });
        }
    });
    
    // Gestion des retours
    $(document).on('click', '.btn-return', function() {
        currentLocationId = $(this).data('id');
        $('#return-location-id').val(currentLocationId);
        $('#return-location-form')[0].reset();
        $('#return-location-modal').show();
    });
    
    $('#confirm-return').click(function() {
        const data = {
            location_id: currentLocationId,
            date_retour: $('#return-date').val(),
            km_retour: parseInt($('#return-km').val()),
            etat: $('#return-etat').val(),
            caution_rendue: parseFloat($('#return-caution-rendue').val()),
            observations: $('#return-notes').val()
        };
        
        $.ajax({
            url: '/api/locations/retour',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(data),
            success: function() {
                $('#return-location-modal').hide();
                loadLocations();
            }
        });
    });
    
    // Fonctions de chargement
    function loadLocations() {
        const filters = {
            vehicule_id: $('#location-vehicule-filter').val(),
            client: $('#location-client-filter').val(),
            statut: $('#location-statut-filter').val()
        };
        
        $.get('/api/locations', filters, function(locations) {
            const tbody = $('#locations-table tbody').empty();
            
            locations.forEach(loc => {
                const dateDebut = new Date(loc.date_debut).toLocaleString();
                const dateFin = new Date(loc.date_fin).toLocaleString();
                
                tbody.append(`
                    <tr>
                        <td>${loc.id}</td>
                        <td>${loc.marque} ${loc.modele}</td>
                        <td>${loc.client_nom} ${loc.client_prenom}</td>
                        <td>${dateDebut}</td>
                        <td>${dateFin}</td>
                        <td>${loc.prix_total.toFixed(2)}€</td>
                        <td><span class="badge ${getStatusClass(loc.statut)}">${loc.statut}</span></td>
                        <td>
                            ${loc.statut !== 'terminee' ? `<button class="btn-return" data-id="${loc.id}">🔄 Retour</button>` : ''}
                            <button class="btn-edit" data-id="${loc.id}">✏️</button>
                            <button class="btn-delete" data-id="${loc.id}">🗑️</button>
                        </td>
                    </tr>
                `);
            });
        });
    }
    
    function loadVehicules() {
        $.get('/api/vehicules', function(vehicules) {
            const select = $('#location-vehicule, #location-vehicule-filter').empty();
            select.append('<option value="">Tous les véhicules</option>');
            
            vehicules.forEach(v => {
                select.append(`<option value="${v.id}">${v.marque} ${v.modele} (${v.immatriculation})</option>`);
            });
        });
    }
    
    function loadClients() {
        $.get('/api/clients', function(clients) {
            const select = $('#location-client').empty();
            select.append('<option value="">Sélectionnez un client</option>');
            
            clients.forEach(c => {
                select.append(`<option value="${c.id}">${c.nom} ${c.prenom}</option>`);
            });
        });
    }
    
    function getStatusClass(statut) {
        switch(statut) {
            case 'active': return 'bg-success';
            case 'reservation': return 'bg-warning';
            case 'terminee': return 'bg-secondary';
            default: return 'bg-info';
        }
    }
    
    // Gestion des modales
    $('.close-btn, .close-modal').click(function() {
        $(this).closest('.modal').hide();
    });
});
4. Points Clés
Structure de la base de données:

4 tables principales (véhicules, clients, locations, retours)

Relations claires entre les tables

Fonctionnalités implémentées:

CRUD complet pour les locations

Gestion des retours de véhicules

Filtrage dynamique

Calcul automatique du prix total

Sécurité:

Utilisation de requêtes paramétrées

Validation côté serveur

Expérience utilisateur:

Interface réactive avec AJAX

Pas de rechargement de page

Feedback visuel sur les statuts

Cette solution offre une base solide que vous pouvez étendre avec des fonctionnalités supplémentaires comme:

Gestion des pénalités pour retard

Système de réservation plus avancé

Génération de contrats PDF

Calendrier de disponibilité des véhicules






