#coding: utf8
import os
import shutil
import subprocess
from distutils.core import setup
from distutils.command.build_py import build_py as _build_py



class build_py(_build_py):

    def install_discount(self):
        root = os.path.dirname(os.path.abspath(__file__))
        md_path = os.path.join(root, 'discount/markdown')
        _md_path = os.path.join(root, '_discount/markdown')
        if os.path.isfile(md_path):
            return
        else:
            os.chdir('_discount')
            subprocess.call('chmod 777 configure.sh'.split())
            subprocess.call(['./configure.sh', '--with-fenced-code', '--with-urlencoded-anchor', '--enable-all-features'])
            subprocess.call(['make', 'install'])
            os.chdir(root)
            shutil.copy(_md_path, md_path )

    def run(self):
        self.install_discount()
        _build_py.run(self)


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
    package_data={'discount': ['markdown']},

    cmdclass={
        'build_py': build_py
    },



    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: C',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Markup'
    ],
)