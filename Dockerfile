# Utiliser l'image de base Apache Airflow
#From pour dire que l'image qu'on tente de contruire sera basée sur l'image officile de Airflow
FROM apache/airflow:2.6.0 

#Ajouter la variable PYTHONPATH
# ENV PYTHONPATH="/opt/airflow/dags:/opt/airflow/utils"


# Installer des dépendances supplémentaires (exemple)
#Copie le ficier requirements.txt de notre repertoire locale vers l'image docker dans le repertoire /requirements.txt
# COPY requirements.txt /requirements.txt
# RUN pip install --no-cache-dir -r /requirements.txt


COPY requirements.txt /opt/airflow/requirements.txt
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# # Copier des fichiers supplémentaires si nécessaire
# COPY my_custom_scripts /opt/airflow/scripts/

# Définir le répertoire de travail
WORKDIR /opt/airflow
# Copier les fichiers DAGs et utilitaires
COPY dags /opt/airflow/dags
COPY utils /opt/airflow/utils
# Exposer le port utilisé par Airflow (facultatif si vous utilisez déjà le port via docker-compose.yml)
#EXPOSE 8080

# COPY requirements.txt /opt/airflow/requirements.txt
# RUN pip install -r /opt/airflow/requirements.txt