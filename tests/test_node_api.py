''' Unit tests for humon.cy '''

#pylint: disable=missing-class-docstring, missing-function-docstring
#pylint: disable=too-many-public-methods, too-many-lines

from pathlib import Path
import unittest
import humon as h

def path_of(filename: str):
    return str(Path(__file__).parent / filename)

class Foo:
    pass

class NodeApiTestCase(unittest.TestCase):
    def setUp(self):
        self.value_only = h.from_string('dreams')
        self.list_only = h.from_string('[]')
        self.dict_only = h.from_string('{}')
        self.gnome = h.from_file(path_of('gnome.hu'))

class TestNodeKind(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.kind, h.NodeKind.VALUE)
        self.assertEqual(self.list_only.root.kind, h.NodeKind.LIST)
        self.assertEqual(self.dict_only.root.kind, h.NodeKind.DICT)
        self.assertEqual(self.gnome.root.kind, h.NodeKind.DICT)

class TestNodeParent(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.parent, None)
        self.assertEqual(self.list_only.root.parent, None)
        self.assertEqual(self.dict_only.root.parent, None)
        self.assertEqual(self.gnome.root.parent, None)

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/textures').parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/skeleton').parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/animations').parent, self.gnome.root)

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').parent.parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/textures/1').parent.parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/textures/2').parent.parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/animations/idle:0').parent.parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/animations/walk').parent.parent, self.gnome.root)
        self.assertEqual(self.gnome.get_node('/animations/idle:1').parent.parent, self.gnome.root)


class TestNodeNumChildren(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.num_children, 0)
        self.assertEqual(self.list_only.root.num_children, 0)
        self.assertEqual(self.dict_only.root.num_children, 0)
        self.assertEqual(self.gnome.root.num_children, 4)

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').num_children, 0)
        self.assertEqual(self.gnome.get_node('/textures').num_children, 3)
        self.assertEqual(self.gnome.get_node('/skeleton').num_children, 0)
        self.assertEqual(self.gnome.get_node('/animations').num_children, 3)

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').num_children, 0)
        self.assertEqual(self.gnome.get_node('/textures/1').num_children, 0)
        self.assertEqual(self.gnome.get_node('/textures/2').num_children, 0)
        self.assertEqual(self.gnome.get_node('/animations/idle:0').num_children, 2)
        self.assertEqual(self.gnome.get_node('/animations/walk').num_children, 2)
        self.assertEqual(self.gnome.get_node('/animations/idle:1').num_children, 2)


class TestNodeNodeIndex(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.node_index, 0)
        self.assertEqual(self.list_only.root.node_index, 0)
        self.assertEqual(self.dict_only.root.node_index, 0)
        self.assertEqual(self.gnome.root.node_index, 0)

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').node_index, 1)
        self.assertEqual(self.gnome.get_node('/textures').node_index, 2)
        self.assertEqual(self.gnome.get_node('/skeleton').node_index, 6)
        self.assertEqual(self.gnome.get_node('/animations').node_index, 7)

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').node_index, 3)
        self.assertEqual(self.gnome.get_node('/textures/1').node_index, 4)
        self.assertEqual(self.gnome.get_node('/textures/2').node_index, 5)
        self.assertEqual(self.gnome.get_node('/animations/idle:0').node_index, 8)
        self.assertEqual(self.gnome.get_node('/animations/walk').node_index, 13)
        self.assertEqual(self.gnome.get_node('/animations/idle:1').node_index, 18)

    def test_by_index(self):
        for i in range(self.gnome.num_nodes):
            self.assertEqual(self.gnome.get_node(i).node_index, i)

