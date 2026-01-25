diff --git a/governance/cpo/kit/scripts/validate_contracts.py b/governance/cpo/kit/scripts/validate_contracts.py
index 4f6a3c1..b91d8a2 100644
--- a/governance/cpo/kit/scripts/validate_contracts.py
+++ b/governance/cpo/kit/scripts/validate_contracts.py
@@ -1,12 +1,40 @@
 import json
 import sys
 from pathlib import Path
-import jsonschema
+from jsonschema import Draft202012Validator, RefResolver
 
 ROOT = Path(__file__).resolve().parents[1]
 
 def load_json(p: Path):
     return json.loads(p.read_text(encoding="utf-8"))
 
+def load_schema_store(schema_root: Path):
+    """
+    Load all schemas under schema_root into a resolver store keyed by $id.
+    This is required for cross-file $ref resolution.
+    """
+    store = {}
+    for path in schema_root.rglob("*.schema.json"):
+        schema = load_json(path)
+        schema_id = schema.get("$id")
+        if not schema_id:
+            raise RuntimeError(f"Schema missing $id: {path}")
+        store[schema_id] = schema
+    return store
+
 def validate(schema_path: Path, instance_path: Path):
-    schema = load_json(schema_path)
-    instance = load_json(instance_path)
-    jsonschema.validate(instance=instance, schema=schema)
+    schema = load_json(schema_path)
+    instance = load_json(instance_path)
+
+    schema_root = ROOT / "schemas" / "cpo-contracts@0.1.0"
+    store = load_schema_store(schema_root)
+
+    resolver = RefResolver.from_schema(schema, store=store)
+    validator = Draft202012Validator(schema, resolver=resolver)
+    validator.validate(instance)
 
 def main():
     cpo = ROOT / "schemas" / "cpo-contracts@0.1.0"
