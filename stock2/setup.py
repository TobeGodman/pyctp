from distutils.core import setup
from distutils.util import get_platform
from distutils.extension import Extension
import re, sys, os, struct, shutil
fp = open('ctp/__init__.py', 'rb'); data = fp.read(); fp.close()
if sys.version_info[0] >= 3: data = data.decode('utf-8')
__version__ = re.search(r"__version__ = '(.+?)'", data).group(1)
__author__ = re.search(r"__author__ = '(.+?)'", data).group(1)

PREFIX = ''
BUILD = (
    ('MdApi', 'thostmduserapiSSE'),
    ('TraderApi', 'thosttraderapiSSE'),
)

platform = get_platform()
api_dir = PREFIX+'api/%s'%platform
include_dirs = [PREFIX+'ctp', api_dir]
library_dirs = [api_dir]
ext_modules = []; package_data = []
for k,v in BUILD:
    extm = Extension(name='ctp._'+k, language='c++',
        include_dirs=include_dirs, library_dirs=library_dirs,
        libraries=[v], sources=['ctp/%s.cpp'%k],
    )
    ext_modules.append(extm)
    if platform.startswith('win'):
        k = '%s.dll'%v
    else:
        extm.extra_link_args = ['-Wl,-rpath,$ORIGIN']
        k = 'lib%s.so'%v
    package_data.append(k)
    v = 'ctp/' + k
    if not os.path.exists(v):
        shutil.copy2('%s/%s'%(api_dir,k), v)

setup(
    name='ctp', version=__version__, author=__author__,
    cmdclass={}, ext_modules=ext_modules,
    packages=['ctp'], package_dir={'ctp':'ctp'}, package_data={'ctp':package_data},
)
