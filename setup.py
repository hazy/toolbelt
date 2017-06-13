from setuptools import setup, find_packages

with open('VERSION') as f:
    version = f.read().strip()

setup(
    name='anon-ai-toolbelt',
    version=version,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    entry_points = {
        'console_scripts': [
            'anon = toolbelt.command:main',
        ],
    },
)
