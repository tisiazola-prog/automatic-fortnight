from flask import Flask, render_template, jsonify , request
from utils.database import ( get_vehicules , filtre_vehicules , get_carburants , get_showOneVehicule 
    ,add_vehicule , get_totalVehicule)
from flask import Flask, request, jsonify, render_template, url_for
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['UPLOAD_FOLDER'] = 'static/upload'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Désactive le cache


if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/')
def index():
    return render_template('admin.html', title=" Agence MobiDrive")


@app.route('/routeVehicule')
def routeVehicule():
    return render_template('vehicule.html', title="Agence MobiDrive")

@app.route('/location')
def location():
    return render_template('location.html', title="Agence MobiDrive")

# Route API pour récupérer les véhicules
@app.route('/api/vehicules', methods=['GET'])
def vehicules_api():
    try:
        data = get_vehicules()  # Récupération des données
        if data is not None:
            print(data)
            return jsonify(data), 200
           #Retourne les données avec un code 200
        else:
            return jsonify({'error': 'Erreur lors de la récupération des données'}), 500  #Erreur 500 si aucune donnée
    except Exception as e:
        return jsonify({'error': str(e)}), 500  #Retourne l'erreur si une exception est levée
    
    
    
@app.route('/api/showOneVehicule', methods=['GET'])
def showOneVehicule_api():
    try:
        
        vehicules_id = request.args.get('vehicule_id' , '').strip()
        vehicules_type = request.args.get('vehicule_type' , '').strip()
        
        
        if vehicules_id and vehicules_type:
            data = get_showOneVehicule(vehicules_id , vehicules_type)
            
            print(data)
            
            if data is not None:
                return jsonify(data), 200  #Retourne les données avec un code 200
            else:
                return jsonify({'error': 'Erreur lors de la récupération des données'}), 500
    
        return jsonify({
            'vehicules_id' : vehicules_id ,
            'vehicules_type' : vehicules_type
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500  #Retourne l'erreur si une exception est levée
    
    

@app.route('/api/action', methods=['POST'])  # Changé en POST pour la sécurité
def action_api():
    try:
        data = request.get_json()
        action = data.get('action', '').strip()
        vehicule_id = data.get('vehicule_id', '').strip()
        message = action
      
        
        if not action or not vehicule_id:
            return jsonify({'error': 'Paramètres manquants'}), 400
        
        return jsonify({'message': message}), 200
        
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/filtreVehicules')
def filtreVehicules():
    type_vehicule = request.args.get('type', '').strip()  # J'ai renommé "type" en "type_vehicule"
    marque = request.args.get('marque', '').strip()

    resultats = filtre_vehicules(type_vehicule, marque);
    return jsonify([dict(row) for row in resultats])



@app.route('/api/carburants', methods=['GET'])
def carburant_api():
    try:
        data = get_carburants()
        if data is not None:
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Erreur lors de la récupération des données'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

@app.route('/ajouterVehicule', methods=['POST'])
def ajouterVehicule():
    
    try:
        
        data = request.get_json() 
        
        # Récupérer les données du formulaire
        type_vehicule = data.get('type_vehicule')
        marque = data.get('marque')
        modele = data.get('modele')
        immatriculation = data.get('immatriculation')
        annee = data.get('annee')
        capacite = data.get('capacite')
        kilometrage = data.get('kilometrage')
        image = data.get('image')
        cylindre = data.get('cylindre')
        nb_place = data.get('nb_place')
        
        
        image_path = None
        if 'image' in request.files:
            
            file = request.files['image']
            
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = url_for('static', filename=f'upload/{filename}') 
                
        vehicule =  add_vehicule(
               type_vehicule , 
               marque, 
               modele, 
               immatriculation, 
               annee, 
               capacite, 
               kilometrage, 
               image_path, 
               nb_place, 
               cylindre 
            )
        
        if vehicule == True :
            return jsonify({
                'success': True, 
                'message': 'Véhicule ajouté avec succès'
            })
            
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Immatriculation déjà existante'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})
    


@app.route('/totalVehicule', methods=['GET'])
def totalVehicule():
    try:
        data = get_totalVehicule()
        if data is not None:
            return jsonify(data), 200
        else:
            return jsonify({'error': 'Erreur lors de la récupération des données'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    

if __name__ == '__main__':
    app.run(debug=True)  # Pour le développement