class TestNodeChildIndex(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.child_index, 0)
        self.assertEqual(self.list_only.root.child_index, 0)
        self.assertEqual(self.dict_only.root.child_index, 0)
        self.assertEqual(self.gnome.root.child_index, 0)

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').child_index, 0)
        self.assertEqual(self.gnome.get_node('/textures').child_index, 1)
        self.assertEqual(self.gnome.get_node('/skeleton').child_index, 2)
        self.assertEqual(self.gnome.get_node('/animations').child_index, 3)

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').child_index, 0)
        self.assertEqual(self.gnome.get_node('/textures/1').child_index, 1)
        self.assertEqual(self.gnome.get_node('/textures/2').child_index, 2)
        self.assertEqual(self.gnome.get_node('/animations/idle:0').child_index, 0)
        self.assertEqual(self.gnome.get_node('/animations/walk').child_index, 1)
        self.assertEqual(self.gnome.get_node('/animations/idle:1').child_index, 2)

class TestNodeGetItem(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root[0], None)
        self.assertEqual(self.value_only.root['foo'], None)
        self.assertEqual(self.list_only.root[0], None)
        self.assertEqual(self.list_only.root['foo'], None)
        self.assertEqual(self.dict_only.root[0], None)
        self.assertEqual(self.dict_only.root['foo'], None)
        self.assertEqual(self.gnome.root[0], self.gnome.get_node(1))
        self.assertEqual(self.gnome.root['model'], self.gnome.get_node(1))
        self.assertEqual(self.gnome.root[1], self.gnome.get_node(2))
        self.assertEqual(self.gnome.root['textures'], self.gnome.get_node(2))
        self.assertEqual(self.gnome.root[2], self.gnome.get_node(6))
        self.assertEqual(self.gnome.root['skeleton'], self.gnome.get_node(6))
        self.assertEqual(self.gnome.root[3], self.gnome.get_node(7))
        self.assertEqual(self.gnome.root['animations'], self.gnome.get_node(7))

    def test_d2(self):
        self.assertEqual(self.gnome.root[0][0], None)
        self.assertEqual(self.gnome.root['model'][0], None)
        self.assertEqual(self.gnome.root[1][0], self.gnome.get_node(3))
        self.assertEqual(self.gnome.root['textures'][0], self.gnome.get_node(3))
        self.assertEqual(self.gnome.root['textures']['foo'], None)
        self.assertEqual(self.gnome.root[2][0], None)
        self.assertEqual(self.gnome.root[2]['foo'], None)
        self.assertEqual(self.gnome.root['skeleton'][0], None)
        self.assertEqual(self.gnome.root['skeleton']['foo'], None)
        self.assertEqual(self.gnome.root[3][0], self.gnome.get_node(8))
        self.assertEqual(self.gnome.root[3][0], self.gnome.get_node(8))
        self.assertEqual(self.gnome.root['animations'][0], self.gnome.get_node(8))
        self.assertEqual(self.gnome.root['animations'][1], self.gnome.get_node(13))
        self.assertEqual(self.gnome.root['animations'][2], self.gnome.get_node(18))

    def test_d3(self):
        at = self.gnome.get_node('/textures')
        an = self.gnome.get_node('/animations')
        self.assertEqual(at[0].value, 'gnome-generic-albedo.png')
        self.assertEqual(at[1].value, 'gnome-generic-bump.png')
        self.assertEqual(at[2].value, 'gnome-generic-metallic.png')
        self.assertEqual(an['idle', 0]['animation'].value, 'gnome-idle_0.anim')
        self.assertEqual(an['idle', 1]['animation'].value, 'gnome-idle_1.anim')
        self.assertEqual(an['idle']['animation'].value, 'gnome-idle_1.anim')

