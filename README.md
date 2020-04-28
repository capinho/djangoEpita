# EPITA gestion etudiants 

Voir demo du projet ici: http://epitagestetud.herokuapp.com/

**Projet Epita Dakar du cours de python**

Pour tester le projet localement il faut le cloner avec ```git clone https://github.com/capinho/djangoEpita.git```

Ce projet utilise la version 3.7 de python et 3.0 de django 
veuiller creer un environnement virtuel pour ne pas interferer avec vos autres projets python voir document sur windows >>https://docs.python.org/fr/3/library/venv.html

Mettez vous a l'interieur du projet et activez votre environnement virtuel et faite un ```pip install -r requirements.txt``` pour installer toutes les dependances du projet 
Pour la documentation de ```pip``` sur windows veuillez voir >>https://docs.aws.amazon.com/fr_fr/elasticbeanstalk/latest/dg/eb-cli3-install-windows.html

Ce projet utilise postgres comme base de donne ,vous changer les parametres de votre base de donnes au niveau du fichier ```settings.py```

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

pour creer un superutilisateur faite un ``` python manage.py createsuperuser```

Ensuite connectez-vous avec cet identifiant vous pourrez de la creer les etudiants et les professeur 


