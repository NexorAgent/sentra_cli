from click.testing import CliRunner

from sentra_cli.cli import main


def test_init_creates_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr("sentra_cli.cli.project_root", lambda: tmp_path)
    runner = CliRunner()
    res = runner.invoke(main, ["init"])
    assert res.exit_code == 0
    for d in ("data", "models", "notebooks", "logs"):
        assert (tmp_path / d).is_dir()
        assert (tmp_path / d / ".gitkeep").exists()


def test_model_fetch_file_url(tmp_path, monkeypatch):
    src = tmp_path / "dummy.txt"
    src.write_text("hello")
    monkeypatch.setattr("sentra_cli.cli.project_root", lambda: tmp_path)
    runner = CliRunner()
    file_url = f"file://{src}"
    res = runner.invoke(main, ["model", "fetch", "dummy", "--url", file_url])
    assert res.exit_code == 0
    dest = tmp_path / "models" / "dummy.txt"
    assert dest.exists()
    assert dest.read_text() == "hello"
