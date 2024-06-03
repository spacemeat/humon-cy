''' Humon-py build. '''
from setuptools import Extension, setup
from distutils.command.build import build as Build_Orig
from Cython.Build import cythonize

extensions = [
    Extension(
        'humon',
        sources = [
            'clib/humon/src/ansiColors.c',
            'clib/humon/src/changes.c',
            'clib/humon/src/encoding.c',
            'clib/humon/src/node.c',
            'clib/humon/src/parse.c',
            'clib/humon/src/printing.c',
            'clib/humon/src/token.c',
            'clib/humon/src/tokenize.c',
            'clib/humon/src/trove.c',
            'clib/humon/src/utils.c',
            'clib/humon/src/vector.c',
            'src/humon/humon.pyx',
        ],
        extra_compile_args = ['-ggdb3', '-O0'],
        include_dirs = [
            'clib/humon/include',
            'clib/humon/src',
            'src/humon'
        ]
    )
]

setup(
    name = 'humon',
    package_data = {'humon': ['clib/humon/humon/humon.h',
                              'clib/humon/humon/ansiColors.h',
                              'clib/humon/humon/version.h',
                              'clib/humon/src/humon_internal.h',
                              'src/humon/humon.pyx',
                              'src/humon/chumon.pyd',
                              'src/humon/humon.c']}, 
    ext_modules = cythonize(extensions,
                            compiler_directives = {'language_level': 3})
)
