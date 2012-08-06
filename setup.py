from setuptools import setup

setup(name='expect', version='0.0.1', author='Sumeet Agarwal',
      author_email='sumeet.a@gmail.com', url='https://github.com/sumeet/expect',
      description='Terse mock expectations for Python and Mock',
      classifiers=['Programming Language :: Python',
                   'Operating System :: OS Independent',
                   'License :: OSI Approved :: MIT License',
                   'Topic :: Software Development :: Testing',
                   'Intended Audience :: Developers',
                   'Development Status :: 2 - Pre-Alpha'],
    install_requires=['Mock'],
    license='MIT',
    py_modules=['expect'],
    long_description=open('README.markdown').read())
