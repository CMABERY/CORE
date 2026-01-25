import json, sys, zipfile
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]
EP_SCHEMAS = ROOT / "schemas" / "evidence-pack@1.0.0"

def load_json_bytes(b: bytes):
    return json.loads(b.decode("utf-8"))

def load_json_file(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def validate_manifest(obj):
    schema = load_json_file(EP_SCHEMAS/"manifest.schema.json")
    jsonschema.validate(obj, schema)

def validate_diff_summary(obj):
    schema = load_json_file(EP_SCHEMAS/"diff_summary.schema.json")
    jsonschema.validate(obj, schema)

def main():
    if len(sys.argv) != 2:
        print("usage: python validate_evidence_pack.py <pack_dir>", file=sys.stderr)
        return 2
    pack = Path(sys.argv[1])
    manifest = load_json_file(pack/"manifest.json")
    validate_manifest(manifest)
    diff = load_json_file(pack/"diff"/"diff_summary.json")
    validate_diff_summary(diff)
    print("OK: evidence pack schema validation passed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
