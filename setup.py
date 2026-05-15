from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="amr-plasmid-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Integrated analysis tool for AMR genes, virulence factors, and plasmids",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/AMR-Plasmid-Analysis-Tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "openpyxl>=3.0.0",
        "scipy>=1.7.0",
    ],
    entry_points={
        "console_scripts": [
            "amr-analyzer=src.main:main",
        ],
    },
)
