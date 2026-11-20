import json
from pathlib import Path
from subprocess import run
import sys
import tempfile
import unittest

BASE = Path(__file__).resolve().parents[1]
SCRIPTS = BASE / 'skills/peta-alur-hidup/scripts'
DEMO = BASE / 'examples/pengajuan'

class SkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='flow map ')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'workflow.py').write_bytes((DEMO/'workflow.py').read_bytes())
        self.model = json.loads((DEMO/'model.json').read_text(encoding='utf-8'))
        self.output = self.root/'ALUR.md'

    def render(self, *flags):
        (self.root/'model.json').write_text(json.dumps(self.model), encoding='utf-8')
        return run([sys.executable,str(SCRIPTS/'render.py'),'model.json','--root','.', '--output','ALUR.md',*flags], cwd=self.root, capture_output=True, text=True)

    def test_generate_and_check(self):
        self.model['steps'][0]['tables'] = {'requests': 'create'}
        result = self.render()
        self.assertEqual(result.returncode,0,result.stderr)
        md = self.output.read_text(encoding='utf-8')
        for label in ['```mermaid', 'Ajukan','Setujui','Tolak','requests','workflow.py']:
            self.assertIn(label,md)
        self.assertEqual(self.render('--check').returncode,0)
        self.assertEqual(self.output.read_text(encoding='utf-8'),md)

    def test_stale_is_read_only(self):
        self.assertEqual(self.render().returncode,0)
        saved = self.output.read_bytes()
        self.model['title'] += ' berbeda'
        self.assertNotEqual(self.render('--check').returncode,0)
        self.assertEqual(self.output.read_bytes(),saved)

    def test_dangling_edge(self):
        self.model['edges'][0]['to']='Missing'
        self.assertNotEqual(self.render().returncode,0)
        self.assertFalse(self.output.exists())

    def test_bad_evidence(self):
        for ref in ['workflow.py:9999','../outside.py:1']:
            with self.subTest(ref=ref):
                self.model['steps'][0]['evidence']=ref
                self.assertNotEqual(self.render().returncode,0)
                self.assertFalse(self.output.exists())

    def test_protect_manual_document(self):
        self.output.write_text('Catatan saya',encoding='utf-8')
        self.assertNotEqual(self.render().returncode,0)
        self.assertEqual(self.output.read_text(encoding='utf-8'),'Catatan saya')

    def test_discover_excludes_hidden_and_vendor(self):
        for name in ['vendor','.hidden']:
            (self.root/name).mkdir()
            (self.root/name/'private.py').touch()
        (self.root/'pyproject.toml').touch()
        result = run([sys.executable,str(SCRIPTS/'discover.py'),str(self.root)],capture_output=True,text=True,check=True)
        facts = json.loads(result.stdout)
        self.assertEqual(facts['candidates'],['workflow.py'])
        self.assertEqual(facts['manifests'][0]['stack_hint'],'Python')
