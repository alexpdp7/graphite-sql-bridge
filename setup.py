from setuptools import setup, find_packages

setup(
    name='graphite-sql-bridge',
    version='0.0.1',
    packages=find_packages(),
    install_requires=['Flask', 'flask-cors'],
    extras_require={
        'dev': ['ipdb', 'ipython'],
    },
)
