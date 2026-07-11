#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, tempfile, zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024), b''): h.update(c)
    return h.hexdigest()

p=argparse.ArgumentParser()
p.add_argument('archive', type=Path)
a=p.parse_args()
if not a.archive.is_file(): raise SystemExit('Archive not found')
with tempfile.TemporaryDirectory() as td:
    td=Path(td)
    with zipfile.ZipFile(a.archive) as z:
        bad=z.testzip()
        if bad: raise SystemExit(f'Corrupt ZIP member: {bad}')
        z.extractall(td)
    roots=[x for x in td.iterdir() if x.is_dir()]
    if len(roots)!=1: raise SystemExit(f'Expected exactly one package root, found {len(roots)}')
    root=roots[0]
    required=['README.md','RELEASE_NOTES.md','KNOWN_LIMITATIONS.md','VERSION','MANIFEST.json','checksums.sha256','02_Hardware/README.md','03_Software/README.md','04_Firmware/README.md','05_User_Interface/README.md']
    missing=[x for x in required if not (root/x).exists()]
    if missing: raise SystemExit('Missing: '+', '.join(missing))
    manifest=json.loads((root/'MANIFEST.json').read_text())
    expected={}
    for line in (root/'checksums.sha256').read_text().splitlines():
        digest, rel=line.split('  ',1); expected[rel]=digest
    failures=[]
    for rel,digest in expected.items():
        path=root/rel
        if not path.is_file() or sha256(path)!=digest: failures.append(rel)
    if failures: raise SystemExit('Checksum failures: '+', '.join(failures[:20]))
    print(f'PASS: {root.name}')
    print(f'Components: {len(manifest.get("components",[]))}')
    print(f'Files verified: {len(expected)}')
    print(f'Archive SHA256: {sha256(a.archive)}')
