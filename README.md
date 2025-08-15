# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
# sentra_cli

**Sentra CLI** — Outils d'automatisation légers pour projets (IA / dev locaux / R&D).  
Un utilitaire minimaliste pour : scaffold de projet, gestion simple de modèles (download/cache), commandes de tests et checks rapides.

---

## Sommaire
- [But du projet](#but-du-projet)  
- [Quickstart](#quickstart)  
- [Usage (notice)](#usage-notice)  
- [Commandes détaillées](#commandes-détaillées)  
- [Développement & tests](#développement--tests)  
- [CI / Packaging](#ci--packaging)  
- [Dépannage rapide](#dépannage-rapide)  
- [Roadmap / Extensions possibles](#roadmap--extensions-possibles)  
- [Licence & Contact](#licence--contact)

---

## But du projet
`sentra_cli` est un **outil utilitaire** pensé pour te faire gagner du temps sur les tâches récurrentes :
- scaffolder une arborescence projet (data/models/notebooks/logs),  
- télécharger et mettre en cache des "modèles" ou fichiers (http(s) ou file://),  
- fournir des commandes utilitaires (status, test) simples à intégrer dans des scripts ou CI.

Cible : développeurs R&D/IA, devs BIM souhaitant automatiser des étapes locales.

---

## Quickstart

**Pré-requi­s** : Python 3.12, Git.

1. Cloner le repo :
```powershell
git clone https://github.com/NexorAgent/sentra_cli.git
cd sentra_cli

2. Créer et activer le virtualenv (Windows PowerShell) :

python -m venv .venv
.\.venv\Scripts\Activate.ps1

3.Installer le package en editable + dépendances dev :

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
python -m pip install -r requirements-dev.txt

4. Vérifier les hooks et tests

pre-commit install
pre-commit run --all-files
pytest -q

Usage — notice rapide

Exemple : venv activé et package installé en editable (pip install -e .).
Commande générale

sentra <command> [options]

Si sentra n’est pas trouvée (Windows), utilise :

python -m sentra_cli.cli <command> [options]

Commandes détaillées (notice)
sentra status

Affiche un état basique. Utile pour checks rapides (à étendre).
sentra status

# => Status: OK - implement checks

sentra init [--force]
Scaffold d’un squelette projet :
crée data/, models/, notebooks/, logs/
ajoute .gitkeep dans chaque dossier.
--force : supprime puis recrée les dossiers si existants.

sentra init
sentra init --force

sentra model fetch <name> --url <url>

Télécharge un fichier « modèle » et le stocke dans models/ du repo (racine détectée automatiquement).

url accepte : http://, https://, file://

Si --url absent, le CLI peut utiliser un mapping interne (configurable dans le code).

L’extension du fichier est déduite depuis l’URL ou le chemin source.

Exemples (Windows) :
# depuis fichier local (formel)
sentra model fetch dummy --url file:///C:/chemin/vers/mon/fichier.bin

# depuis path Windows (fonctionne aussi)
sentra model fetch dummy --url file://C:\chemin\vers\mon\fichier.txt

# depuis HTTP
sentra model fetch example-small --url https://example.com/models/example-small.bin
Remarques :
Les file:// sont normalisés pour Windows et POSIX.
Pour de gros fichiers, pense à ajouter contrôle checksum et extraction d’archives (feature possible).

sentra test
Lance pytest (le CLI ajoute src au PYTHONPATH si nécessaire).

Développement & tests
Style & hooks

Le repo utilise pre-commit avec black et ruff.
Pour travailler proprement :

pre-commit install
pre-commit run --all-files

Si ruff propose des corrections :
ruff format src\sentra_cli\cli.py tests\test_cli.py
ruff check --fix src\sentra_cli\cli.py tests\test_cli.py

Lancer les tests
pytest -q

Installer en  editable (dev)
python -m pip install -e .

CI / Packaging

Le workflow GitHub Actions (fichier .github/workflows/ci.yml) doit :

1.checkout,
2.setup-python (3.12),
3.pip install -e . (editable) + installer deps dev (requirements-dev.txt),
4.lancer ruff check ., black --check ., pytest -q.

Ceci garantit que la CI reproduit l’environnement dev et évite les hacks PYTHONPATH.

Dépannage rapide

.configparser.MissingSectionHeaderError / BOM
Vérifie l’encodage des fichiers de config (setup.cfg / pyproject.toml). Le BOM (EF BB BF) bloquera configparser. Réécris en UTF-8 sans BOM.

.sentra non trouvé sur Windows
Active le venv ou exécute python -m sentra_cli.cli <cmd>. Tu peux créer un shim .venv\Scripts\sentra.cmd pour développement local.
.ModuleNotFoundError: No module named 'click'
Installer click : python -m pip install click ou via requirements-dev.txt.
.Tests ne trouvent pas sentra_cli
Soit installer le package en editable (pip install -e .), soit ajouter PYTHONPATH=src dans l’environnement de test.
.Pre-commit fail / black error
Exécute localement pre-commit run --all-files, laisse black/ruff modifier et commit à nouveau (git add -A, git commit).

Roadmap / Extensions possibles

Idées à prioriser :

.Intégration Hugging Face Hub (téléchargement + caching + token management).
.Gestion d’archives (.zip, .tar.gz) : téléchargement → extraction automatique.
.Vérification checksum / signatures des fichiers téléchargés.
.Commandes additionnelles : sentra model list, sentra model remove, sentra backup.

Licence & Contact

Licence : MIT (ajoute un LICENSE si besoin).
Mainteneur local : Julien — ajoute mail ou lien GitHub si tu veux partager.