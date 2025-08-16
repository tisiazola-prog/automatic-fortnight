import sqlite3 

conn = sqlite3.connect('gestion_vehicule.db')
cursor = conn.cursor()

# Creating the Vehicule table
cursor.execute('''
    CREATE TABLE Vehicule (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        type TEXT NOT NULL CHECK(type IN ('Voiture', 'Camion', 'Moto')),
        marque TEXT NOT NULL,
        model TEXT NOT NULL,
        immatriculation TEXT NOT NULL,
        annee TEXT NOT NULL,
        capacite INTEGER NOT NULL,
        kilometrage INTEGER NOT NULL,
        image TEXT,
        prix INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'disponible' CHECK(status IN ('disponible', 'en location', 'en entretien')),
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Creating the Voiture table
cursor.execute('''
    CREATE TABLE "Voiture" (
        "voiture_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "vehicule_id" INTEGER NOT NULL,
        "nb_places" INTEGER NOT NULL,
        FOREIGN KEY("vehicule_id") REFERENCES "Vehicule"("id") ON DELETE CASCADE
    )
''')

# Creating the Camion table
cursor.execute('''
    CREATE TABLE "Camion" (
        "camion_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "vehicule_id" INTEGER NOT NULL,
        "nb_places" INTEGER NOT NULL,
        FOREIGN KEY("vehicule_id") REFERENCES "Vehicule"("id") ON DELETE CASCADE
    )
''')

# Creating the Moto table
cursor.execute('''
    CREATE TABLE "Moto" (
        "moto_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        "vehicule_id" INTEGER NOT NULL,
        "cylindree" TEXT NOT NULL,
        FOREIGN KEY("vehicule_id") REFERENCES "Vehicule"("id") ON DELETE CASCADE
    )
''')

# Creating the Client table
cursor.execute('''
    CREATE TABLE Client (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom_complet TEXT NOT NULL,
        telephone TEXT NOT NULL,
        adresse TEXT
    )
''')

# Creating the Location table
cursor.execute('''
    CREATE TABLE Location (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicule_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        date_debut TEXT NOT NULL,  
        date_fin TEXT NOT NULL,
        prix_total REAL NOT NULL,
        statut TEXT NOT NULL DEFAULT 'active' CHECK(statut IN ('active', 'terminee', 'annulee')),
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id),
        FOREIGN KEY (client_id) REFERENCES Client(id)
    )
''')

# Creating the Entretien table
cursor.execute('''
    CREATE TABLE Entretien (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicule_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        type TEXT NOT NULL,
        description TEXT,
        cout REAL NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id)
    )
''')

# Creating the Consommation table
cursor.execute('''
    CREATE TABLE Consommation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicule_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        litres REAL NOT NULL,
        km_parcourus INTEGER NOT NULL,
        cout_total REAL NOT NULL,
        FOREIGN KEY (vehicule_id) REFERENCES Vehicule(id)
    )
