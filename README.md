***********************Configuration du yaml************************
Ce fichier contient plusieurs définitions de services :

airflow-scheduler- Le planificateur surveille toutes les tâches et DAG, puis déclenche les instances de tâches une fois leurs dépendances terminées.

airflow-webserver- Le serveur Web est disponible à l'adresse http://localhost:8080.

airflow-worker- Le travailleur qui exécute les tâches données par le planificateur.

airflow-triggerer- Le déclencheur exécute une boucle d'événements pour les tâches reportables.

airflow-init- Le service d'initialisation.

postgres- La base de données.

redis- Le courtier redis qui transmet les messages du planificateur au travailleur.

Facultativement, vous pouvez activer flower en ajoutant une option, par exemple , ou en la spécifiant explicitement sur la ligne de commande, par exemple .--profile flowerdocker compose --profile flower updocker compose up flower

flower- L'application florale pour surveiller l'environnement. Il est disponible sur http://localhost:5555.

Tous ces services vous permettent d'exécuter Airflow avec CeleryExecutor . Pour plus d'informations, consultez Présentation de l'architecture .

Certains répertoires du conteneur sont montés, ce qui signifie que leur contenu est synchronisé entre votre ordinateur et le conteneur.

./dags- vous pouvez mettre vos fichiers DAG ici.

./logs- contient les journaux de l'exécution des tâches et du planificateur.

./config- vous pouvez ajouter un analyseur de journaux personnalisé ou ajouter airflow_local_settings.py pour configurer la politique de cluster.

./plugins- vous pouvez mettre vos plugins personnalisés ici.

Ce fichier utilise la dernière image Airflow ( apache/airflow ). Si vous devez installer une nouvelle bibliothèque Python ou une nouvelle bibliothèque système, vous pouvez créer votre image .

************************Explication du yaml**************************

Ce fichier docker-compose.yml configure un cluster Apache Airflow utilisant CeleryExecutor avec Redis et PostgreSQL pour un environnement de développement local. Voici une explication détaillée des différentes sections et composants du fichier :

Introduction
Commentaire sur la licence : Le fichier commence par une déclaration de licence, indiquant que le code est sous licence Apache 2.0.
Avertissement : Il est indiqué que cette configuration est destinée au développement local et ne doit pas être utilisée en production.
Variables d'environnement supportées
Certaines variables d'environnement peuvent être définies pour personnaliser le comportement de l'installation, telles que AIRFLOW_IMAGE_NAME, AIRFLOW_UID, AIRFLOW_PROJ_DIR, etc.

Structure de base
Le fichier utilise Docker Compose pour définir plusieurs services nécessaires pour exécuter Airflow avec CeleryExecutor.

Services définis
* x-airflow-common
    x-airflow-common : Un alias YAML pour définir les paramètres communs à plusieurs services Airflow.
    image : Utilise l'image Docker apache/airflow:2.6.0 par défaut.
    environment : Définit les variables d'environnement pour configurer Airflow, comme le type d'exécuteur, les connexions à la base de données, le backend des résultats de Celery, etc.
    volumes : Monte les répertoires locaux pour les dags, les logs et les plugins dans les conteneurs.
    user : Définit l'utilisateur dans le conteneur Docker.
    depends_on : Définit les dépendances entre services, spécifiant que certains services doivent être sains avant de démarrer les services dépendants.
* postgres
    image : Utilise l'image postgres:13.
    environment : Définit les variables d'environnement pour PostgreSQL.
    volumes : Monte un volume Docker pour persister les données PostgreSQL.
    healthcheck : Définit un test de santé pour vérifier que PostgreSQL est prêt.
    restart : Redémarre le conteneur automatiquement en cas de problème.
    redis
    image : Utilise l'image redis:latest.
    expose : Expose le port 6379 pour Redis.
    healthcheck : Définit un test de santé pour vérifier que Redis est prêt.
    restart : Redémarre le conteneur automatiquement en cas de problème.
