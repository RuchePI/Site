# Site Web du projet RuchePI

Ce dépôt contient le site Web permettant d'afficher les diverses données provenant des ruches. Le site est codé à le *framework* Django. Vous y trouverez ci-dessous les instructions pour l'installer.

## Installation d'une version locale

### Génération du *frontend*

Après avoir installé Node.js et les *packages* (`npm install`), il suffit de lancer Gulp.

```
gulp build
```

Il faut parfois relancer 2 à 3 fois cette commande pour que les fichiers soient générés entièrement. Les fichiers compilés se retrouveront dans le dossier `assets`.

Pour le développement, on peut utiliser

```
gulp watch
```

qui va regénérer les fichiers à chaque modification et permettre l'utilisation avec LiveReload.

Il est ensuite possible de nettoyer les fichiers inutiles au fonctionnement du site.

```
gulp clean
```

### Lancement du serveur

Django doit être installé ainsi que les diverses dépendances Python. Pour cela, on les installe en lançant la commande suivante.

```
sudo pip3 install -r requirements.txt
```

On lance ensuite le serveur en ayant pris soin de créer la base de données et le compte super-utilisateur.

```
python3 manage.py makemigrations beehive
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Installation en production

Il faut suivre les mêmes étapes que précedemment. Ensuite, on créé un ficher `rpi/settings_prod.py` avec le contenu suivant, la clé secrète et le mot de passe de la base sont à changer. Ici, la configuration est pour PythonAnywhere.

```python
# Prod settings

SECRET_KEY = ''

DEBUG = False

ALLOWED_HOSTS = [RPI_APP['domain'], ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'RuchePI.mysql.pythonanywhere-services.com',
        'NAME': 'RuchePI$rpi',
        'USER': 'RuchePI',
        'PASSWORD': '',
    }
}
```

Une clé secrète peut être générée avec le script `tools/gen_secret_key.py`.

Ensuite, on configure nginx et le serveur WSGI. Ne pas oublier de déservir les fichiers statiques qui se trouvent dans `assets/`.

## Bonnes pratiques

* L'indentation est uniquement réalisée avec 4 espaces et non des tabulations.
* Respectez [les conventions de codes de Django](https://docs.djangoproject.com/en/1.9/internals/contributing/writing-code/coding-style/), ce qui inclut la [PEP 008](https://www.python.org/dev/peps/pep-0008/) (sauf l'erreur E501 pour le dépassement des 80 caractères). Veuillez donc utiliser l'outil `flake8`.
* Vérifier qu'il n'y est pas d'indentations inutiles et d'espaces en fin de ligne.
```
./tools/find_trailing_spaces.sh
```
* Le code ainsi que les commentaires sont exclusivement en anglais.
* Les messages de *commits*, quant à eux, sont en français (avec majuscule au début !).
