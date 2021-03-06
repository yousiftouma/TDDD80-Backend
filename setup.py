from setuptools import setup

setup(name='MyApplication',
      version='1.0',
      description='OpenShift App',
      author='Yousif Touma',
      author_email='youto814@student.liu.se',
      url='http://www.python.org/sigs/distutils-sig/',
      install_requires=['Flask==0.10.1', 'Flask-SQLAlchemy==2.0', 'sqlalchemy-migrate'],
      )
