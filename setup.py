from setuptools import find_packages, setup

setup(
    name='volcano_stats_flask',
    version='1.0',
    description='COMP0034 Coursework 1 2021-22',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plotly',
        'pandas',
        'dash',
        'dash-bootstrap-components',
    ],
)
