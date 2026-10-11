#!/usr/bin/env python3
"""Validate the curated public CTRO ClaimGate package using the standard library."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "checksums/PUBLIC_REPOSITORY_MANIFEST.tsv"
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
    path = ROOT / "workflow/gate_matrix.tsv"
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
    path = ROOT / "workflow/eng04_author_input_contract.json"
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
    readme = (ROOT / "submission/README.md").read_text(encoding="utf-8")
    if "PREPARATION_HOLD_NOT_READY_FOR_JOURNAL_SUBMISSION" not in readme:
        fail("submission readiness boundary is missing")
    with (ROOT / "submission/SUBMISSION_READINESS_MATRIX.tsv").open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or any(row["status"] in {"READY", "COMPLETE", "AUTHORIZED"} for row in rows):
        fail("submission matrix unexpectedly claims readiness")


def validate_v4_boundary() -> None:
    state = json.loads((ROOT / 'workflow/v4_gate_status.json').read_text(encoding='utf-8'))
    expected = {'G0': 'PARTIAL', 'G1': 'HOLD', 'G2': 'HOLD', 'G3': 'HOLD', 'G4': 'LOCKED', 'C5': 'SEPARATE_HOLD'}
    if any(state.get(key) != value for key, value in expected.items()):
        fail('unapproved scientific-gate promotion')
    if any(state.get(key) is not False for key in ['formal_execution_authorized', 'primary_endpoint_computed', 'submission_authorized']):
        fail('unapproved formal execution, endpoint or submission')
    if any(state.get(key) != 0 for key in ['confirmed_external_people', 'packets_sent', 'external_opinions_received']):
        fail('external-review state changed without verified evidence')


def main() -> None:
    validate_manifest()
    validate_gate_matrix()
    validate_contract()
    validate_public_file_types()
    validate_submission_boundary()
    validate_v4_boundary()
    print("PASS_PUBLIC_PACKAGE_CONTRACT")


if __name__ == "__main__":
    main()
