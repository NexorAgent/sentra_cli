import os
import subprocess

import click


@click.group()
def main():
    """Sentra CLI - automation helpers for SENTRA_CORE_MEM"""
    pass


@main.command()
def status():
    """Show status"""
    click.echo("Status: OK - implement checks")


@main.command()
def test():
    """Run tests"""
    env = os.environ.copy()
    env["PYTHONPATH"] = env.get("PYTHONPATH", "") + os.pathsep + "src"
    subprocess.check_call(["pytest", "-q"], env=env)


if __name__ == "__main__":
    main()
