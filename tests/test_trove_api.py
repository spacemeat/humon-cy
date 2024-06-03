''' Unit tests for humon.cy '''

#pylint: disable=missing-class-docstring, missing-function-docstring
#pylint: disable=too-many-public-methods, too-many-lines

from pathlib import Path
import unittest
import humon as h

class Foo:
    pass

def path_of(filename: str):
    return str(Path(__file__).parent / filename)

class TroveApiTestCase(unittest.TestCase):
    def setUp(self):
        self.inane = h.from_string('')
        self.comment_only = h.from_string('// snark')
        self.metatag_only = h.from_string('@ foo: bar')
        self.value_only = h.from_string('dreams')
        self.list_only = h.from_string('[]')
        self.dict_only = h.from_string('{}')
        self.gnome = h.from_file(path_of('gnome.hu'))


class TestTroveRoot(TroveApiTestCase):
    def test_root_inane(self):
        root = self.inane.root
        self.assertIsNone(root)

    def test_root_kind_comment_only(self):
        root = self.comment_only.root
        self.assertIsNone(root)

    def test_root_kind_metatag_only(self):
        root = self.metatag_only.root
        self.assertIsNone(root)

    def test_root_kind_value_only(self):
        root = self.value_only.root
        self.assertIsInstance(root, h.Node)
        self.assertEqual(root.kind, h.NodeKind.VALUE)
        self.assertEqual(root.num_children, 0)
        self.assertEqual(root.source_text, 'dreams')

    def test_root_kind_list_only(self):
        root = self.list_only.root
        self.assertIsInstance(root, h.Node)
        self.assertEqual(root.kind, h.NodeKind.LIST)
        self.assertEqual(root.num_children, 0)
        self.assertEqual(root.source_text, '[]')

    def test_root_kind_dict_only(self):
        root = self.dict_only.root
        self.assertIsInstance(root, h.Node)
        self.assertEqual(root.kind, h.NodeKind.DICT)
        self.assertEqual(root.num_children, 0)
        self.assertEqual(root.source_text, '{}')

    def test_root_gnome(self):
        root = self.gnome.root
        self.assertIsInstance(root, h.Node)
        self.assertEqual(root.kind, h.NodeKind.DICT)
        self.assertEqual(root.num_children, 4)
        cmp = '{\n    model: gnome-generic'
        self.assertEqual(root.source_text[:len(cmp)], cmp)

class TestTroveGetNodeInt(TroveApiTestCase):
    def test_pathological_negone(self):
        self.assertIsNone(self.inane.get_node(-1))
        self.assertIsNone(self.comment_only.get_node(-1))
        self.assertIsNone(self.metatag_only.get_node(-1))
        self.assertIsNone(self.value_only.get_node(-1))
        self.assertIsNone(self.list_only.get_node(-1))
        self.assertIsNone(self.dict_only.get_node(-1))
        self.assertIsNone(self.gnome.get_node(-1))

    def test_pathological_much(self):
        self.assertIsNone(self.inane.get_node(1000000))
        self.assertIsNone(self.comment_only.get_node(1000000))
        self.assertIsNone(self.metatag_only.get_node(1000000))
        self.assertIsNone(self.value_only.get_node(1000000))
        self.assertIsNone(self.list_only.get_node(1000000))
        self.assertIsNone(self.dict_only.get_node(1000000))
        self.assertIsNone(self.gnome.get_node(1000000))

    def test_zero(self):
        self.assertIsNone(self.inane.get_node(0))
        self.assertIsNone(self.comment_only.get_node(0))
        self.assertIsNone(self.metatag_only.get_node(0))
        n = self.value_only.get_node(0)
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)
        n = self.list_only.get_node(0)
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.LIST)
        n = self.dict_only.get_node(0)
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.DICT)
        n = self.gnome.get_node(0)
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.DICT)

    def test_one(self):
        self.assertIsNone(self.inane.get_node(1))
        self.assertIsNone(self.comment_only.get_node(1))
        self.assertIsNone(self.metatag_only.get_node(1))
        self.assertIsNone(self.value_only.get_node(1))
        self.assertIsNone(self.list_only.get_node(1))
        self.assertIsNone(self.dict_only.get_node(1))
        n = self.gnome.get_node(1)
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)

