# Utiliser l'image de base Apache Airflow
#From pour dire que l'image qu'on tente de contruire sera basée sur l'image officile de Airflow
FROM apache/airflow:2.6.0  

# Installer des dépendances supplémentaires (exemple)
#Copie le ficier requirements.txt de notre repertoire locale vers l'image docker dans le repertoire /requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copier des fichiers supplémentaires si nécessaire
# COPY my_custom_scripts /opt/airflow/scripts/

# Définir le répertoire de travail
WORKDIR /opt/airflow

# Exposer le port utilisé par Airflow (facultatif si vous utilisez déjà le port via docker-compose.yml)
#EXPOSE 8080
