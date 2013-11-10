#coding: utf8
import os
import subprocess
import glob
from distutils.core import setup, Extension
from distutils.command.build_py import build_py as _build_py
from distutils.command.build_ext import build_ext as _build_ext


DISCOUNT_VERSION = '2.1.7'
root = os.path.dirname(os.path.abspath(__file__))

class build_ext(_build_ext):
    def install_discount(self):
        os.chdir('_discount')
        subprocess.call('chmod 755 configure.sh'.split())
        subprocess.call(
            ['./configure.sh',
             '--with-fenced-code',
             '--with-urlencoded-anchor',
             '--enable-all-features',
            ], env=os.environ)
        subprocess.call(['make', 'install'], env=os.environ)
        os.chdir(root)

    def build_extension(self, ext):
        self.install_discount()

        discount_src_path = os.path.join(root, '_discount')

        ext.extra_compile_args += [
            '-I%s' % discount_src_path,
            '-DVERSION="%s"' % DISCOUNT_VERSION
        ]

        _build_ext.build_extension(self, ext)




class build_py(_build_py):

    def install_discount(self):
        root = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.join(root, '_discount'))
        subprocess.call('chmod 755 configure.sh'.split())
        subprocess.call(
            ['./configure.sh',
             '--with-fenced-code',
             '--with-urlencoded-anchor',
             '--enable-all-features', '--shared'
            ], env=os.environ)
        os.chdir(root)

    def run(self):
        self.install_discount()
        _build_py.run(self)

os.chdir('_discount')
resources = glob.glob('_discount/*.c')
os.chdir(root)


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

    ext_modules=[
        Extension(
            '_discount',
            sources=resources,
        )
    ],


    cmdclass={
        'build_ext': build_ext
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