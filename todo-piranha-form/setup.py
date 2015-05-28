import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'pyramid_jinja2',
    'WTForms',
    ]

setup(name='todo-piranha-form',
      version='0.0',
      description='todo-piranha-form',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Areski Belaid',
      author_email='areski@gmail.com',
      url='https://github.com/areski/todo-piranha',
      keywords='python pyramid web todo',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='todopiranhaform',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = todopiranhaform:main
      [console_scripts]
      initialize_todo-piranha-form_db = todopiranhaform.scripts.initializedb:main
      """,
      )
