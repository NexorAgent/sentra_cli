from sentra_cli.cli import model_fetch

# Exemple d'utilisation via module (script)
# Attention: exécuter depuis la racine du repo avec environnement activé
if __name__ == "__main__":
    # exemple utilisant un fichier local
    model_fetch.callback("demo", url="file:///C:/chemin/vers/ton/fichier.txt")
