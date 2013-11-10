#coding: utf8
import os
import shutil
import subprocess
import glob
from distutils.core import setup

def install_discount():
    root = os.path.dirname(os.path.abspath(__file__))
    os.chdir('_discount')
    subprocess.call('chmod 755 configure.sh'.split())
    subprocess.call(
        ['./configure.sh',
         '--with-fenced-code',
         '--with-urlencoded-anchor',
         '--enable-all-features',
         '--shared',
        ], env=os.environ)
    subprocess.call(['make', 'install'])
    os.chdir(root)


    _md_path = None
    for path in glob.glob('_discount/libmarkdown.so*') + glob.glob('_discount/libmarkdown.dylib'):
        if not os.path.islink(path):
            _md_path = path
            break
    if not _md_path:
        return # ignore

    md_path = os.path.join(root, 'discount/markdown.so')

    shutil.copy(_md_path, md_path )


install_discount()

setup(
    name='discount',
    license='BSD',
    version='0.2.1STABLE',

    author='Trapeze',
    author_email='tkemenczy@trapeze.com',
    url="http://github.com/trapeze/python-discount",
    download_url='http://pypi.python.org/pypi/discount',
    description='A Python interface for Discount, the C Markdown parser',
    long_description=open('README.rst').read(),
    keywords='markdown discount ctypes',

    packages = ['discount', ],
    package_data={'discount': ['markdown.so']},

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Markup'
    ],
)