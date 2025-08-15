import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

import click


def project_root() -> Path:
    """
    Détecte la racine du projet:
    - le dossier courant s'il contient un marqueur (pyproject.toml, .git, requirements.txt)
    - sinon, remonte dans les parents
    - sinon, fallback: cwd
    """
    p = Path.cwd()
    markers = ("pyproject.toml", ".git", "requirements.txt")
    for parent in (p, *p.parents):
        if any((parent / m).exists() for m in markers):
            return parent
    return p


def _models_dir() -> Path:
    d = project_root() / "models"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _download_url_to_path(url: str, dest: Path) -> None:
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()

    if scheme in ("http", "https"):
        with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
            shutil.copyfileobj(r, f)
        return

    if scheme == "file":
        # Cas 1 (Windows «non canonique»): file://C:\path\to\file.txt
        #   -> urlparse.netloc contient "C:\path\to\file.txt", path est vide.
        # Cas 2 (canonique):                file:///C:/path/to/file.txt
        #   -> urlparse.path contient "/C:/path/to/file.txt"
        src_path = ""
        if os.name == "nt" and parsed.netloc and parsed.path in ("", "/"):
            src_path = unquote(parsed.netloc)  # ex: C:\Users\...\dummy.txt
        else:
            src_path = unquote(parsed.path)  # ex: /C:/Users/...  (à normaliser)
            if (
                os.name == "nt"
                and src_path.startswith("/")
                and len(src_path) > 3
                and src_path[2] == ":"
            ):
                src_path = src_path.lstrip("/")

        src = Path(src_path)
        if not src.exists():
            raise FileNotFoundError(src)
        shutil.copyfile(src, dest)
        return

    raise click.ClickException(f"Unsupported URL scheme: {scheme or '(none)'}")


@click.group()
def main():
    """Sentra CLI - automation helpers for SENTRA_CORE_MEM"""


@main.command()
def init():
    """Scaffold a basic project structure: - data/, models/, notebooks/, logs/"""
    root = project_root()
    created = []
    for name in ("data", "models", "notebooks", "logs"):
        p = root / name
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
            created.append(name)
        # Assure la présence d'un marqueur pour VCS
        (p / ".gitkeep").touch(exist_ok=True)
    click.echo(f"Created directories: {', '.join(created) if created else 'nothing to do'}")


@main.group()
def model():
    """Model related commands"""


@model.command("fetch")
@click.argument("name")
@click.option("--url", required=True, help="Source URL (http(s):// ou file://)")
def model_fetch(name: str, url: str):
    """Fetch a model and store it under <project>/models."""
    dest_dir = _models_dir()
    parsed = urlparse(url)
    filename = Path(unquote(parsed.path or parsed.netloc)).name or f"{name}.bin"
    dest = dest_dir / filename

    click.echo(f"Downloading {url} -> {dest}")
    try:
        _download_url_to_path(url, dest)
    except Exception as err:  # noqa: BLE001
        raise click.ClickException(f"Failed to fetch model: {err}") from err

    click.echo(f"Model saved to: {dest}")


@main.command()
def status():
    """Show status"""
    root = project_root()
    click.echo(f"Project root: {root}")
    for d in ("data", "models", "notebooks", "logs"):
        click.echo(f"- {d}/ {'OK' if (root / d).exists() else 'MISSING'}")


@main.command()
@click.option(
    "--use-local", is_flag=True, help="Run pytest with 'python -m pytest' from current shell."
)
def test(use_local: bool):
    """Run tests"""
    env = os.environ.copy()
    cmd = ["python", "-m", "pytest", "-q"] if use_local else [sys.executable, "-m", "pytest", "-q"]

    proc = subprocess.run(cmd, env=env, capture_output=True, text=True)
    if proc.returncode == 0:
        # Affiche tout de même la sortie résumé de pytest si utile
        if proc.stdout:
            click.echo(proc.stdout.rstrip())
        return

    output = (proc.stdout or "") + (proc.stderr or "")
    if "No module named pytest" in output:
        raise click.ClickException(
            "pytest n'est pas installé dans l'environnement courant.\n"
            "- pipx inject sentra-cli pytest   (si installé via pipx)\n"
            "- OU activez votre venv de projet puis: python -m pip install pytest\n"
            "- OU lancez: sentra test --use-local"
        )
    # Montre la sortie pour aider au debug
    if output.strip():
        click.echo(output.rstrip(), err=True)
    raise click.ClickException(f"Tests failed (exit code {proc.returncode}).")


if __name__ == "__main__":
    main()