class TestNodeGetNode(NodeApiTestCase):
    def test_idx_root(self):
        self.assertEqual(self.value_only.root.get_node(0), None)
        self.assertEqual(self.list_only.root.get_node(0), None)
        self.assertEqual(self.dict_only.root.get_node(0), None)
        self.assertEqual(self.gnome.root.get_node(0), self.gnome.root[0])
        self.assertEqual(self.gnome.root.get_node(1), self.gnome.root[1])
        self.assertEqual(self.gnome.root.get_node(2), self.gnome.root[2])
        self.assertEqual(self.gnome.root.get_node(3), self.gnome.root[3])

    def test_idx_d2(self):
        self.assertEqual(self.gnome.root.get_node(0).get_node(0), None)
        self.assertEqual(self.gnome.root.get_node(1).get_node(0), self.gnome.get_node(3))
        self.assertEqual(self.gnome.root.get_node(2).get_node(0), None)
        self.assertEqual(self.gnome.root.get_node(3).get_node(0), self.gnome.get_node(8))
        self.assertEqual(self.gnome.root.get_node(3).get_node(0), self.gnome.get_node(8))
        self.assertEqual(self.gnome.root.get_node(3).get_node(1), self.gnome.get_node(13))
        self.assertEqual(self.gnome.root.get_node(3).get_node(2), self.gnome.get_node(18))

    def test_mixed_d3(self):
        at = self.gnome.get_node('/textures')
        an = self.gnome.get_node('/animations')
        self.assertEqual(at.get_node(0).value, 'gnome-generic-albedo.png')
        self.assertEqual(at.get_node(1).value, 'gnome-generic-bump.png')
        self.assertEqual(at.get_node(2).value, 'gnome-generic-metallic.png')
        self.assertEqual(an.get_node('idle:0').get_node('animation').value, 'gnome-idle_0.anim')
        self.assertEqual(an.get_node('idle:1').get_node('animation').value, 'gnome-idle_1.anim')
        self.assertEqual(an.get_node('idle').get_node('animation').value, 'gnome-idle_1.anim')

    def test_backpath(self):
        self.assertEqual(self.gnome.root.get_node(
            'textures/0/../../model/../animations/idle:1/audio/1').value, 'gnome-scratch.ogg')

    def test_wrong(self):
        at = self.gnome.get_node('/textures')
        an = self.gnome.get_node('/animations')
        self.assertEqual(at.get_node(3), None)
        self.assertEqual(at.get_node('foo'), None)
        self.assertEqual(an.get_node(3), None)
        self.assertEqual(an.get_node('foo'), None)
        self.assertEqual(self.gnome.root.get_node('..'), None)

    def test_pathological(self):
        with self.assertRaises(TypeError):
            self.value_only.root.get_node(Foo())
        with self.assertRaises(TypeError):
            self.list_only.root.get_node(Foo())
        with self.assertRaises(TypeError):
            self.dict_only.root.get_node(Foo())
        with self.assertRaises(TypeError):
            self.gnome.root.get_node(Foo())
        self.assertEqual(self.gnome.root.get_node(''), self.gnome.root)
        self.assertEqual(self.gnome.root.get_node(-1), None)
        with self.assertRaises(TypeError):
            self.gnome.root.get_node(1.5)
        self.assertEqual(self.gnome.root.get_node(1000000000000000), None)

class TestNodeAddress(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.address, '/')
        self.assertEqual(self.list_only.root.address, '/')
        self.assertEqual(self.dict_only.root.address, '/')
        self.assertEqual(self.gnome.root.address, '/')

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').address, '/model')
        self.assertEqual(self.gnome.get_node('/textures').address, '/textures')
        self.assertEqual(self.gnome.get_node('/skeleton').address, '/skeleton')
        self.assertEqual(self.gnome.get_node('/animations').address, '/animations')

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').address, '/textures/0')
        self.assertEqual(self.gnome.get_node('/textures/1').address, '/textures/1')
        self.assertEqual(self.gnome.get_node('/textures/2').address, '/textures/2')
        self.assertEqual(self.gnome.get_node('/animations/idle:0').address, '/animations/idle:0')
        self.assertEqual(self.gnome.get_node('/animations/walk').address, '/animations/walk')
        self.assertEqual(self.gnome.get_node('/animations/idle:1').address, '/animations/idle:1')