class TestTroveGetNodeAddress(TroveApiTestCase):
    def test_pathological_none(self):
        with self.assertRaises(TypeError):
            self.inane.get_node(None)
        with self.assertRaises(TypeError):
            self.comment_only.get_node(None)
        with self.assertRaises(TypeError):
            self.metatag_only.get_node(None)
        with self.assertRaises(TypeError):
            self.value_only.get_node(None)
        with self.assertRaises(TypeError):
            self.list_only.get_node(None)
        with self.assertRaises(TypeError):
            self.dict_only.get_node(None)
        with self.assertRaises(TypeError):
            self.gnome.get_node(None)

    def test_pathological_foo(self):
        with self.assertRaises(TypeError):
            self.inane.get_node(Foo())
        with self.assertRaises(TypeError):
            self.comment_only.get_node(Foo())
        with self.assertRaises(TypeError):
            self.metatag_only.get_node(Foo())
        with self.assertRaises(TypeError):
            self.value_only.get_node(Foo())
        with self.assertRaises(TypeError):
            self.list_only.get_node(Foo())
        with self.assertRaises(TypeError):
            self.dict_only.get_node(Foo())
        with self.assertRaises(TypeError):
            self.gnome.get_node(Foo())

    def test_pathological_nonsense(self):
        self.assertIsNone(self.inane.get_node('foo'))
        self.assertIsNone(self.comment_only.get_node('foo'))
        self.assertIsNone(self.metatag_only.get_node('foo'))
        self.assertIsNone(self.value_only.get_node('foo'))
        self.assertIsNone(self.list_only.get_node('foo'))
        self.assertIsNone(self.dict_only.get_node('foo'))
        self.assertIsNone(self.gnome.get_node('foo'))

    def test_pathological_neg_idx(self):
        self.assertIsNone(self.inane.get_node('/-1'))
        self.assertIsNone(self.comment_only.get_node('/-1'))
        self.assertIsNone(self.metatag_only.get_node('/-1'))
        self.assertIsNone(self.value_only.get_node('/-1'))
        self.assertIsNone(self.list_only.get_node('/-1'))
        self.assertIsNone(self.dict_only.get_node('/-1'))
        self.assertIsNone(self.gnome.get_node('/-1'))

    def test_pathological_huge_idx(self):
        self.assertIsNone(self.inane.get_node('/1000000'))
        self.assertIsNone(self.comment_only.get_node('/1000000'))
        self.assertIsNone(self.metatag_only.get_node('/1000000'))
        self.assertIsNone(self.value_only.get_node('/1000000'))
        self.assertIsNone(self.list_only.get_node('/1000000'))
        self.assertIsNone(self.dict_only.get_node('/1000000'))
        self.assertIsNone(self.gnome.get_node('/1000000'))

    def test_pathological_wrong_path(self):
        self.assertIsNone(self.inane.get_node('/foo'))
        self.assertIsNone(self.comment_only.get_node('/foo'))
        self.assertIsNone(self.metatag_only.get_node('/foo'))
        self.assertIsNone(self.value_only.get_node('/foo'))
        self.assertIsNone(self.list_only.get_node('/foo'))
        self.assertIsNone(self.dict_only.get_node('/foo'))
        self.assertIsNone(self.gnome.get_node('/foo'))

    def test_root(self):
        self.assertIsNone(self.inane.get_node('/'))
        self.assertIsNone(self.comment_only.get_node('/'))
        self.assertIsNone(self.metatag_only.get_node('/'))
        n = self.value_only.get_node('/')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)
        n = self.list_only.get_node('/')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.LIST)
        n = self.dict_only.get_node('/')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.DICT)
        n = self.gnome.get_node('/')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.DICT)

    def test_basic(self):
        self.assertIsNone(self.inane.get_node('/model'))
        self.assertIsNone(self.comment_only.get_node('/model'))
        self.assertIsNone(self.metatag_only.get_node('/model'))
        self.assertIsNone(self.value_only.get_node('/model'))
        self.assertIsNone(self.list_only.get_node('/model'))
        self.assertIsNone(self.dict_only.get_node('/model'))
        n = self.gnome.get_node('/model')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)

    def test_interesting(self):
        n = self.gnome.get_node('/textures')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.LIST)
        n = self.gnome.get_node('/textures/0')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)
        n = self.gnome.get_node('/animations')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.DICT)
        n = self.gnome.get_node('/animations/idle/animation')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.value, 'gnome-idle_1.anim')
        self.assertEqual(n.kind, h.NodeKind.VALUE)
        n = self.gnome.get_node('/animations/idle:0/animation')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)
        self.assertEqual(n.value, 'gnome-idle_0.anim')
        n = self.gnome.get_node('/animations/idle:1/animation')
        self.assertIsInstance(n, h.Node)
        self.assertEqual(n.kind, h.NodeKind.VALUE)
        self.assertEqual(n.value, 'gnome-idle_1.anim')

