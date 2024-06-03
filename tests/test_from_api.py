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

class TestFromString(unittest.TestCase):
    def test_wrong(self):
        with self.assertRaises(h.DeserializeError):
            h.from_file('foo:bar')

    def test_pathological(self):
        with self.assertRaises(TypeError):
            h.from_string(None)
        with self.assertRaises(TypeError):
            h.from_string(Foo())
        with self.assertRaises(TypeError):
            h.from_string('{foo:bar}', Foo())
        with self.assertRaises(h.DeserializeError):
            h.from_string('{foo:bar}', -1)
        with self.assertRaises(TypeError):
            h.from_string('{foo:bar}', None)

class TestFromFile(unittest.TestCase):
    def test_wrong(self):
        with self.assertRaises(h.DeserializeError):
            h.from_file(path_of('foobarbaz.hu'))

    def test_pathological(self):
        with self.assertRaises(TypeError):
            h.from_file(None)
        with self.assertRaises(TypeError):
            h.from_file(Foo())
        with self.assertRaises(TypeError):
            h.from_file(path_of('gnome.hu'), Foo())
        with self.assertRaises(TypeError):
            h.from_file(path_of('gnome.hu'), -1)
        with self.assertRaises(TypeError):
            h.from_file(path_of('gnome.hu'), h.Encoding.UTF8, Foo())
        with self.assertRaises(h.DeserializeError):
            h.from_file(path_of('gnome.hu'), h.Encoding.UTF8, -1)
        with self.assertRaises(h.DeserializeError):
            h.from_file(path_of('gnome.hu'), h.Encoding.UTF16_LE)
        with self.assertRaises(h.DeserializeError):
            h.from_file(path_of('gnome.hu'), h.Encoding.UTF32_LE)
