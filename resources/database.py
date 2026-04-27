from pathlib import Path
from ruamel.yaml import YAML
from integrityCheck import readConfig
import re

__all__ = []

def safe_list(x):
    if not x:
        return []
    if isinstance(x, list):
        return [str(i).lower() for i in x]
    return [str(x).lower()]

def createDB(TOOL_DIR, PLUGIN_DIR):
    yaml = YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)

    db = {"items": []}

    # tools
    tools = Path(TOOL_DIR)
    if tools.exists():
        for category in tools.iterdir():
            if not category.is_dir():
                continue
            for tool_dir in category.iterdir():
                if not tool_dir.is_dir():
                    continue
                cfg_path = tool_dir / "config.yaml"
                if not cfg_path.exists():
                    continue
                try:
                    cfg = readConfig(cfg_path)
                    db["items"].append({
                        "name": str(cfg.get("name", tool_dir.name)).lower(),
                        "kind": str(cfg.get("kind", "tool")).lower(),
                        "category": str(cfg.get("type", category.name)).lower(),
                        "desc": str(cfg.get("description", "")),
                        "tags": safe_list(cfg.get("tags", [])),
                        "action": f"use {str(cfg.get('name', tool_dir.name)).lower()}"
                    })
                except Exception:
                    pass

    # plugins
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

                # derive searchable keywords from nuclei path + nuclei YAML content
                hay = source_text
                try:
                    src_path = Path(source_text)
                    if src_path.exists():
                        hay += " " + src_path.read_text(errors="ignore")
                except Exception:
                    pass

                for word in re.split(r"[^a-zA-Z0-9]+", hay.lower()):
                    if (
                        len(word) > 2
                        and not word.isdigit()
                        and word not in ("http", "https", "cves", "cve", "yaml", "nuclei", "templates", "ginsu", "home")
                    ):
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
