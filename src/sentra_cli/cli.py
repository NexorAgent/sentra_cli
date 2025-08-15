import os
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlparse

import click


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


@click.group()
def main():
    """Sentra CLI - automation helpers for SENTRA_CORE_MEM"""
    pass


@main.command()
def status():
    """Show status"""
    click.echo("Status: OK - implement checks")


@main.command()
@click.option("--force", is_flag=True, help="Force recreate directories")
def init(force: bool):
    """
    Scaffold a basic project structure:
      - data/, models/, notebooks/, logs/
    """
    root = project_root()
    dirs = ["data", "models", "notebooks", "logs"]
    created = []
    for d in dirs:
        p = root / d
        if p.exists() and force:
            if p.is_dir():
                shutil.rmtree(p)
        if not p.exists():
            ensure_dir(p)
            (p / ".gitkeep").write_text("", encoding="utf-8")
            created.append(str(p.relative_to(root)))
    if created:
        click.echo("Created directories: " + ", ".join(created))
    else:
        click.echo("No directories created (already present).")


def _file_path_from_url(url: str) -> Path:
    """
    Robustly convert file:// URLs to local Path on both Windows and POSIX.
    Accepts forms like:
      file:///C:/path/to/file.txt
      file:///C:/path/to/file.txt
      file://localhost/C:/path/to/file.txt
      file:///some/unix/path
    Returns a pathlib.Path or None if the URL scheme is not file.
    """
    up = urlparse(url)
    if up.scheme != "file":
        return None

    # Build raw path from netloc and path parts.
    # Examples:
    #  - urlparse('file:///C:/a/b') => netloc='', path='/C:/a/b'
    #  - urlparse('file://C:/a/b')  => netloc='C:', path='/a/b'  (on some forms)
    #  - urlparse('file:///unix/path') => netloc='', path='/unix/path'
    if up.netloc and up.path:
        raw = up.netloc + up.path
    elif up.netloc:
        raw = up.netloc
    else:
        raw = up.path

    raw = unquote(raw)

    # Normalize for Windows: remove a leading slash if it produces '/C:...' -> 'C:...'
    if os.name == "nt":
        # Remove leading slashes (one or more) which can appear before "C:".
        raw = raw.lstrip("/")
        # Convert forward slashes to backslashes for consistency
        raw = raw.replace("/", os.sep)
    else:
        # POSIX: raw is fine (starts with '/')
        pass

    return Path(raw)


def _download_url_to_path(url: str, dest: Path):
    dest_parent = dest.parent
    ensure_dir(dest_parent)
    parsed = urlparse(url)
    if parsed.scheme == "file":
        src_path = _file_path_from_url(url)
        if not src_path or not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")
        shutil.copyfile(src_path, dest)
    else:
        # HTTP(S) download
        with urllib.request.urlopen(url) as resp:
            status = getattr(resp, "status", None)
            if status is not None and status != 200:
                raise RuntimeError(f"Download failed (status {status})")
            with open(dest, "wb") as out:
                out.write(resp.read())


@main.group()
def model():
    """Model related commands"""
    pass


@model.command("fetch")
@click.argument("name")
@click.option("--url", required=False, help="URL to download the model (http(s) or file://).")
def model_fetch(name: str, url: str):
    root = project_root()
    models_dir = root / "models"
    ensure_dir(models_dir)

    mapping = {"example-small": "https://example.com/some-model-file.bin"}

    if not url:
        if name in mapping:
            url = mapping[name]
            click.echo(f"Using mapped URL for {name}: {url}")
        else:
            raise click.UsageError("No URL provided and no mapping found for model: " + name)

    # choose extension: if file URL, use source suffix; else parse from URL path
    parsed = urlparse(url)
    if parsed.scheme == "file":
        src_path = _file_path_from_url(url)
        ext = src_path.suffix if src_path is not None else ".bin"
    else:
        ext = Path(parsed.path).suffix or ".bin"

    dest = models_dir / f"{name}{ext}"

    click.echo(f"Downloading {url} -> {dest}")
    try:
        _download_url_to_path(url, dest)
    except Exception as e:
        raise click.ClickException(f"Failed to fetch model: {e}") from e

    click.echo(f"Model saved to: {dest}")


@main.command()
def test():
    """Run tests"""
    env = os.environ.copy()
    env["PYTHONPATH"] = env.get("PYTHONPATH", "") + os.pathsep + "src"
    subprocess.check_call([sys.executable, "-m", "pytest", "-q"], env=env)


if __name__ == "__main__":
    main()
