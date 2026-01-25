import json
from pathlib import Path
from urllib.parse import urljoin

from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_NS = "urn:cpo-contracts@0.1.0/"

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def normalize_refs(obj):
    """
    Recursively rewrite $ref values to absolute URIs
    under SCHEMA_NS.
    """
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref = obj["$ref"]
            if not ref.startswith(SCHEMA_NS):
                obj["$ref"] = urljoin(SCHEMA_NS, ref)
        for v in obj.values():
            normalize_refs(v)
    elif isinstance(obj, list):
        for v in obj:
            normalize_refs(v)

def canonicalize_schema(schema, raw_id):
    canonical_id = urljoin(SCHEMA_NS, raw_id)
    schema["$id"] = canonical_id
    normalize_refs(schema)
    return canonical_id, schema

def load_schema_store(schema_root: Path):
    store = {}
    for path in schema_root.rglob("*.schema.json"):
        schema = load_json(path)
        raw_id = schema.get("$id")
        if not raw_id:
            raise RuntimeError(f"Schema missing $id: {path}")
        cid, normalized = canonicalize_schema(schema, raw_id)
        store[cid] = normalized
    return store

def validate(schema_path: Path, instance_path: Path):
    schema = load_json(schema_path)
    instance = load_json(instance_path)

    schema_root = ROOT / "schemas" / "cpo-contracts@0.1.0"
    store = load_schema_store(schema_root)

    raw_id = schema["$id"]
    root_id, schema = canonicalize_schema(schema, raw_id)

    resolver = RefResolver(base_uri=root_id, referrer=schema, store=store)
    validator = Draft202012Validator(schema, resolver=resolver)
    validator.validate(instance)

def main():
    cpo = ROOT / "schemas" / "cpo-contracts@0.1.0"
    examples = ROOT / "examples"

    pairs = [
        (cpo / "charter.schema.json", examples / "charter_v1_0_0.json"),
        (cpo / "state_snapshot.schema.json", examples / "state_snapshot.json"),
        (cpo / "decision.schema.json", examples / "decision_example.json"),
        (cpo / "exception.schema.json", examples / "exception_example.json"),
        (cpo / "drift_event.schema.json", examples / "drift_event_example.json"),
    ]

    for schema_path, instance_path in pairs:
        validate(schema_path, instance_path)
        print(f"OK: {instance_path.name} validates against {schema_path.name}")

    print("OK: CPO contract examples validate.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
