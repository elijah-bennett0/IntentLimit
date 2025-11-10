import io
import yaml
import shutil
import zipfile
import tempfile
import requests
from pathlib import Path

__all__ = ["checkUpdate"]
from time import sleep

def checkUpdate(il):

	VERSION_URL = "https://raw.githubusercontent.com/elijah-bennett0/IntentLimit/main/config.yaml"
	ZIP_URL = "https://raw.githubusercontent.com/elijah-bennett0/IntentLimit/main/dist/IntentLimit-1.0.0.zip"
	vfile = Path(il.baseDir) / "config.yaml"
	config = yaml.safe_load(vfile.read_text(encoding="utf-8"))
	LOCAL_VER = str(config["version"])
	r = requests.get(VERSION_URL, timeout=15)
	r.raise_for_status()
	remote_config = yaml.safe_load(r.text)
	REMOTE_VER = str(remote_config["version"])
	INSTALL_DIR = Path(il.baseDir)

	if REMOTE_VER > LOCAL_VER:
		il.io.Print('w', "Update found. CTRL+C to cancel...")
		r2 = requests.get(ZIP_URL)
		r2.raise_for_status()
		zip_bytes = r2.content

		try:
			tmp_path = Path(tempfile.mkdtemp(prefix="update-"))
			with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
				zf.extractall(tmp_path)

			entries = list(tmp_path.iterdir())
			extracted_path = tmp_path
			if len(entries) == 1 and entries[0].is_dir():
				extracted_path = entries[0]

			parent = INSTALL_DIR.parent
			new_dir = parent / (INSTALL_DIR.name + ".new")
			bkp_dir = parent / (INSTALL_DIR.name + ".bak")

			if new_dir.exists():
				shutil.rmtree(new_dir)
			shutil.copytree(extracted_path, new_dir, dirs_exist_ok=False)

			if bkp_dir.exists():
				shutil.rmtree(bkp_dir)
			if INSTALL_DIR.exists():
				INSTALL_DIR.rename(bkp_dir)

			new_dir.rename(INSTALL_DIR)

			shutil.rmtree(bkp_dir, ignore_errors=True)
			il.io.Print('s', f"IntentLimit updated to version {REMOTE_VER}")
		finally:
			shutil.rmtree(tmp_path, ignore_errors=True)
	else:
		il.io.Print('s', f"IntentLimit version {LOCAL_VER} up-to-date.")

if __name__ == "__main__":
	checkUpdate()
