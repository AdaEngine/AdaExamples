"""Asset-level regression checks for the portable garden; runtime checks run in Studio."""
import json
from pathlib import Path
import struct
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_glb(path):
    data = path.read_bytes()
    magic, version, length = struct.unpack_from('<III', data)
    assert (magic, version, length) == (0x46546c67, 2, len(data))
    json_length = struct.unpack_from('<I', data, 12)[0]
    document = json.loads(data[20:20+json_length])
    offset = 20+json_length
    binary_length, kind = struct.unpack_from('<II', data, offset)
    assert kind == 0x004e4942
    binary = data[offset+8:offset+8+binary_length]
    def accessor(index):
        info = document['accessors'][index]
        view = document['bufferViews'][info['bufferView']]
        count = {'SCALAR':1,'VEC2':2,'VEC3':3,'VEC4':4}[info['type']]
        fmt = '<' + {5126:'f',5125:'I',5123:'H'}[info['componentType']]*count
        start = view.get('byteOffset',0)+info.get('byteOffset',0)
        step = struct.calcsize(fmt)
        return [struct.unpack_from(fmt,binary,start+i*step) for i in range(info['count'])]
    primitive = document['meshes'][0]['primitives'][0]
    positions = accessor(primitive['attributes']['POSITION'])
    indices = [i[0] for i in accessor(primitive['indices'])]
    return positions, indices


class PortableGardenAssets(unittest.TestCase):
    def setUp(self):
        self.scene = yaml.safe_load((ROOT/'Assets/Scenes/Main.ascn').read_text())

    def test_project_is_portable_and_all_model_references_exist(self):
        project = json.loads((ROOT/'.ada/project.json').read_text())
        self.assertEqual(project['build']['system'],'adascript')
        self.assertFalse(list(ROOT.rglob('*.swift')))
        self.assertEqual(project['runtime']['entry']['scene'],'Assets/Scenes/Main.ascn')
        ids = [e['id'] for e in self.scene['entities']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(ids),539)
        for item in self.scene['entities']:
            source = item['components'].get('AdaScene.Model3DSource')
            if source:
                refs = [source['source']]+source.get('lod',{}).get('sources',[])
                for ref in refs:
                    self.assertTrue(ref.startswith('@res://'))
                    self.assertTrue((ROOT/'Assets'/ref[7:]).is_file(),ref)
        actions = {a['name']:a['bindings'] for a in project['inputActions']}
        self.assertEqual(actions['Run'],[{'key':{'_0':'shift'}}])
        self.assertEqual(actions['Orbit'],[{'mouseButton':{'_0':1}}])

    def test_landscape_counts_and_collider_geometry(self):
        names = [e['name'] for e in self.scene['entities']]
        self.assertEqual(names.count('Tree'),65)
        self.assertEqual(names.count('Rock'),42)
        self.assertEqual(names.count('Grass'),193)
        terrain = next(e for e in self.scene['entities'] if e['name']=='Rolling landscape')
        mesh = terrain['components']['AdaPhysics.PhysicsBody3DComponent']['shapes'][0]['fixture']['triangleMesh']['_0'].copy()
        mesh['vertices'] = [[float(v[a]) for a in ('x','y','z')] for v in mesh['vertices']]
        self.assertEqual(len(mesh['vertices']),65*65)
        self.assertEqual(len(mesh['indices']),8192*3)
        self.assertGreater(max(p[1] for p in mesh['vertices']),3)
        self.assertLess(min(p[1] for p in mesh['vertices']),-.5)
        for i in range(0,len(mesh['indices']),3):
            a,b,c = [mesh['vertices'][j] for j in mesh['indices'][i:i+3]]
            # Positive Y winding produces a solid walkable surface.
            self.assertGreater((b[2]-a[2])*(c[0]-a[0])-(b[0]-a[0])*(c[2]-a[2]),0)

    def test_chunk_lods_share_boundaries_and_match_collision_surface(self):
        terrain = next(e for e in self.scene['entities'] if e['name']=='Rolling landscape')
        points = terrain['components']['AdaPhysics.PhysicsBody3DComponent']['shapes'][0]['fixture']['triangleMesh']['_0']['vertices']
        heights = {(round(float(p['x']),5),round(float(p['z']),5)):float(p['y']) for p in points}
        for item in self.scene['entities']:
            if not item['name'].startswith('Terrain '): continue
            source = item['components']['AdaScene.Model3DSource']
            levels = [read_glb(ROOT/'Assets'/s[7:]) for s in [source['source']]+source['lod']['sources']]
            x0,x1=min(p[0] for p in levels[0][0]),max(p[0] for p in levels[0][0])
            z0,z1=min(p[2] for p in levels[0][0]),max(p[2] for p in levels[0][0])
            boundaries=[]
            for vertices,indices in levels:
                self.assertTrue(all(i<len(vertices) for i in indices))
                boundaries.append({p for p in vertices if p[0] in (x0,x1) or p[2] in (z0,z1)})
                for x,y,z in vertices: self.assertAlmostEqual(y,heights[(round(x,5),round(z,5))],places=5)
            self.assertEqual(boundaries[0],boundaries[1])
            self.assertEqual(boundaries[1],boundaries[2])
            self.assertGreater(len(levels[0][1]),len(levels[1][1]))
            self.assertGreater(len(levels[1][1]),len(levels[2][1]))


if __name__ == '__main__': unittest.main()
