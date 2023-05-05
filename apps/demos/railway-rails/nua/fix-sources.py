from pathlib import Path

gemfile = Path("src/Gemfile").read_text()
gemfile = gemfile.replace('ruby "3.1.2"', 'ruby "3.0.2"')
Path("src/Gemfile").write_text(gemfile)

Path("src/Gemfile.lock").unlink()
