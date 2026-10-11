"""Synthetic tests only. No source expression or saved scientific result is read."""
import hashlib,io,json,tempfile,unittest
from pathlib import Path
from safe_source_inspector import inspect_source, read_header_record, write_new_report, AuditError
class Guarded(io.BytesIO):
    def __init__(self,data):super().__init__(data);self.boundary=data.index(b'\n')+1
    def read(self,n=-1):
        if n<0 or self.tell()+n>self.boundary:raise AssertionError('attempted to read data row')
        return super().read(n)
class TestSafeSource(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)/'source';self.root.mkdir()
        self.data=b'gene_id\tc1\tc2\nGENE_SENTINEL\t0\t999\n';self.p=self.root/'counts.tsv';self.p.write_bytes(self.data)
        self.sha=hashlib.sha256(self.data).hexdigest()
    def tearDown(self):self.tmp.cleanup()
    def run_header(self,**kw):
        a=dict(mode='counts_header',expected_sha256=self.sha,expected_cells=['c1','c2'],role='author_expression_input');a.update(kw)
        return inspect_source(self.root,'counts.tsv',**a)
    def test_default_opaque(self):
        r=inspect_source(self.root,'counts.tsv');self.assertEqual(r['header_lines_decoded'],0);self.assertEqual(r['opaque_bytes_hashed'],len(self.data))
    def test_opaque_invalid_utf8(self):
        self.p.write_bytes(b'\xff\xfe');self.assertEqual(inspect_source(self.root,'counts.tsv')['source_data_rows_decoded'],0)
    def test_exact_first_line_guard(self):
        fields,n=read_header_record(Guarded(self.data),1024);self.assertEqual(fields,['gene_id','c1','c2']);self.assertEqual(n,self.data.index(b'\n')+1)
    def test_invalid_body_not_decoded(self):
        fields,_=read_header_record(Guarded(b'gene\tc1\n\xff\xfe\n'),100);self.assertEqual(fields,['gene','c1'])
    def test_missing_role(self):
        with self.assertRaises(AuditError):self.run_header(role=None)
    def test_missing_hash(self):
        with self.assertRaises(AuditError):self.run_header(expected_sha256=None)
    def test_bad_hash(self):
        with self.assertRaises(AuditError):self.run_header(expected_sha256='0'*64)
    def test_hash_format(self):
        with self.assertRaises(AuditError):self.run_header(expected_sha256='bad')
    def test_missing_metadata(self):
        with self.assertRaises(AuditError):self.run_header(expected_cells=None)
    def test_metadata_duplicates(self):
        with self.assertRaises(AuditError):self.run_header(expected_cells=['c1','c1'])
    def test_match(self):
        r=self.run_header();self.assertTrue(r['ordered_cells_match']);self.assertFalse(r['execution_authorized']);self.assertEqual(r['source_data_rows_decoded'],0)
    def test_reorder_not_automatic(self):
        r=self.run_header(expected_cells=['c2','c1']);self.assertFalse(r['ordered_cells_match']);self.assertTrue(r['cell_set_match'])
    def test_set_mismatch(self):
        r=self.run_header(expected_cells=['c1','c3']);self.assertFalse(r['cell_set_match'])
    def test_header_duplicate(self):
        with self.assertRaises(AuditError):read_header_record(io.BytesIO(b'g\tc1\tc1\n'),100)
    def test_empty_identifier(self):
        with self.assertRaises(AuditError):read_header_record(io.BytesIO(b'g\tc1\t\n'),100)
    def test_bom_crlf(self):
        f,_=read_header_record(Guarded(b'\xef\xbb\xbfg\tc1\r\nsecret'),100);self.assertEqual(f,['g','c1'])
    def test_no_lf(self):
        with self.assertRaises(AuditError):read_header_record(io.BytesIO(b'g\tc1'),100)
    def test_limit(self):
        with self.assertRaises(AuditError):read_header_record(io.BytesIO(b'g\tc1\nsecret'),4)
    def test_invalid_header_utf8(self):
        with self.assertRaises(AuditError):read_header_record(io.BytesIO(b'\xff\tc1\n'),100)
    def test_traversal(self):
        with self.assertRaises(AuditError):inspect_source(self.root,'../counts.tsv')
    def test_absolute(self):
        with self.assertRaises(AuditError):inspect_source(self.root,str(self.p))
    def test_backslash(self):
        with self.assertRaises(AuditError):inspect_source(self.root,'d\\counts.tsv')
    def test_symlink(self):
        (self.root/'alias.tsv').symlink_to(self.p)
        with self.assertRaises(AuditError):inspect_source(self.root,'alias.tsv')
    def test_result_path_block(self):
        d=self.root/'interactome_src';d.mkdir();(d/'counts.tsv').write_bytes(self.data)
        with self.assertRaises(AuditError):inspect_source(self.root,'interactome_src/counts.tsv',mode='counts_header',expected_sha256=self.sha,expected_cells=['c1','c2'],role='author_expression_input')
    def test_saved_result_name_block(self):
        (self.root/'pvalues.txt').write_bytes(self.data)
        with self.assertRaises(AuditError):inspect_source(self.root,'pvalues.txt',mode='counts_header',expected_sha256=self.sha,expected_cells=['c1','c2'],role='author_expression_input')
    def test_append_only(self):
        p=Path(self.tmp.name)/'report.json';r=inspect_source(self.root,'counts.tsv');write_new_report(p,r,self.root)
        with self.assertRaises(AuditError):write_new_report(p,r,self.root)
    def test_no_report_in_source(self):
        with self.assertRaises(AuditError):write_new_report(self.root/'report.json',{},self.root)
    def test_deterministic(self):self.assertEqual(self.run_header(),self.run_header())
if __name__=='__main__':unittest.main(verbosity=2)