airflow-webserver
* <<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    command : Spécifie la commande webserver pour démarrer le serveur web Airflow.
    ports : Mappe le port 8080 du conteneur au port 8080 de l'hôte.
    healthcheck : Définit un test de santé pour vérifier que le serveur web est prêt.
    depends_on : Ajoute une dépendance au service airflow-init.
    airflow-scheduler
*<<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    command : Spécifie la commande scheduler pour démarrer le planificateur Airflow.
    healthcheck : Définit un test de santé pour vérifier que le planificateur est prêt.
    depends_on : Ajoute une dépendance au service airflow-init.
airflow-worker
*<<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    command : Spécifie la commande celery worker pour démarrer un worker Celery.
    healthcheck : Définit un test de santé pour vérifier que le worker est prêt.
    environment : Ajoute une variable d'environnement supplémentaire pour gérer l'arrêt des workers.
    depends_on : Ajoute une dépendance au service airflow-init.
    airflow-triggerer
*<<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    command : Spécifie la commande triggerer pour démarrer le service de déclenchement.
    healthcheck : Définit un test de santé pour vérifier que le service de déclenchement est prêt.
    depends_on : Ajoute une dépendance au service airflow-init.
    airflow-init
*<<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    entrypoint : Utilise /bin/bash comme point d'entrée.
    command : Exécute un script bash pour vérifier la version d'Airflow, les ressources disponibles, et créer les répertoires nécessaires avec les bonnes permissions.
    environment : Définit des variables d'environnement supplémentaires pour initialiser la base de données Airflow et créer un utilisateur admin.
    user : Définit l'utilisateur root pour ce conteneur spécifique.
    volumes : Monte le répertoire projet local dans le conteneur.
    airflow-cli
*<<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    profiles : Définit un profil pour le service.
    environment : Définit des variables d'environnement supplémentaires.
    command : Utilise bash comme commande pour le conteneur.
    flower
*<<: airflow-common : Hérite des paramètres définis dans x-airflow-common.
    command : Spécifie la commande celery flower pour démarrer l'interface Flower pour Celery.
    profiles : Définit un profil pour le service.
    ports : Mappe le port 5555 du conteneur au port 5555 de l'hôte.
    healthcheck : Définit un test de santé pour vérifier que Flower est prêt.
    depends_on : Ajoute une dépendance au service airflow-init.
Volumes
postgres-db-volume : Définit un volume Docker pour persister les données PostgreSQL.

* Conclusion
Ce fichier docker-compose.yml configure une instance Airflow complète avec PostgreSQL comme base de données et Redis comme broker pour Celery. Il utilise un alias YAML pour partager les configurations communes entre plusieurs services Airflow et définit des dépendances et des tests de santé pour s'assurer que les services démarrent dans le bon ordre et restent sains. Cette configuration est adaptée pour le développement local et permet de tester facilement les fonctionnalités d'Airflow dans un environnement Dockerisé.

*************************Construction de l'image**********************

docker build -t my-airflow-image .
* docker build pour construire l'image
* -t pour nommer l'image
* . Indique que le dockerfile se trouve dans le repertoire courant

docker run -d -p 8080:8080 --name my-airflow-container my-airflow-image
* docker run pour executer un conteneur
* -d execute le conteneur en mode détaché (en arriere plan)
* -p 8080:8080 mappe le port 8080 de l'hôte au port 8080 du conteneur (ajustez le port si nécessaire).
* --name my-airflow-container donne un nom au conteneur, ici my-airflow-container
* my-airflow-image est le nom de l'image à partir de laquelle le conteneur sera créé.

docker logs my-airflow-container
* Verifier les logs du conteneur pour s'assurer qu'il fonctionne correctement 

docker stop my-airflow-container
* Pour arreter le conteneur

docker start my-airflow-container
* Pour le redemarrer

docker rm my-airflow-container
* pour supprimer le conteneur

docker-compose up -d
* Avec un fichier yaml, si vous l'avez fait pour lancer le service Airflow avec vos configurations 

* DAns le fichier docker-compose yaml, il a fallu integrer