import json
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver

ROOT = Path(__file__).resolve().parents[1]

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def load_schema_store(schema_root: Path):
    """
    Load all schemas under schema_root into a resolver store keyed by $id.
    Required for cross-file $ref resolution.
    """
    store = {}
    for path in schema_root.rglob("*.schema.json"):
        schema = load_json(path)
        schema_id = schema.get("$id")
        if not schema_id:
            raise RuntimeError(f"Schema missing $id: {path}")
        store[schema_id] = schema
    return store

def validate(schema_path: Path, instance_path: Path):
    schema = load_json(schema_path)
    instance = load_json(instance_path)

    schema_root = ROOT / "schemas" / "cpo-contracts@0.1.0"
    store = load_schema_store(schema_root)

    resolver = RefResolver.from_schema(schema, store=store)
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