''')

# Data for voitures
voitures = [
    ("Voiture", "Toyota", "Corolla", "AA-123-BB", 2002, 20, 150, 5000, "voiture1.jpg", 5),
    ("Voiture", "Renault", "Clio", "CC-124-DD", 2019, 45000, 250, 6500, "voiture2.jpg", 2),
    ("Voiture", "Peugeot", "208", "EE-125-FF", 2021, 20000, 150, 4560, "voiture3.jpg", 9),
    ("Voiture", "Volkswagen", "Golf", "GG-126-HH", 2018, 60000, 260, 5892, "voiture4.jpg", 10),
    ("Voiture", "BMW", "Série 3", "II-127-JJ", 2022, 15000, 160, 10000, "voiture5.jpg", 15),
    ("Voiture", "Mercedes", "Classe A", "KK-128-LL", 2020, 30000, 250, 6920, "voiture6.jpg", 6),
    ("Voiture", "Audi", "A3", "MM-129-NN", 2019, 40000, 350, 2589, "voiture7.jpg", 4),
    ("Voiture", "Citroën", "C3", "OO-130-PP", 2021, 25000, 60, 236, "voiture8.jpg", 4),
    ("Voiture", "Ford", "Focus", "QQ-131-RR", 2018, 70000, 150, 14256, "voiture9.jpg", 8),
    ("Voiture", "Tesla", "Model 3", "SS-132-TT", 2022, 10000, 255, 257896, "voiture10.jpg", 6)
]

# Data for camions
camions = [
    ("Camion", "Volvo", "FH16", "UU-133-VV", 2019, 150000, 200, 4560, "camion1.jpg", 6),
    ("Camion", "MAN", "TGX", "WW-134-XX", 2020, 120000, 180, 6590, "camion2.jpg", 5),
    ("Camion", "Scania", "R450", "YY-135-ZZ", 2021, 80000, 220, 254, "camion3.jpg", 8),
    ("Camion", "Mercedes", "Actros", "A1-136-B2", 2018, 200000, 250, 4589, "camion4.jpg", 6),
    ("Camion", "Iveco", "Stralis", "E5-138-F6", 2019, 170000, 210, 2030, "camion6.jpg", 5),
    ("Camion", "Renault", "T Range", "G7-139-H8", 2021, 60000, 230, 6000, "camion7.jpg", 4),
    ("Camion", "Kenworth", "T680", "I9-140-J0", 2018, 180000, 270, 7000, "camion8.jpg", 10),
    ("Camion", "Mack", "Anthem", "M3-142-N4", 2022, 50000, 260, 95000, "camion10.jpg", 10)
]

# Data for motos
motos = [
    ("Moto", "Honda", "CBR 1000RR", "AB-123-CD", 2020, 12000, 100, 250, "moto1.jpg", "Mono-cylindre"),
    ("Moto", "Yamaha", "MT-07", "EF-456-GH", 2019, 15000, 689, 500, "moto2.jpg", "Bi-cylindre en ligne"),
    ("Moto", "Kawasaki", "Ninja 650", "IJ-789-KL", 2021, 8000, 649, 580, "moto3.jpg", "Bi-cylindre en V"),
    ("Moto", "Ducati", "Monster 821", "MN-101-OP", 2018, 20000, 821, 450, "moto4.jpg", "Bi-cylindre en V"),
    ("Moto", "BMW", "R 1250 GS", "QR-112-ST", 2022, 5000, 125, 590, "moto5.jpg", "Mono-cylindre"),
    ("Moto", "Suzuki", "GSX-R 750", "UV-131-WX", 2017, 25000, 750, 750, "moto6.jpg", "Quadri-cylindre en ligne"),
    ("Moto", "Triumph", "Bonneville T120", "YZ-415-AA", 2020, 10000, 120, 600, "moto7.jpg", "Quadri-cylindre en V"),
    ("Moto", "Harley-Davidson", "Fat Boy", "BB-516-CC", 2019, 18000, 174, 502, "moto8.jpg", "Quadri-cylindre en V"),
    ("Moto", "KTM", "1290 Super Duke R", "DD-717-EE", 2021, 9000, 1301, 1500, "moto9.jpg", "Bi-cylindre en V"),
    ("Moto", "Aprilia", "RSV4", "FF-818-GG", 2022, 3000, 109, 2506, "moto10.jpg", "Bi-cylindre en V")
]

# Inserting voitures into the database
for voiture in voitures:
    cursor.execute('''
        INSERT INTO Vehicule (type, marque, model, immatriculation, annee, capacite, kilometrage, prix, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', voiture[:9])
    
    vehicule_id1 = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO Voiture (vehicule_id, nb_places)
        VALUES (?, ?)
    ''', (vehicule_id1, voiture[9]))

# Inserting camions into the database
for camion in camions:
    cursor.execute('''
        INSERT INTO Vehicule (type, marque, model, immatriculation, annee, capacite, kilometrage, prix, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', camion[:9])
    
    vehicule_id2 = cursor.lastrowid
    
    cursor.execute('''
        INSERT INTO Camion (vehicule_id, nb_places)
        VALUES (?, ?)
    ''', (vehicule_id2, camion[9]))

# Inserting motos into the database
for moto in motos:
    cursor.execute('''
        INSERT INTO Vehicule (type, marque, model, immatriculation, annee, capacite, kilometrage, prix, image)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', moto[:9])

    vehicule_id3 = cursor.lastrowid

    cursor.execute('''
        INSERT INTO Moto (vehicule_id, cylindree)
        VALUES (?, ?)
    ''', (vehicule_id3, moto[9]))

# Commit the changes
conn.commit()

# Closing the connection
conn.close()