# -*- coding: utf-8 -*-
"""Shared CVE module runner for exploitation tools."""

import importlib.util
from pathlib import Path

import yaml


def _handler(ctx):
	return getattr(ctx, "handler", None) or getattr(ctx, "io", None)


def normalize_cve(name):
	value = str(name or "").strip().lower().replace("-", "_")
	if value.startswith("cve_"):
		return value
	if value.startswith("cve"):
		return "cve_" + value[3:].lstrip("_")
	return value


def get_selected_cve(ctx):
	exploit = ctx.options.get("exploit")
	return normalize_cve(exploit)


def cve_dir(exploits_dir, cve_name):
	return Path(exploits_dir) / normalize_cve(cve_name)


def valid_cves(exploits_dir):
	base = Path(exploits_dir)
	if not base.exists():
		return []
	return sorted(path.name for path in base.iterdir() if path.is_dir() and path.name.startswith("cve_"))


def load_cve_module(exploits_dir, cve_name):
	name = normalize_cve(cve_name)
	module_path = cve_dir(exploits_dir, name) / f"{name}.py"
	if not module_path.exists():
		return None

	spec = importlib.util.spec_from_file_location(name, module_path)
	if spec is None or spec.loader is None:
		return None

	module = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(module)
	return module


def load_cve_config(exploits_dir, cve_name):
	config_path = cve_dir(exploits_dir, cve_name) / "config.yaml"
	if not config_path.exists():
		return {}

	with config_path.open("r", encoding="utf-8") as config_file:
		return yaml.safe_load(config_file) or {}


def command_spec(config, command):
	commands = config.get("commands", {})
	if not isinstance(commands, dict):
		return {}

	spec = commands.get(command, {})
	return spec if isinstance(spec, dict) else {}


def command_params(config, command):
	spec = command_spec(config, command)
	params = spec.get("params", {})
	return params if isinstance(params, dict) else {}


def command_enabled(config, command):
	spec = command_spec(config, command)
	if "enabled" not in spec:
		return True
	return bool(spec.get("enabled"))


def build_params(ctx, config=None, command=None):
	params = dict(getattr(ctx, "options", {}))

	if config and command:
		for name, spec in command_params(config, command).items():
			if not isinstance(spec, dict):
				continue
			if name not in params and "default" in spec:
				default = spec.get("default")
				if default is not None:
					params[name] = default

		if command == "exploit":
			for name, value in (config.get("exploit_params") or {}).items():
				params.setdefault(name, value)

	params.setdefault("target", "")
	params.setdefault("port", "443")
	params.setdefault("ssl", "true")
	params.setdefault("path", "")
	return params


def validate_params(handler, params, config, command):
	missing = []
	for name, spec in command_params(config, command).items():
		if not isinstance(spec, dict) or not spec.get("required"):
			continue
		value = params.get(name)
		if value is None or str(value).strip() in ("", "None"):
			missing.append(name)

	if missing:
		handler.Print("f", f"Missing required {command} parameter(s): {', '.join(missing)}")
		return False

	return True


def require_cve(ctx, exploits_dir):
	handler = _handler(ctx)
	cve_name = get_selected_cve(ctx)
	if not cve_name:
		handler.Print("f", "Missing exploit. Use: set exploit cve_YYYY_NNNN")
		return None, None, None

	config = load_cve_config(exploits_dir, cve_name)
	module = load_cve_module(exploits_dir, cve_name)
	if module is None:
		handler.Print("f", f"Unknown CVE for this tool: {cve_name}")
		handler.Print("i", "Use `list` to show CVEs available in this tool.")
		return None, None, None

	return cve_name, module, config


def list_cves(ctx, exploits_dir):
	handler = _handler(ctx)
	cves = valid_cves(exploits_dir)
	if not cves:
		handler.Print("w", "No CVE exploit folders found.")
		return

	for name in cves:
		handler.Print("i", name)


def scan_cve(ctx, exploits_dir):
	handler = _handler(ctx)
	cve_name, module, config = require_cve(ctx, exploits_dir)
	if module is None:
		return

	scan_func_name = command_spec(config, "scan").get("function", cve_name)
	scan_func = getattr(module, scan_func_name, None)
	if scan_func is None:
		handler.Print("f", f"{cve_name} does not expose scan function {scan_func_name}.")
		return

	params = build_params(ctx, config, "scan")
	if not validate_params(handler, params, config, "scan"):
		return

	scan_func(handler, params)


def exploit_cve(ctx, exploits_dir):
	handler = _handler(ctx)
	cve_name, module, config = require_cve(ctx, exploits_dir)
	if module is None:
		return

	if not command_enabled(config, "exploit"):
		handler.Print("w", f"Exploit disabled for {cve_name}.")
		return

	exploit_func_name = command_spec(config, "exploit").get("function", "exploit")
	exploit_func = getattr(module, exploit_func_name, None)
	if exploit_func is None:
		handler.Print("f", f"Selected CVE does not expose exploit function {exploit_func_name}.")
		return

	params = build_params(ctx, config, "exploit")
	if not validate_params(handler, params, config, "exploit"):
		return

	exploit_func(handler, params)