class TestTroveNumNodes(TroveApiTestCase):
    def test(self):
        self.assertEqual(self.inane.num_nodes, 0)
        self.assertEqual(self.comment_only.num_nodes, 0)
        self.assertEqual(self.metatag_only.num_nodes, 0)
        self.assertEqual(self.value_only.num_nodes, 1)
        self.assertEqual(self.list_only.num_nodes, 1)
        self.assertEqual(self.dict_only.num_nodes, 1)
        self.assertEqual(self.gnome.num_nodes, 23)

class TestTroveSourceText(TroveApiTestCase):
    def test(self):
        self.assertEqual(self.inane.source_text, '')
        self.assertEqual(self.comment_only.source_text, '// snark')
        self.assertEqual(self.metatag_only.source_text, '@ foo: bar')
        self.assertEqual(self.value_only.source_text, 'dreams')
        self.assertEqual(self.list_only.source_text, '[]')
        self.assertEqual(self.dict_only.source_text, '{}')
        with open(path_of('gnome.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.source_text, f.read())

class TestTroveMetatags(TroveApiTestCase):
    def test(self):
        self.assertEqual(self.inane.metatags, {})
        self.assertEqual(self.comment_only.metatags, {})
        self.assertEqual(self.metatag_only.metatags, {'foo': 'bar'})
        self.assertEqual(self.value_only.metatags, {})
        self.assertEqual(self.list_only.metatags, {})
        self.assertEqual(self.dict_only.metatags, {})
        metatags = {'app': "gamin'-djinn", 'component': 'assets-gnome', 'version': '0.1.0'}
        self.assertEqual(self.gnome.metatags, metatags)

class TestTroveToString(TroveApiTestCase):
    def test_pathological_indent_neg(self):
        with self.assertRaises(h.SerializeError):
            self.inane.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.comment_only.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.metatag_only.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.value_only.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.list_only.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.dict_only.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.gnome.to_string(
            whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)

    def test_pathological_empty_table(self):
        table = {}
        with open(path_of('inane-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.inane.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('comment-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.comment_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('metatag-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.metatag_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('value-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.value_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('list-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.list_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('dict-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.dict_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('gnome-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())

    def test_pathological_goofy_table(self):
        table = {}.fromkeys('foo' * h.ColorCode.NUMCOLORS.value)
        with open(path_of('inane-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.inane.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('comment-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.comment_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('metatag-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.metatag_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('value-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.value_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('list-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.list_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('dict-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.dict_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())
        with open(path_of('gnome-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table), f.read())

    def test_default(self):
        with open(path_of('inane-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.inane.to_string(), f.read())
        with open(path_of('comment-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.comment_only.to_string(), f.read())
        with open(path_of('metatag-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.metatag_only.to_string(), f.read())
        with open(path_of('value-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.value_only.to_string(), f.read())
        with open(path_of('list-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.list_only.to_string(), f.read())
        with open(path_of('dict-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.dict_only.to_string(), f.read())
        with open(path_of('gnome-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(), f.read())

    def test_cloned(self):
        self.assertEqual(self.inane.to_string(h.WhitespaceFormat.CLONED), '')
        self.assertEqual(self.comment_only.to_string(h.WhitespaceFormat.CLONED), '// snark')
        self.assertEqual(self.metatag_only.to_string(h.WhitespaceFormat.CLONED), '@ foo: bar')
        self.assertEqual(self.value_only.to_string(h.WhitespaceFormat.CLONED), 'dreams')
        self.assertEqual(self.list_only.to_string(h.WhitespaceFormat.CLONED), '[]')
        self.assertEqual(self.dict_only.to_string(h.WhitespaceFormat.CLONED), '{}')
        with open(path_of('gnome.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(h.WhitespaceFormat.CLONED), f.read())

    def test_minimal(self):
        with open(path_of('inane-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.inane.to_string(h.WhitespaceFormat.MINIMAL), f.read())
        with open(path_of('comment-only-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.comment_only.to_string(h.WhitespaceFormat.MINIMAL), f.read())
        with open(path_of('metatag-only-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.metatag_only.to_string(h.WhitespaceFormat.MINIMAL), f.read())
        with open(path_of('value-only-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.value_only.to_string(h.WhitespaceFormat.MINIMAL), f.read())
        with open(path_of('list-only-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.list_only.to_string(h.WhitespaceFormat.MINIMAL), f.read())
        with open(path_of('dict-only-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.dict_only.to_string(h.WhitespaceFormat.MINIMAL), f.read())
        with open(path_of('gnome-pm-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(h.WhitespaceFormat.MINIMAL), f.read())

    def test_pretty(self):
        with open(path_of('inane-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.inane.to_string(h.WhitespaceFormat.PRETTY), f.read())
        with open(path_of('comment-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.comment_only.to_string(h.WhitespaceFormat.PRETTY), f.read())
        with open(path_of('metatag-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.metatag_only.to_string(h.WhitespaceFormat.PRETTY), f.read())
        with open(path_of('value-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.value_only.to_string(h.WhitespaceFormat.PRETTY), f.read())
        with open(path_of('list-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.list_only.to_string(h.WhitespaceFormat.PRETTY), f.read())
        with open(path_of('dict-only-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.dict_only.to_string(h.WhitespaceFormat.PRETTY), f.read())
        with open(path_of('gnome-pp-cn.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(h.WhitespaceFormat.PRETTY), f.read())

    def test_pretty_colors(self):
        with open(path_of('inane-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.inane.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())
        with open(path_of('comment-only-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.comment_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())
        with open(path_of('metatag-only-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.metatag_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())
        with open(path_of('value-only-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.value_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())
        with open(path_of('list-only-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.list_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())
        with open(path_of('dict-only-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.dict_only.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())
        with open(path_of('gnome-pp-ca.hu'), 'rt', encoding = 'utf-8') as f:
            self.assertEqual(self.gnome.to_string(
                h.WhitespaceFormat.PRETTY, use_colors = True), f.read())

class TestTroveToFile(TroveApiTestCase):
    def test_pathological_indent_neg(self):
        with self.assertRaises(h.SerializeError):
            self.inane.to_file(path_of("test_output/inane.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.comment_only.to_file(path_of("test_output/comment_only.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.metatag_only.to_file(path_of("test_output/metatag_only.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.value_only.to_file(path_of("test_output/value_only.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.list_only.to_file(path_of("test_output/list_only.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.dict_only.to_file(path_of("test_output/dict_only.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)
        with self.assertRaises(h.SerializeError):
            self.gnome.to_file(path_of("test_output/gnome.hu"),
                whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = -1)

    def test_pathological_empty_table(self):
        table = {}
        self.inane.to_file(path_of("test_output/inane.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())

    def test_pathological_goofy_table(self):
        table = {}.fromkeys([f'foo{i}' for i in range(h.ColorCode.NUMCOLORS.value)])
        self.inane.to_file(path_of("test_output/inane.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True, color_table = table)
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())

    def test_default(self):
        self.inane.to_file(path_of("test_output/inane.hu"))
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"))
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"))
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"))
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"))
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"))
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"))
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())

    def test_cloned(self):
        self.inane.to_file(path_of("test_output/inane.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"), h.WhitespaceFormat.CLONED)
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pc-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())

    def test_minimal(self):
        self.inane.to_file(path_of("test_output/inane.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"), h.WhitespaceFormat.MINIMAL)
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pm-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())

    def test_pretty(self):
        self.inane.to_file(path_of("test_output/inane.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"), h.WhitespaceFormat.PRETTY)
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pp-cn.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())

    def test_pretty_colors(self):
        self.inane.to_file(path_of("test_output/inane.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/inane.hu"), 'rb') as o:
            with open(path_of('inane-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.comment_only.to_file(path_of("test_output/comment_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/comment_only.hu"), 'rb') as o:
            with open(path_of('comment-only-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.metatag_only.to_file(path_of("test_output/metatag_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/metatag_only.hu"), 'rb') as o:
            with open(path_of('metatag-only-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.value_only.to_file(path_of("test_output/value_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/value_only.hu"), 'rb') as o:
            with open(path_of('value-only-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.list_only.to_file(path_of("test_output/list_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/list_only.hu"), 'rb') as o:
            with open(path_of('list-only-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.dict_only.to_file(path_of("test_output/dict_only.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/dict_only.hu"), 'rb') as o:
            with open(path_of('dict-only-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
        self.gnome.to_file(path_of("test_output/gnome.hu"),
                h.WhitespaceFormat.PRETTY, use_colors = True)
        with open(path_of("test_output/gnome.hu"), 'rb') as o:
            with open(path_of('gnome-pp-ca.hu'), 'rb') as f:
                self.assertEqual(o.read(), f.read())
