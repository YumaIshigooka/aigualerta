from setuptools import setup, find_packages

setup(
    name='aigualerta',  # Replace with your actual package name if different
    version='0.1.0',    # Replace with your package version
    packages=find_packages(where='src'),  # Adapt if your packages are not in 'src'
    package_dir={'': 'src'},  # Adapt if your packages are not in 'src'
    install_requires=[
        'pandas',
        'numpy',
        'pyarrow',
        'matplotlib',
        'scikit-learn',
        'seaborn',
        'streamlit',
        'st-theme',
        'pytest',
        'pytest-cov'
    ],
)