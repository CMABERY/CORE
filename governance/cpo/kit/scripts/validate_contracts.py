import json, sys
from pathlib import Path
import jsonschema

ROOT = Path(__file__).resolve().parents[1]

def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def validate(schema_path: Path, instance_path: Path):
    schema = load_json(schema_path)
    instance = load_json(instance_path)
    jsonschema.validate(instance=instance, schema=schema)

def main():
    cpo = ROOT / "schemas" / "cpo-contracts@0.1.0"
    examples = ROOT / "examples"
    pairs = [
        (cpo/"charter.schema.json", examples/"charter_v1_0_0.json"),
        (cpo/"state_snapshot.schema.json", examples/"state_snapshot.json"),
        (cpo/"decision.schema.json", examples/"decision_example.json"),
        (cpo/"exception.schema.json", examples/"exception_example.json"),
        (cpo/"drift_event.schema.json", examples/"drift_event_example.json"),
    ]
    for s,i in pairs:
        validate(s,i)
        print(f"OK: {i.name} validates against {s.name}")
    print("OK: contract examples validate.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
