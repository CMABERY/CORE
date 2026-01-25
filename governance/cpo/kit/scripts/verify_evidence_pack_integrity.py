import json, sys, hashlib, zipfile
from pathlib import Path

# NOTE: For deterministic hashing of JSON structures, prefer RFC8785 JCS (see scripts/jcs.js).

def sha256_bytes(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()

def read_zip(zpath: Path):
    with zipfile.ZipFile(zpath, "r") as z:
        return {name: z.read(name) for name in z.namelist() if not name.endswith("/")}

def main():
    from pathlib import Path

# ... after parsing argv ...
zpath = Path(sys.argv[1])

if not zpath.exists():
    print(f"FAIL: pack path does not exist: {zpath}", file=sys.stderr)
    print("CWD:", Path.cwd(), file=sys.stderr)
    print("CWD contents:", list(Path.cwd().iterdir()), file=sys.stderr)
    raise SystemExit(1)

    if len(sys.argv) != 2:
        print("usage: python verify_evidence_pack_integrity.py <pack.zip>", file=sys.stderr)
        return 2
    zpath = Path(sys.argv[1])
    files = read_zip(zpath)
    # minimal verifier: ensure required files exist; if file_hashes populated, verify
    required = ["manifest.json","diff/diff_summary.json","integrity/file_hashes.json"]
    missing = [r for r in required if r not in files]
    if missing:
        print("FAIL: missing required files:", missing)
        return 1

    file_hashes = json.loads(files["integrity/file_hashes.json"].decode("utf-8"))
    entries = file_hashes.get("files", [])
    if not entries:
        print("WARN: integrity/file_hashes.json has no entries (placeholder).")
        print("OK: basic structure present.")
        return 0

    # verify listed hashes
    for e in entries:
        path = e["path"]
        expected = e["hash"]
        if path not in files:
            print(f"FAIL: listed path missing in zip: {path}")
            return 1
        got = sha256_bytes(files[path])
        if got != expected:
            print(f"FAIL: hash mismatch for {path}: got {got} expected {expected}")
            return 1

    print("OK: file hashes verify.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
