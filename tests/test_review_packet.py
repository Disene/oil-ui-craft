import hashlib
import json
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import zlib
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import review_packet as r

def png():
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data))
    return r.PNG+chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))+chunk(b'tEXt',b'Author\0expected-score-9')+chunk(b'IDAT',zlib.compress(b'\0\xff\xff\xff'))+chunk(b'IEND',b'')

class PacketTests(unittest.TestCase):
    def test_metadata_is_removed_not_image_data(self):
        data=r.clean_png(png());self.assertNotIn(b'expected-score',data);self.assertIn(b'IDAT',data)
        with self.assertRaises(ValueError):r.clean_png(png()+b'extra')
        with self.assertRaises(ValueError):r.clean_png(png()[:-2])

    def test_blinded_files_and_no_implicit_model_call(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);im=root/'author-favorite.png';im.write_bytes(png());out=root/'packet'
            m=r.prepare([im],'比较布局',out)
            text=(out/'reviewer'/'manifest.json').read_text();self.assertNotIn(im.name,text)
            report={'round':1,'review_type':'self','issues':[],'score':8}
            result=r.validate(out/'reviewer'/'manifest.json',report)
            self.assertEqual(result['independence'],'not_verified_by_tool')
            self.assertEqual(result['business_acceptance'],'not_performed')
            with self.assertRaises(ValueError):r.prepare([im],'task',out)

    def test_bad_evidence_round_and_tampering_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);im=root/'input.png';im.write_bytes(png());out=root/'packet';r.prepare([im],'task',out);m=out/'reviewer'/'manifest.json'
            base={'round':1,'review_type':'independent','issues':[{'severity':'major','finding':'overlap','evidence':['E01']}]}
            self.assertTrue(r.validate(m,base)['format_valid'])
            for change in ({'round':4},{'round':True},{'score':float('nan')},{'issues':[{'severity':'major','finding':'overlap','evidence':['invented']}]}):
                with self.assertRaises(ValueError):r.validate(m,{**base,**change})
            (out/'reviewer'/'E01.png').write_bytes(b'changed')
            with self.assertRaises(ValueError):r.validate(m,base)

if __name__=='__main__':unittest.main()
