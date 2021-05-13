from setuptools import setup


setup(
  name='gswidgetkit',   
  packages=['gswidgetkit', 'gswidgetkit.icons'],   
  version='0.0.2',
  license='Apache 2.0',
  description='Custom wxPython widgets created for use in Gimel Studio',
  long_description_content_type="text/markdown",
  author='Noah Rahm', 
  author_email='correctsyntax@yahoo.com',     
  url='https://github.com/GimelStudio/gswidgetkit', 
  keywords=['wxpython', 'widgets', 'custom'], 
  install_requires=[           
      'wxpython==4.1.1'
    ],
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Topic :: Desktop Environment',
    'Topic :: Multimedia :: Graphics :: Editors',
    'License :: OSI Approved :: Apache Software License', 
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
