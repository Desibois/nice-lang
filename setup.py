from setuptools import setup, find_packages

setup(
    name="nice-lang",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
"rich>=13.9.4",
"regex>=2024.11.6",
"requests>=2.32.3",
"pyyaml>=6.0.2",
"sympy>=1.13.1",
"langchain-ollama>=0.2.3"
], 
    entry_points={
        "console_scripts": [
            "nice=nice.compiler:run_compiler"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
