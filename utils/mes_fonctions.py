
import pandas as pd
import random
from datetime import datetime
import os
# from faker import Faker

# def verifier_faker():
#     from faker import Faker

#     # Exemple de code utilisant Faker
#     fake = Faker()
#     print(fake.name())

def generer_fichier():
    # Créer une instance de Faker
    from faker import Faker  
    fake = Faker() 

    # Initialiser les listes de données
    data = {
        'numero_police': [],
        'date_edition': [],  
        'date_effet': [],
        'date_echeance': [],
        'numero_immatriculation': [],
        'statut_contrat': [],
        'entite': [],
        'type_intermediaire': [],
        'prime_nette': []
    }

    # Options possibles pour certaines colonnes
    statut_options = ['valide', 'expiré', 'annulé', 'suspendu']
    entite_options = ['NSIA', 'SUNU', 'LEADWAY']
    type_intermediaire_options = ['courtier', 'agent generale', 'bureau direct', 'banque assurance']

    # Générer 1000 lignes de données
    for _ in range(10000):
        numero_police = fake.unique.numerify('POL######')
        date_edition = fake.date_between(start_date='-5y', end_date='today')
        date_effet = fake.date_between(start_date=date_edition, end_date='+1y')
        date_echeance = fake.date_between(start_date=date_effet, end_date='+1y')
        numero_immatriculation = fake.unique.license_plate()
        statut_contrat = random.choice(statut_options)
        entite = random.choice(entite_options)
        type_intermediaire = random.choice(type_intermediaire_options)
        prime_nette = random.randint(0, 5000000)

        # Ajouter les données à la liste
        data['numero_police'].append(numero_police)
        data['date_edition'].append(date_edition)
        data['date_effet'].append(date_effet)
        data['date_echeance'].append(date_echeance) 
        data['numero_immatriculation'].append(numero_immatriculation)
        data['statut_contrat'].append(statut_contrat)
        data['entite'].append(entite)
        data['type_intermediaire'].append(type_intermediaire)
        data['prime_nette'].append(prime_nette) 
    
    # Obtenir la date du jour
    a = datetime.now().strftime("%d/%m/%Y %H:%M")
    a = a.replace('/', '-') 
    a = a.replace(' ', '')
    a = a.replace(':','')
    data['date_creation'] = a 
     
    old_path = "D:/BUREAU/infos/Projets_Personnels/Airflow_projet/Dossier_des_Fichiers/donnees_assurance_old.csv"
    new_path = "D:/BUREAU/infos/Projets_Personnels/Airflow_projet/Dossier_des_Fichiers/donnees_assurance_new.csv"
    
    # Créer un DataFrame
    new = pd.DataFrame(data)
    new.to_csv(new_path, index =False)

    if os.path.exists(old_path):
        old = pd.read_csv(old_path)
        old = pd.concat([new, old]).reset_index(drop=True)
        old.to_csv(old_path, index =False) 
        # return old 
    else: 
        old = new.copy()
        old.to_csv(old_path, index=False)
        # return old  

    ####### traitement des données 

