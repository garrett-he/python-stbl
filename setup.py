from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='stbl',
    ext_modules=cythonize([
        './src/stbl/__init__.py',

        './src/stbl/__cli__.py',

    ], language_level='3str'),
    requires=['Cython']
)
