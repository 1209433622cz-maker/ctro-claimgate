#!/usr/bin/env python3
"""CTRO Stage53: opaque hashing by default; explicit, bounded header-only parsing.

Never imports author code, opens an expression array, or parses a source data row.
Reading opaque bytes for SHA-256 is reported separately from decoding a header.
This tool is NOT a C5 adjudicator and never authorizes any scientific execution.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import os
import re
import stat
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Sequence

VERSION = 'stage53-safe-source-1.0.0'
HEX64 = re.compile(r'^[0-9a-fA-F]{64}$')
RESULT_NAMES = {'means.txt', 'pvalues.txt', 'significant_means.txt', 'deconvoluted.txt'}
RESULT_DIRS = {'interactome_src', 'interactome_res', 'subsampling_1000_cells'}

class AuditError(ValueError):
    """A failed prerequisite; do not fall back to broader reading."""

def safe_path(root: Path, relative: str) -> Path:
    if not relative or '\\' in relative or '\0' in relative or ':' in relative:
        raise AuditError('non-canonical relative path')
    rel = PurePosixPath(relative)
    if rel.is_absolute() or any(p in {'.', '..', ''} for p in relative.split('/')):
        raise AuditError('absolute, empty, dot or traversal component')
    root = root.resolve(strict=True)
    path = root.joinpath(*rel.parts)
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise AuditError('symlink component is not allowed')
    if not path.is_file():
        raise AuditError('target must be an existing regular file')
    if not path.resolve(strict=True).is_relative_to(root):
        raise AuditError('path escapes source root')
    return path

def read_header_record(stream: BinaryIO, limit: int) -> tuple[list[str], int]:
    """One byte at a time: never request a byte beyond the first LF.

    This is intentionally stricter than a buffered prefix read. It is for the
    bounded number of preflight headers, not high-throughput matrix ingestion.
    """
    if limit < 2:
        raise AuditError('header limit must be at least two bytes')
    data = bytearray()
    for _ in range(limit):
        b = stream.read(1)
        if not b:
            raise AuditError('header lacks a terminating LF; body not inspected')
        if len(b) != 1:
            raise AuditError('reader returned more bytes than requested')
        data.extend(b)
        if b == b'\n':
            break
    else:
        raise AuditError('header length limit reached; no body fallback')
    body = bytes(data[:-1])
    if body.endswith(b'\r'):
        body = body[:-1]
    if b'\r' in body or b'\0' in body:
        raise AuditError('control character in header')
    try:
        text = body.decode('utf-8-sig', errors='strict')
        fields = next(csv.reader([text], delimiter='\t', strict=True))
    except (UnicodeError, csv.Error, StopIteration) as e:
        raise AuditError('invalid UTF-8 or TSV header') from e
    if len(fields) < 2 or any(x == '' for x in fields[1:]):
        raise AuditError('no cell columns or an empty cell identifier')
    if len(set(fields[1:])) != len(fields[1:]):
        raise AuditError('duplicate cell columns')
    return fields, len(data)

def inspect_source(root: Path, relative: str, *, mode: str = 'opaque_hash',
                   expected_sha256: str | None = None,
                   expected_cells: Sequence[str] | None = None,
                   role: str | None = None, max_header_bytes: int = 16*1024*1024) -> dict:
    """Header mode requires explicit role, immutable hash and ordered cell list.

    The expected list may be a reconstructed metadata candidate. Agreement does
    not prove author-original identity, matrix scale, or runtime provenance.
    """
    if mode not in {'opaque_hash', 'counts_header'}:
        raise AuditError('unknown mode')
    if expected_sha256 is not None and not HEX64.fullmatch(expected_sha256):
        raise AuditError('expected SHA-256 must be 64 hexadecimal characters')
    path = safe_path(root, relative)
    if mode == 'counts_header':
        if role != 'author_expression_input':
            raise AuditError('explicit author_expression_input role required')
        if expected_sha256 is None or expected_cells is None:
            raise AuditError('immutable hash and ordered metadata cells required')
        if not expected_cells or any(not isinstance(x,str) or not x for x in expected_cells):
            raise AuditError('expected cells must be nonempty strings')
        if len(set(expected_cells)) != len(expected_cells):
            raise AuditError('duplicate cells in expected metadata')
        if path.suffix.lower() not in {'.tsv','.txt'} or path.name.lower() in RESULT_NAMES:
            raise AuditError('not an allowed expression-header file')
        if any(x.lower() in RESULT_DIRS for x in PurePosixPath(relative).parts):
            raise AuditError('saved-result locations cannot be header candidates')
    flags = os.O_RDONLY | getattr(os,'O_BINARY',0) | getattr(os,'O_NOFOLLOW',0)
    fd = os.open(path, flags)
    with os.fdopen(fd, 'rb', buffering=0) as handle:
        before = os.fstat(handle.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise AuditError('not a regular file descriptor')
        digest = hashlib.sha256(); hashed = 0
        for block in iter(lambda: handle.read(1024*1024), b''):
            digest.update(block); hashed += len(block)
        actual = digest.hexdigest()
        if expected_sha256 is not None and actual != expected_sha256.lower():
            raise AuditError('source hash mismatch')
        result = {'version':VERSION, 'relative_path':relative, 'mode':mode,
                  'status':'OPAQUE_IDENTITY_ONLY', 'sha256':actual,
                  'opaque_bytes_hashed':hashed, 'header_bytes_read':0,
                  'header_lines_decoded':0, 'source_data_rows_decoded':0,
                  'source_data_values_parsed':False, 'method_executed':False,
                  'execution_authorized':False, 'author_original_identity_proven':False}
        if mode == 'counts_header':
            handle.seek(0)
            fields, used = read_header_record(handle, max_header_bytes)
            observed = fields[1:]; expected = list(expected_cells)
            result.update({'status':('HEADER_IDENTITY_PASS_SCIENTIFIC_HOLD' if observed == expected else 'HEADER_IDENTITY_MISMATCH_HOLD'),
                           'header_identity_pass':observed == expected,
                           'header_bytes_read':used,'header_lines_decoded':1,
                           'cell_column_count':len(observed),
                           'ordered_cells_match':observed == expected,
                           'cell_set_match':set(observed) == set(expected),
                           'ordered_cell_list_sha256':hashlib.sha256(json.dumps(observed,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),
                           'expression_scale':'UNKNOWN_BODY_NOT_PARSED',
                           'no_reordering_performed':True})
        after = os.fstat(handle.fileno())
        if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns):
            raise AuditError('source changed during inspection')
        if hashed != before.st_size:
            raise AuditError('hashed-byte count does not match opened-file size')
    return result

def write_new_report(path: Path, result: dict, source_root: Path) -> None:
    path = path.absolute()
    if path.resolve().is_relative_to(source_root.resolve()):
        raise AuditError('report must not be inside immutable source root')
    if path.exists():
        raise AuditError('report exists; use a new stage/run path')
    path.parent.mkdir(parents=True,exist_ok=True)
    # x mode enforces append-only creation even if another writer races.
    with path.open('x',encoding='utf-8',newline='\n') as handle:
        json.dump(result,handle,ensure_ascii=False,sort_keys=True,indent=2);handle.write('\n')

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root',type=Path,required=True)
    ap.add_argument('--relative-path',required=True)
    ap.add_argument('--mode',choices=['opaque_hash','counts_header'],default='opaque_hash')
    ap.add_argument('--expected-sha256')
    ap.add_argument('--expected-cells-json',type=Path,help='JSON list from separately frozen metadata; no matrix rows')
    ap.add_argument('--role',choices=['author_expression_input'])
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    try:
        expected=None
        if args.expected_cells_json:
            expected=json.loads(args.expected_cells_json.read_text(encoding='utf-8-sig'))
            if not isinstance(expected,list):raise AuditError('expected-cells JSON must be a list')
        result=inspect_source(args.source_root,args.relative_path,mode=args.mode,
                              expected_sha256=args.expected_sha256,expected_cells=expected,role=args.role)
        write_new_report(args.output,result,args.source_root)
    except (AuditError,OSError,json.JSONDecodeError) as exc:
        print(json.dumps({'status':'BLOCKED','error':str(exc),'execution_authorized':False}));return 2
    print(json.dumps({'status':result['status'],'output':str(args.output),'execution_authorized':False}));return 2 if result.get('header_identity_pass') is False else 0

if __name__=='__main__':raise SystemExit(main())