class TestNodeGetSibling(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.get_sibling(), None)
        self.assertEqual(self.value_only.root.get_sibling('foo'), None)
        self.assertEqual(self.list_only.root.get_sibling(), None)
        self.assertEqual(self.list_only.root.get_sibling('foo'), None)
        self.assertEqual(self.dict_only.root.get_sibling(), None)
        self.assertEqual(self.dict_only.root.get_sibling('foo'), None)
        self.assertEqual(self.gnome.root.get_sibling(), None)
        self.assertEqual(self.gnome.root.get_sibling('foo'), None)

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').get_sibling().address, '/textures')
        self.assertEqual(self.gnome.get_node('/model').get_sibling('textures').address, '/textures')
        self.assertEqual(self.gnome.get_node('/model').get_sibling('skeleton').address, '/skeleton')
        self.assertEqual(self.gnome.get_node('/textures').get_sibling().address,
                         '/skeleton')
        self.assertEqual(self.gnome.get_node('/textures').get_sibling('skeleton').address,
                         '/skeleton')
        self.assertEqual(self.gnome.get_node('/skeleton').get_sibling().address,
                         '/animations')
        self.assertEqual(self.gnome.get_node('/skeleton').get_sibling('animations').address,
                         '/animations')

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').get_sibling().address, '/textures/1')
        self.assertEqual(self.gnome.get_node('/textures/1').get_sibling().address, '/textures/2')
        self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling().address,
                         '/animations/walk')
        self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling('walk').address,
                         '/animations/walk')
        self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling('idle').address,
                         '/animations/idle:1')
        self.assertEqual(self.gnome.get_node('/animations/walk').get_sibling().address,
                         '/animations/idle:1')
        self.assertEqual(self.gnome.get_node('/animations/walk').get_sibling('idle').address,
                         '/animations/idle:1')
        self.assertEqual(self.gnome.get_node('/animations/idle:1').get_sibling(), None)

    def test_wrong(self):
        self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling('trot'), None)

    def test_pathological(self):
        with self.assertRaises(TypeError):
            self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling(0), None)
        with self.assertRaises(TypeError):
            self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling(-1), None)
        with self.assertRaises(TypeError):
            self.assertEqual(self.gnome.get_node('/animations/idle:0').get_sibling(Foo()), None)

class TestNodeKey(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.key, None)
        self.assertEqual(self.list_only.root.key, None)
        self.assertEqual(self.dict_only.root.key, None)
        self.assertEqual(self.gnome.root.key, None)

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').key, 'model')
        self.assertEqual(self.gnome.get_node('/textures').key, 'textures')
        self.assertEqual(self.gnome.get_node('/skeleton').key, 'skeleton')
        self.assertEqual(self.gnome.get_node('/animations').key, 'animations')

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').key, None)
        self.assertEqual(self.gnome.get_node('/textures/1').key, None)
        self.assertEqual(self.gnome.get_node('/textures/2').key, None)
        self.assertEqual(self.gnome.get_node('/animations/idle:0').key, 'idle')
        self.assertEqual(self.gnome.get_node('/animations/walk').key, 'walk')
        self.assertEqual(self.gnome.get_node('/animations/idle:1').key, 'idle')

class TestNodeValue(NodeApiTestCase):
    def test_root(self):
        self.assertEqual(self.value_only.root.value, 'dreams')
        self.assertEqual(self.list_only.root.value, '[')
        self.assertEqual(self.dict_only.root.value, '{')
        self.assertEqual(self.gnome.root.value, '{')

    def test_d2(self):
        self.assertEqual(self.gnome.get_node('/model').value, 'gnome-generic.mesh')
        self.assertEqual(self.gnome.get_node('/textures').value, '[')
        self.assertEqual(self.gnome.get_node('/skeleton').value, 'gnome-generic-bones.skel')
        self.assertEqual(self.gnome.get_node('/animations').value, '{')

    def test_d3(self):
        self.assertEqual(self.gnome.get_node('/textures/0').value, 'gnome-generic-albedo.png')
        self.assertEqual(self.gnome.get_node('/textures/1').value, 'gnome-generic-bump.png')
        self.assertEqual(self.gnome.get_node('/textures/2').value, 'gnome-generic-metallic.png')
        self.assertEqual(self.gnome.get_node('/animations/idle:0').value, '{')
        self.assertEqual(self.gnome.get_node('/animations/walk').value, '{')
        self.assertEqual(self.gnome.get_node('/animations/idle:1').value, '{')

