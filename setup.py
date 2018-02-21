from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    with open('README.md') as f:
        long_description = f.read().strip()

with open('VERSION') as f:
    version = f.read().strip()

setup(
    name='anon-ai-toolbelt',
    description='A command-line tool for using the Anon AI web service.',
    long_description=long_description,
    url='https://github.com/anon-ai/toolbelt',
    author='Anon AI',
    author_email='info@anon.ai',
    version=version,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
      'click>=5',
      'pycrypto>=2',
      'requests>=2',
    ],
    python_requires='>=3',
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'anon = anon_ai_toolbelt.command:main',
        ],
    },
)
