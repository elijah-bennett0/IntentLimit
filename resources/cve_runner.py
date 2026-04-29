# -*- coding: utf-8 -*-
"""Shared CVE module runner for exploitation tools."""

import importlib.util
from pathlib import Path


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


def build_params(ctx):
	params = dict(getattr(ctx, "options", {}))
	params.setdefault("target", "")
	params.setdefault("port", "443")
	params.setdefault("ssl", "true")
	params.setdefault("path", "")
	return params


def require_cve(ctx, exploits_dir):
	handler = _handler(ctx)
	cve_name = get_selected_cve(ctx)
	if not cve_name:
		handler.Print("f", "Missing exploit. Use: set exploit cve_YYYY_NNNN")
		return None, None

	module = load_cve_module(exploits_dir, cve_name)
	if module is None:
		handler.Print("f", f"Unknown CVE for this tool: {cve_name}")
		handler.Print("i", "Use `list` to show CVEs available in this tool.")
		return None, None

	return cve_name, module


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
	cve_name, module = require_cve(ctx, exploits_dir)
	if module is None:
		return

	scan_func = getattr(module, cve_name, None)
	if scan_func is None:
		handler.Print("f", f"{cve_name} does not expose a scan function.")
		return

	scan_func(handler, build_params(ctx))


def exploit_cve(ctx, exploits_dir):
	handler = _handler(ctx)
	_, module = require_cve(ctx, exploits_dir)
	if module is None:
		return

	exploit_func = getattr(module, "exploit", None)
	if exploit_func is None:
		handler.Print("f", "Selected CVE does not expose an exploit function.")
		return

	exploit_func(handler, build_params(ctx))
