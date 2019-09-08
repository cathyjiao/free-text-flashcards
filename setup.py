from setuptools import setup, find_packages
from setuptools.command.install import install as _install

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read()


class Install(_install):
    """
    Need to download wordnet from nltk
    """

    def run(self):
        _install.do_egg_install(self)
        import nltk
        nltk.download("wordnet")


setup(
    name='vocabtion',
    version='1.0.0',
    description='interactive vocabulary tester',
    long_description=readme,
    author='Cathy Jiao',
    author_email='cathy.jiao@mgmail.com',
    license=license,
    packages=find_packages(),
    package_data={
        'vocabtion': [
            'data/*.json',
            'vocab/*.txt'
        ]
    },
    install_requires=requirements,
    setup_requires=['nltk'],
    cmdclass={'install': Install},
)
