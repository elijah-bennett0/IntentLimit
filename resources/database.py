# -*- coding: utf-8 -*-
"""
MIT License

Copyright (c) 2023 Elijah Bennett (Ginsu)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@Description		: Creates initial search index at startup
@Author			: Ginsu
@Date			: 20260130
"""

### Imports
from pathlib import Path
from ruamel.yaml import YAML
from integrityCheck import readConfig
###

__all__ = []

# Name the main function the same name as the file
### Code:
def createDB(TOOL_DIR, PLUGIN_DIR):
	'''
1. check if index.yaml exists in /resources
2. if not, create it

Format:

items:

    - name: item name
      kind: touch or exploit or tool etc
      desc: ...
      tags: [..,..,..]
      action: "use tool"
	'''
	yaml = YAML()
	yaml.indent(mapping=2, sequence=4, offset=2)

	db = {

		"items": []

	}

	tools = Path(TOOL_DIR) # probably make a combined tool/plugin dir to iterate and index both
	for category in tools.iterdir():
		for tool_dir in category.iterdir():
			if not tool_dir.is_dir():
				continue

			cfg_path = tool_dir / "config.yaml"
			cfg = readConfig(cfg_path)
			db["items"].append({
				"name": cfg["name"].lower(),
				"kind": cfg["kind"].lower(),
				"category": cfg["type"].lower(),
				"desc": cfg["description"],
				"tags": cfg["tags"],
				"action": f"use {cfg['name'].lower()}"
			})

	db_path = tools.parent / "resources/database.yaml"
	with open(db_path, 'w') as f:
		yaml.dump(db, f)

###

if __name__ == "__main__":
	createDB()
