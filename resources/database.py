from pathlib import Path
from ruamel.yaml import YAML
from integrityCheck import readConfig
import hashlib
import re

__all__ = []

def safe_list(x):
	if not x:
		return []
	if isinstance(x, list):
		return [str(i).lower() for i in x]
	return [str(x).lower()]

def calcHash(TOOL_DIR, PLUGIN_DIR):
	'''This will hash all the configs IOT determine if something was changed'''
	h = hashlib.sha256()
	for root in (Path(TOOL_DIR), Path(PLUGIN_DIR)):
		# get all config.yaml files
		for cfg in sorted(root.rglob("config.yaml")):
			h.update(str(cfg.relative_to(root)).encode())
			h.update(cfg.read_bytes())
	return h.hexdigest()

def ensureDB(TOOL_DIR, PLUGIN_DIR, RESOURCE_DIR, il):
	'''This will check the stored hash to current calc hash and detect change'''
	currentHash = calcHash(TOOL_DIR, PLUGIN_DIR)
	hashFile = Path(RESOURCE_DIR) / "database.hash"
	db = Path(RESOURCE_DIR) / "database.yaml"

	if not hashFile.exists() or not db.exists():
		il.io.Print('i', "Hashfile not detected, generating hash and database...")
		createDB(TOOL_DIR, PLUGIN_DIR, RESOURCE_DIR, il)
		hashFile.write_text(currentHash)
		return
	stored = hashFile.read_text().strip()

	if stored != currentHash:
		il.io.Print('i', "Framework change detected, rebuilding database...")
		createDB(TOOL_DIR, PLUGIN_DIR, RESOURCE_DIR, il)
		hashFile.write_text(currentHash)

	il.io.Print('s', "Database check good.\n")


def createDB(TOOL_DIR, PLUGIN_DIR, RESOURCE_DIR, il):
	il.io.Print('i', "Creating database...")
	yaml = YAML()
	yaml.indent(mapping=2, sequence=4, offset=2)

	db = {"items": []}

	tools = Path(TOOL_DIR)
	if tools.exists():
		for cfg_path in tools.rglob("config.yaml"):
			try:
				tool_dir = cfg_path.parent
				category = tool_dir.parent
				cfg = readConfig(cfg_path)

				name = str(cfg.get("name", tool_dir.name)).lower()

				db["items"].append({
				    "name": name,
				    "kind": str(cfg.get("kind", "tool")).lower(),
				    "category": str(cfg.get("type", category.name)).lower(),
				    "desc": str(cfg.get("description", "")),
				    "tags": sorted(set(safe_list(cfg.get("tags", [])) + re.findall(r"[a-zA-Z0-9_\-]+", str(cfg).lower()))),
				    "action": f"use {name}"
				})
			except Exception:
				pass

	plugins = Path(PLUGIN_DIR)
	if plugins.exists():
		for plug_dir in plugins.iterdir():
			if not plug_dir.is_dir() or plug_dir.name.startswith("_"):
				continue

			cfg_path = plug_dir / "config.yaml"
			if not cfg_path.exists():
				continue

			try:
				cfg = readConfig(cfg_path)
				name = str(cfg.get("name", plug_dir.name)).lower()
				cve_id = cfg.get("cve", {}).get("id") if isinstance(cfg.get("cve"), dict) else ""
				source = cfg.get("source", {})
				source_text = source.get("nuclei_template", "") if isinstance(source, dict) else ""

				tags = safe_list(cfg.get("tags", []))
				if cve_id:
				    tags.append(str(cve_id).lower())
				if "nuclei" in source_text.lower():
				    tags.append("nuclei")

				hay = source_text
				try:
				    src_path = Path(source_text)
				    if src_path.exists():
				        hay += " " + src_path.read_text(errors="ignore")
				except Exception:
				    pass

				for word in re.split(r"[^a-zA-Z0-9]+", hay.lower()):
				    if len(word) > 2 and not word.isdigit() and word not in ("http", "https", "cves", "cve", "yaml", "nuclei", "templates", "ginsu", "home"):
				        tags.append(word)

				desc = str(cfg.get("description", ""))
				if cve_id and cve_id not in desc:
				    desc = f"{cve_id}: {desc}"

				db["items"].append({
				    "name": name,
				    "kind": str(cfg.get("kind", "plugin")).lower(),
				    "category": str(cfg.get("type", "plugin")).lower(),
				    "desc": desc,
				    "tags": sorted(set(tags)),
				    "action": f"use {name}"
				})
			except Exception:
				pass

	db_path = tools.parent / "resources/database.yaml"
	with open(db_path, "w") as f:
		yaml.dump(db, f)

	il.io.Print('s', "Database created.")
