from sentra_cli import hello


def test_hello():
    assert hello("Julien") == "Hello, Julien!"
