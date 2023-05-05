from pathlib import Path

package_json = Path("src/package.json").read_text()
package_json = package_json.replace('"node": "14.21.2"', '"node": "14.21.3"')
Path("src/package.json").write_text(package_json)
