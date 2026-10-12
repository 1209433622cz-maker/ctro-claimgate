#!/usr/bin/env python3
"""Validate the curated public CTRO ClaimGate package using the standard library."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "6_release/checksums/PUBLIC_REPOSITORY_MANIFEST.tsv"
PROHIBITED_SUFFIXES = {
    ".h5", ".h5ad", ".rds", ".rda", ".mtx", ".zip", ".tar", ".gz", ".docx", ".xlsx", ".pdf"
}
REQUIRED_GATES = {"C1", "C2", "C3", "C4", "C5", "C6"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def validate_manifest() -> None:
    if not MANIFEST.is_file():
        fail("public manifest is missing")
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {"relative_path", "bytes", "sha256"}
    if not rows or not required.issubset(rows[0]):
        fail("public manifest schema is invalid")
    declared = set()
    for row in rows:
        relative = row["relative_path"]
        if relative in declared or ".." in Path(relative).parts or Path(relative).is_absolute() or "\\" in relative:
            fail("unsafe or duplicate manifest path")
        path = ROOT / relative
        if not path.is_file():
            fail(f"manifest file is missing: {relative}")
        if path.stat().st_size != int(row["bytes"]):
            fail(f"byte count differs: {relative}")
        if sha256(path) != row["sha256"].lower():
            fail(f"sha256 differs: {relative}")
        declared.add(relative)
    actual = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and "__pycache__" not in path.parts
        and path.suffix.lower() not in {".pyc", ".pyo"}
        and path != MANIFEST
    }
    if actual != declared:
        fail(f"manifest membership differs: missing={sorted(actual-declared)}, extra={sorted(declared-actual)}")


def validate_gate_matrix() -> None:
    path = ROOT / "0_admin/gates/gate_matrix.tsv"
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if {row["gate_id"] for row in rows} != REQUIRED_GATES:
        fail("gate matrix must contain exactly C1-C6")
    if any(row["formal_execution_authorized"].lower() != "false" for row in rows):
        fail("formal execution is unexpectedly authorized")
    c6 = next(row for row in rows if row["gate_id"] == "C6")
    if c6["status"] != "PASS":
        fail("C6 traceability must remain PASS")


def validate_contract() -> None:
    path = ROOT / "1_data/contracts/eng04_author_input_contract.json"
    contract = json.loads(path.read_text(encoding="utf-8"))
    if contract.get("execution_authorized") is not False:
        fail("ENG04 execution must remain unauthorized")
    if contract.get("disease_effect_computation_authorized") is not False:
        fail("disease-effect computation must remain unauthorized")
    if contract.get("author_request_status") != "DRAFT_NOT_SENT":
        fail("public contract expects DRAFT_NOT_SENT author-request status")


def validate_public_file_types() -> None:
    offenders = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in PROHIBITED_SUFFIXES:
            offenders.append(path.relative_to(ROOT).as_posix())
    if offenders:
        fail(f"prohibited public file types: {offenders}")


def validate_submission_boundary() -> None:
    readme = (ROOT / "6_release/submission_preparation/README.md").read_text(encoding="utf-8")
    if "PREPARATION_HOLD_NOT_READY_FOR_JOURNAL_SUBMISSION" not in readme:
        fail("submission readiness boundary is missing")
    with (ROOT / "6_release/submission_preparation/SUBMISSION_READINESS_MATRIX.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or any(row["status"] in {"READY", "COMPLETE", "AUTHORIZED"} for row in rows):
        fail("submission matrix unexpectedly claims readiness")


def validate_v4_boundary() -> None:
    state = json.loads((ROOT / '0_admin/gates/v4_gate_status.json').read_text(encoding='utf-8'))
    expected = {'G0': 'PARTIAL', 'G1': 'HOLD', 'G2': 'HOLD', 'G3': 'HOLD', 'G4': 'LOCKED', 'C5': 'SEPARATE_HOLD'}
    if any(state.get(key) != value for key, value in expected.items()):
        fail('unapproved scientific-gate promotion')
    if any(state.get(key) is not False for key in ['formal_execution_authorized', 'primary_endpoint_computed', 'submission_authorized']):
        fail('unapproved formal execution, endpoint or submission')
    if any(state.get(key) != 0 for key in ['confirmed_external_people', 'packets_sent', 'external_opinions_received']):
        fail('external-review state changed without verified evidence')


def validate_eight_folder_layout() -> None:
    expected = {'0_admin','1_data','2_code','3_results','4_figures','5_manuscript','6_release','7.Report'}
    if any(not (ROOT / folder / 'README.md').is_file() for folder in expected):
        fail('required eight-folder structure or guide missing')
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if len(rel.parts) > 1 and rel.parts[0] not in expected:
            fail('payload outside the eight public collections: '+str(rel))
        if path.is_symlink():
            fail('public payload must not contain symlinks')


def validate_links_and_privacy() -> None:
    # Report filenames only, never matching credential strings or private content.
    sensitive = re.compile(r'\b[A-Z]:[\\/]|\b(?:ghp|github_pat)_[A-Za-z0-9_]{20,}|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bsk-[A-Za-z0-9_-]{20,}')
    for path in ROOT.rglob('*'):
        if not path.is_file() or '.git' in path.parts or '__pycache__' in path.parts or path.suffix == '.png':
            continue
        text = path.read_text(encoding='utf-8')
        if sensitive.search(text):
            fail('private absolute path or credential pattern: '+path.relative_to(ROOT).as_posix())
        if path.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)',text):
                if target.startswith(('http:','https:','mailto:','#')):
                    continue
                target=target.split('#',1)[0]
                if not (path.parent / target).resolve().exists():
                    fail('broken Markdown link in '+path.relative_to(ROOT).as_posix()+': '+target)


def validate_selected_figures() -> None:
    with (ROOT/'4_figures/PUBLIC_FIGURE_INDEX.tsv').open(encoding='utf-8',newline='') as handle:
        rows=list(csv.DictReader(handle,delimiter='\t'))
    if len(rows)!=8 or len({r['scientific_object'] for r in rows})!=4:
        fail('expected four scientific objects and eight PNG/SVG exports')
    for row in rows:
        p=ROOT/row['path']
        if p.stat().st_size!=int(row['bytes']) or sha256(p)!=row['sha256']:
            fail('selected figure identity mismatch')
        if p.suffix=='.png' and p.read_bytes()[:8]!=b'\x89PNG\r\n\x1a\n':
            fail('invalid selected PNG signature')
        if p.suffix=='.svg':
            tree=ET.parse(p)
            if any(x.tag.split('}')[-1] in {'script','foreignObject','image'} for x in tree.iter()):
                fail('unexpected executable/external SVG payload')
    with (ROOT/'3_results/figure_sources/H1_Frozen_Source_Coordinates.tsv').open(encoding='utf-8',newline='') as handle:
        coordinates=list(csv.DictReader(handle,delimiter='\t'))
    if len(coordinates)!=14 or any(sha256(ROOT/r['source_path'])!=r['source_sha256'] for r in coordinates):
        fail('H1 frozen summary source binding differs')


def validate_manuscript_boundary() -> None:
    main=(ROOT/'5_manuscript/author_review/CTRO_Stage67_Prospective_Design.md').read_text(encoding='utf-8')
    supplement=(ROOT/'5_manuscript/author_review/CTRO_Stage67_Supplementary_Design.md').read_text(encoding='utf-8')
    if any(t not in main for t in ['AUTHOR REVIEW','No formal probability sample','## References']):
        fail('prospective manuscript status missing')
    if '[[FIGURE:' in main+supplement or '[[EQUATION:' in main+supplement or '[[TABLE:' in main+supplement:
        fail('unresolved manuscript builder token')
    if len(re.findall(r'^\d+\. ',main.split('## References')[1],re.M))!=7:
        fail('seven-reference conservation differs')
    with (ROOT/'3_results/design_and_planning/Figure_S1_Planning_Source.tsv').open(encoding='utf-8',newline='') as handle:
        if len(list(csv.DictReader(handle,delimiter='\t')))!=51:
            fail('hypothetical source rows differ')


def main() -> None:
    validate_manifest()
    validate_gate_matrix()
    validate_contract()
    validate_public_file_types()
    validate_submission_boundary()
    validate_v4_boundary()
    validate_eight_folder_layout()
    validate_links_and_privacy()
    validate_selected_figures()
    validate_manuscript_boundary()
    print("PASS_PUBLIC_PACKAGE_CONTRACT")


if __name__ == "__main__":
    main()
