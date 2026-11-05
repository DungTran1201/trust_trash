from pathlib import Path

required = [
    Path("backend/src/trust_trash/bootstrap/app.py"),
    Path("backend/src/trust_trash/connector_sdk/base.py"),
    Path("backend/src/trust_trash/modules/discovery/domain/ports.py"),
    Path("apps/web/src/app/page.tsx"),
    Path("docs/architecture/overview.md"),
]
missing = [str(path) for path in required if not path.exists()]
if missing:
    raise SystemExit("Missing required starter files:\n" + "\n".join(missing))
print("Trust Trash starter structure: OK")
