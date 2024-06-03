# humon

A Python wrapper for the Humon C API. This project uses Cython, so can theoretically be used wherever Cython modules can be used.

## Installation

Thus far, the Python wrapper has only been tested on Linux-like systems. Available as a PyPI package:

```
$ pip install humon
```

Or, you can clone it from github:

```
$ git clone https://github.com/spacemeat/humon-cy
$ pip install ./humon-cy
```

It's best practice to emplace it in a virtual environment.

## API overview

See the [Humon project readme](https://github.com/spacemeat/humon) for comprehensive details about Humon's format. This readme only describes the Python interface. The API is not strictly 1-1 with the C/C++ APIs.

### Loading troves

Easy. There are two ways:

```python
import humon as h
eqipment_trove = h.from_file('equipment.hu') # default encoding = h.Encoding.UNKNOWN
quests_trove = h.from_file('equipment.hu', h.Encoding.UTF8)
```

```python
import humon as h
trove = h.from_string('{foo: bar}')
```

The file on disk may be encoded with any UTF-n format, as in the C API. Python strings are already Unicode-encoded, and will be converted to UTF-8 (Humon's internal format) if need be.

The returned `trove` is the container for the Humon data. It will hold the entire file or string, and provide very quick access to the contents for reading once loaded. Troves are immutable once created.

> Both functions also take an optional parameter `tab_size: int`. This is to help error diagnostics determine the correct column.

### Accessing nodes

For much of the rest of this document, we'll utilize a sample Humon file on disk:

```
$ cat gnome.hu
@ { app: gamin'-djinn, component: assets-gnome, version: 0.1.0 }
{
    model: gnome-generic.fbx
    textures: [
        gnome-generic-albedo.png
        gnome-generic-bump.png          @ units: model-space
        gnome-generic-metallic.png
    ]
    animations: {
        idle: [
            gnome-idle_0.anim
            gnome-idle_1.anim
        ]
    }
}
```

Humon data is a tree of nodes: lists, dicts, and values, organized like JSON data. There are also comments and annotations, and all of this is described in the [Humon project readme](https://github.com/spacemeat/humon). Currently, comments cannot be accessed through the API, though that is forthcoming.

Getting the root node is done through the `root` property of a trove:

```python
import humon as h
trove = h.from_string('{foo: [a b c d]}')
root = trove.root
```

The returned object is of type `Node`. You can access its kind--list, dict, value--by the `kind` property. A list or dict will have child nodes, accessible through __getitem__(). Any child of a dict will have a `key` property. A value node will have a `value` property.

```python
import humon as h
trove = h.from_string('{foo: [a b c d]}')
root = trove.root
assert root.kind == NodeKind.DICT
lnode = root['foo']
vnode = lnode[2]
print (vnode.value)  # prints: c
```

A minor difference between Humon and JSON is that Humon dict entries can be accessed by index as well, and keep their order as loaded. (This is a strict language feature, and not dependent on any API.)

```python
import humon as h
trove = h.from_string('{foo: foofoo, bar: barbar, baz: bazbaz}')
vnode = trove.root[2]
print (vnode.value)  # prints bazbaz
```

Another minor difference between Humon and JSON is that Humon dicts do not have to have unique keys. You can access the nth child node with a given key:

```python
import humon as h
trove = h.from_string('''{ foo: [a b c d]
                                 bar: snaa
                                 foo: [e f g h]
                                 baz: plugh
                                 foo: [i j k l] }''')
vnode = trove.root['foo', 2]
print (f'{vnode.address}: {vnode.value}') # prints: /foo: [i j k l]
```

You can also access nodes via address:

```python
import humon as h
trove = h.from_string('{foo: [a b c d]}')
vnode = trove.get_node('/foo/2')
print (f'{vnode.address}: {vnode.value}') # prints: /foo/2: c
vnode = vnode.get_node('../3')
print (f'{vnode.address}: {vnode.value}') # prints: /foo/3: d
```

Nodes which share a parent are `sibling` nodes:

```python
import humon as h
trove = h.from_string('{foo: [a b c d] bar: [e f g h]}')
vnode = trove.get_node('/foo')
print (f'{vnode.address}: {vnode.value}') # prints: /foo: [a b c d]
vnode = vnode.get_sibling('bar')
print (f'{vnode.address}: {vnode.value}') # prints: /bar: [e f g h]
vnode = vnode[0].sibling()
print (f'{vnode.address}: {vnode.value}') # prints: /bar/0: e
```

A trove stores nodes as a linear array internally, and nodes can be accessed by index from the Trove ojbect:

```python
import humon as h
trove = h.from_string('{foo: [a b c d]}')
print (trove.get_node(4).value) # prints: c
```

### Annotations

Annotations on a trove or node are returned as dicts. Assuming a reasonable implementation of a Version class:

```python
import humon as h

data = '''@ { app: gamin'-djinn, component: assets-gnome, version: 0.1.0 }
{
    model: gnome-generic.fbx
    textures: [
        gnome-generic-albedo.png
        gnome-generic-bump.png          @ units: model-space
        gnome-generic-metallic.png
    ]
    animations: {
        idle: [
            gnome-idle_0.anim
            gnome-idle_1.anim
        ]
    }
}'''

trove = h.from_string(data)
to = trove.annotations
assert to['app'] == "gamin'-djinn"
if Version(to['version']).in_range('0.0.4', '0.1.3'):
    print (trove.get_node('/textures/1').annotations) # prints: {'units': 'model-space'}
```

### Serializing

Though a trove is immutable, it can be printed in a few ways. The most useful maybe is with Trove.to_string() and Trove.to_file():

```python
...
s = trove.to_string(h.WhitespaceFormat.MINIMAL, print_comments = False)
```

The minimal formatting reduces the whitespace to a minimum while keeping Humon semantics the same. You can do a pretty formatting as well:

```python
...
trove.to_file(path: 'pretty.h',
              whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = 4,
              indent_with_tabs = False, use_colors = True, color_table = None, 
              print_comments = True, newline = '\n', print_bom = True)
```

Passing `True` to `use_colors` will insert colorizing markup entries appropriately in the resutlant string. If you specify `use_colors`, but do not provide a color table, the API will use some ANSI color codes as default values. Set color entries for each color type like so:

```python
...
named_fg = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',

    'bright black': '\033[90m',
    'bright red': '\033[91m',
    'bright green': '\033[92m',
    'bright yellow': '\033[93m',
    'bright blue': '\033[94m',
    'bright magenta': '\033[95m',
    'bright cyan': '\033[96m',
    'bright white': '\033[97m',
}

color_table = {
    h.ColorCode.TOKENSTREAMBEGIN: '',
    h.ColorCode.TOKENSTREAMEND: '\033[0m',
    h.ColorCode.TOKENEND: '',
    h.ColorCode.PUNCLIST: named_fg['bright white'],
    h.ColorCode.PUNCDICT: named_fg['bright white'],
    h.ColorCode.PUNCKEYVALUESEP: named_fg['bright white'],
    h.ColorCode.PUNCANNOTATE: named_fg['bright blue'],
    h.ColorCode.PUNCANNOTATEDICT: named_fg['bright blue'],
    h.ColorCode.PUNCANNOTATEKEYVALUESEP: named_fg['blue'],
    h.ColorCode.KEY: named_fg['cyan'],
    h.ColorCode.VALUE: named_fg['bright cyan'],
    h.ColorCode.COMMENT: named_fg['red'],
    h.ColorCode.ANNOKEY: named_fg['magenta'],
    h.ColorCode.ANNOVALUE: named_fg['bright magenta'],
    h.ColorCode.WHITESPACE: named_fg['white'],
}

trove.to_file(path: 'pretty.h',
              whitespace_format = h.WhitespaceFormat.PRETTY, indent_size = 4,
              indent_with_tabs = False, use_colors = True, color_table = color_table,
              print_comments = True, newline = '\n', print_bom = True)
```

You can also access full text in a node or trove with `token_string`:

```python
import humon as h
trove = h.from_string('{foo: [a b {color: {green: [froggy, leafy]}} d]}')
print (trove.get_node('/foo/2').token_string)   # prints: {green: [froggy, leafy]}}
print (trove.token_string)                      # prints the whole trove
```

> Calling `token_string` on the trove is nearly equivalent to calling 'Trove.to_string' with `whitespace_format` set to `humon.WhitespaceFormat.CLONED` and no colors. But, since it copies directly from the loaded text, it is much faster.
