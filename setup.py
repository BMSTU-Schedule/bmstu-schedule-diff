from setuptools import setup

setup(
    name='bmstu-schedule-diff',
    version='1.0.0',
    author='Nikola Trubitsyn',
    author_email='nikola.trubitsyn@gmail.com',
    url='https://github.com/trubitsyn/bmstu-schedule-diff',
    python_requires='>=3.6',
    long_description_content_type='text/markdown',
    description='Display BMSTU schedule diff',
    long_description=open('README.md').read(),
    classifiers=[
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['bmstu_schedule_diff'],
    install_requires=[
        'bmstu_schedule'
    ],
    entry_points={
        'console_scripts': [
            'bmstu-schedule-diff = bmstu_schedule_diff.__main__:main'
        ]
    },
)