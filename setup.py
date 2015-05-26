import os
import sys
from setuptools import setup, find_packages
import versioneer
import platform


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if on_rtd:
    install_requires = []
    ext_modules = []
    include_dirs = []
    all_cython_exts = []
else:
    from Cython.Build import cythonize
    import numpy as np

    extra_compile_args = []
    extra_link_args = []

    _platform = platform.platform().lower()
    if 'linux' in _platform:
        extra_compile_args += ['-fopenmp']
        extra_link_args += ['-fopenmp']
    elif 'windows' in _platform:
        extra_compile_args += ['/openmp']
        extra_link_args += ['/openmp']

    # ---- C/C++ EXTENSIONS ---- #
    cython_modules = ['menpo/shape/mesh/normals.pyx',
                      'menpo/transform/piecewiseaffine/fastpwa.pyx',
                      'menpo/feature/windowiterator.pyx',
                      'menpo/external/skimage/_warps_cy.pyx',
                      'menpo/image/extract_patches.pyx']
    openmp_cython_modules = ['menpo/feature/gradient.pyx']

    cython_exts = cythonize(cython_modules, quiet=True)
    openmp_cython_exts = cythonize(openmp_cython_modules, quiet=True)
    for e in openmp_cython_exts:
        e.extra_compile_args = extra_compile_args
        e.extra_link_args = extra_link_args

    all_cython_exts = cython_exts + openmp_cython_exts

    include_dirs = [np.get_include()]
    install_requires = ['numpy>=1.9.1,<1.10',
                        'scipy>=0.15,<0.16',
                        'matplotlib>=1.4,<1.5',
                        'pillow==2.7.0',
                        'Cython>=0.21,<0.22']

    if sys.version_info.major == 2:
        install_requires.append('pathlib==1.0')

# Versioneer allows us to automatically generate versioning from
# our git tagging system which makes releases simpler.
versioneer.VCS = 'git'
versioneer.versionfile_source = 'menpo/_version.py'
versioneer.versionfile_build = 'menpo/_version.py'
versioneer.tag_prefix = 'v'  # tags are like v1.2.0
versioneer.parentdir_prefix = 'menpo-'  # dirname like 'menpo-v1.2.0'

setup(name='menpo',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='iBUG Facial Modelling Toolkit',
      author='James Booth',
      author_email='james.booth08@imperial.ac.uk',
      include_dirs=include_dirs,
      ext_modules=all_cython_exts,
      packages=find_packages(),
      install_requires=install_requires,
      package_data={'menpo': ['data/*',
                              'feature/cpp/*.cpp',
                              'feature/cpp/*.h',
                              'transform/piecewiseaffine/fastpwa/*.c',
                              'transform/piecewiseaffine/fastpwa/*.h'],
                    '': ['*.pxd', '*.pyx']},
      tests_require=['nose', 'mock']
)
