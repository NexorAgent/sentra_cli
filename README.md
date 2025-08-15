<!-- Badges -->
![CI](https://github.com/NexorAgent/sentra_cli/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![PyPI (placeholder)](https://img.shields.io/pypi/v/sentra-cli?label=PyPI)

# pytest cache directory #

This directory contains data from the pytest's cache plugin,
which provides the `--lf` and `--ff` options, as well as the `cache` fixture.

**Do not** commit this to version control.

See [the docs](https://docs.pytest.org/en/stable/how-to/cache.html) for more information.
# sentra_cli

**Sentra CLI** â€” Outils d'automatisation lÃ©gers pour projets (IA / dev locaux / R&D).  
Un utilitaire minimaliste pour : scaffold de projet, gestion simple de modÃ¨les (download/cache), commandes de tests et checks rapides.

---

## Sommaire
- [But du projet](#but-du-projet)  
- [Quickstart](#quickstart)  
- [Usage (notice)](#usage-notice)  
- [Commandes dÃ©taillÃ©es](#commandes-dÃ©taillÃ©es)  
- [DÃ©veloppement & tests](#dÃ©veloppement--tests)  
- [CI / Packaging](#ci--packaging)  
- [DÃ©pannage rapide](#dÃ©pannage-rapide)  
- [Roadmap / Extensions possibles](#roadmap--extensions-possibles)  
- [Licence & Contact](#licence--contact)

---

## But du projet
`sentra_cli` est un **outil utilitaire** pensÃ© pour te faire gagner du temps sur les tÃ¢ches rÃ©currentes :
- scaffolder une arborescence projet (data/models/notebooks/logs),  
- tÃ©lÃ©charger et mettre en cache des "modÃ¨les" ou fichiers (http(s) ou file://),  
- fournir des commandes utilitaires (status, test) simples Ã  intÃ©grer dans des scripts ou CI.

Cible : dÃ©veloppeurs R&D/IA, devs BIM souhaitant automatiser des Ã©tapes locales.

---

## Quickstart

**PrÃ©-requiÂ­s** : Python 3.12, Git.

1. Cloner le repo :
```powershell
git clone https://github.com/NexorAgent/sentra_cli.git
cd sentra_cli

2. CrÃ©er et activer le virtualenv (Windows PowerShell) :

python -m venv .venv
.\.venv\Scripts\Activate.ps1

3.Installer le package en editable + dÃ©pendances dev :

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e .
python -m pip install -r requirements-dev.txt

4. VÃ©rifier les hooks et tests

pre-commit install
pre-commit run --all-files
pytest -q

Usage â€” notice rapide

Exemple : venv activÃ© et package installÃ© en editable (pip install -e .).
Commande gÃ©nÃ©rale

sentra <command> [options]

Si sentra nâ€™est pas trouvÃ©e (Windows), utilise :

python -m sentra_cli.cli <command> [options]

Commandes dÃ©taillÃ©es (notice)
sentra status

Affiche un Ã©tat basique. Utile pour checks rapides (Ã  Ã©tendre).
sentra status

# => Status: OK - implement checks

sentra init [--force]
Scaffold dâ€™un squelette projet :
crÃ©e data/, models/, notebooks/, logs/
ajoute .gitkeep dans chaque dossier.
--force : supprime puis recrÃ©e les dossiers si existants.

sentra init
sentra init --force

sentra model fetch <name> --url <url>

TÃ©lÃ©charge un fichier Â« modÃ¨le Â» et le stocke dans models/ du repo (racine dÃ©tectÃ©e automatiquement).

url accepte : http://, https://, file://

Si --url absent, le CLI peut utiliser un mapping interne (configurable dans le code).

Lâ€™extension du fichier est dÃ©duite depuis lâ€™URL ou le chemin source.

Exemples (Windows) :
# depuis fichier local (formel)
sentra model fetch dummy --url file:///C:/chemin/vers/mon/fichier.bin

# depuis path Windows (fonctionne aussi)
sentra model fetch dummy --url file://C:\chemin\vers\mon\fichier.txt

# depuis HTTP
sentra model fetch example-small --url https://example.com/models/example-small.bin
Remarques :
Les file:// sont normalisÃ©s pour Windows et POSIX.
Pour de gros fichiers, pense Ã  ajouter contrÃ´le checksum et extraction dâ€™archives (feature possible).

sentra test
Lance pytest (le CLI ajoute src au PYTHONPATH si nÃ©cessaire).

DÃ©veloppement & tests
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

Ceci garantit que la CI reproduit lâ€™environnement dev et Ã©vite les hacks PYTHONPATH.

DÃ©pannage rapide

.configparser.MissingSectionHeaderError / BOM
VÃ©rifie lâ€™encodage des fichiers de config (setup.cfg / pyproject.toml). Le BOM (EF BB BF) bloquera configparser. RÃ©Ã©cris en UTF-8 sans BOM.

.sentra non trouvÃ© sur Windows
Active le venv ou exÃ©cute python -m sentra_cli.cli <cmd>. Tu peux crÃ©er un shim .venv\Scripts\sentra.cmd pour dÃ©veloppement local.
.ModuleNotFoundError: No module named 'click'
Installer click : python -m pip install click ou via requirements-dev.txt.
.Tests ne trouvent pas sentra_cli
Soit installer le package en editable (pip install -e .), soit ajouter PYTHONPATH=src dans lâ€™environnement de test.
.Pre-commit fail / black error
ExÃ©cute localement pre-commit run --all-files, laisse black/ruff modifier et commit Ã  nouveau (git add -A, git commit).

Roadmap / Extensions possibles

IdÃ©es Ã  prioriser :

.IntÃ©gration Hugging Face Hub (tÃ©lÃ©chargement + caching + token management).
.Gestion dâ€™archives (.zip, .tar.gz) : tÃ©lÃ©chargement â†’ extraction automatique.
.VÃ©rification checksum / signatures des fichiers tÃ©lÃ©chargÃ©s.
.Commandes additionnelles : sentra model list, sentra model remove, sentra backup.

Licence & Contact

Licence : MIT (ajoute un LICENSE si besoin).
Mainteneur local : Julien â€” ajoute mail ou lien GitHub si tu veux partager.