class TestNodeSourceText(NodeApiTestCase):
    def test_root(self):
        root = '''{
    model: gnome-generic.mesh
    textures: [
        gnome-generic-albedo.png
        gnome-generic-bump.png          @ units: model-space
        gnome-generic-metallic.png
    ]
    skeleton: gnome-generic-bones.skel
    animations: {
        idle: {
            animation: gnome-idle_0.anim
            audio: [
                gnome-sigh.ogg
                gnome-stretch.ogg
            ]
        }
        walk: {
            animation: gnome-walk_0-anim
            audo: [
                gnome-footfall-left-quiet.ogg
                gnome-footfall-right-quiet.ogg
            ]
        }
        idle: {
            animation: gnome-idle_1.anim
            audio: [
                gnome-idle-mumble.ogg
                gnome-scratch.ogg
            ]
        }
    }
}'''
        self.assertEqual(self.value_only.root.source_text, 'dreams')
        self.assertEqual(self.list_only.root.source_text, '[]')
        self.assertEqual(self.dict_only.root.source_text, '{}')
        self.assertEqual(self.gnome.root.source_text, root)

    def test_d2(self):
        textures = '''textures: [
        gnome-generic-albedo.png
        gnome-generic-bump.png          @ units: model-space
        gnome-generic-metallic.png
    ]'''
        animations = '''animations: {
        idle: {
            animation: gnome-idle_0.anim
            audio: [
                gnome-sigh.ogg
                gnome-stretch.ogg
            ]
        }
        walk: {
            animation: gnome-walk_0-anim
            audo: [
                gnome-footfall-left-quiet.ogg
                gnome-footfall-right-quiet.ogg
            ]
        }
        idle: {
            animation: gnome-idle_1.anim
            audio: [
                gnome-idle-mumble.ogg
                gnome-scratch.ogg
            ]
        }
    }'''
        self.assertEqual(self.gnome.get_node('/model').source_text, 'model: gnome-generic.mesh')
        self.assertEqual(self.gnome.get_node('/textures').source_text, textures)
        self.assertEqual(self.gnome.get_node('/skeleton').source_text,
                         'skeleton: gnome-generic-bones.skel')
        self.assertEqual(self.gnome.get_node('/animations').source_text, animations)

    def test_d3(self):
        idle_0 = '''idle: {
            animation: gnome-idle_0.anim
            audio: [
                gnome-sigh.ogg
                gnome-stretch.ogg
            ]
        }'''
        walk = '''walk: {
            animation: gnome-walk_0-anim
            audo: [
                gnome-footfall-left-quiet.ogg
                gnome-footfall-right-quiet.ogg
            ]
        }'''
        idle_1 = '''idle: {
            animation: gnome-idle_1.anim
            audio: [
                gnome-idle-mumble.ogg
                gnome-scratch.ogg
            ]
        }'''
        self.assertEqual(self.gnome.get_node('/textures/0').source_text, 'gnome-generic-albedo.png')
        self.assertEqual(self.gnome.get_node('/textures/1').source_text,
                         'gnome-generic-bump.png          @ units: model-space')
        self.assertEqual(self.gnome.get_node('/textures/2').source_text,
                         'gnome-generic-metallic.png')
        self.assertEqual(self.gnome.get_node('/animations/idle:0').source_text, idle_0)
        self.assertEqual(self.gnome.get_node('/animations/walk').source_text, walk)
        self.assertEqual(self.gnome.get_node('/animations/idle:1').source_text, idle_1)

class TestNodeMetatags(NodeApiTestCase):
    def test_by_index(self):
        for i in range(self.gnome.num_nodes):
            n = self.gnome.get_node(i)
            self.assertEqual(n.metatags, {'units': 'model-space'} if i == 4 else {})
