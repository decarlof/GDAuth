from setuptools import setup, Extension, find_packages

setup(
    name = 'gdauth',
    author = 'Francesco De Carlo',
    author_email = 'decarlo@anl.gov',
    description = 'Globus Data Management Tool.',
    packages = find_packages(),
    entry_points={'console_scripts':['gdauth = gdauth.__main__:main'],},
    version = open('VERSION').read().strip(),
    zip_safe = False,
    url='http://gdauth.readthedocs.org',
    download_url='https://github.com/decarlof/gdauth.git',
    license='BSD-3',
    platforms='Any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Education',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
)

