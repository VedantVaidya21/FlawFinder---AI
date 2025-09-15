"""
Setup script for FlawFinder AI Backend

This file is maintained for backward compatibility with older Python packaging tools.
Newer projects should use pyproject.toml instead.
"""

from setuptools import setup, find_packages

# Read requirements from pyproject.toml
def get_requirements():
    with open('requirements.txt') as f:
        return f.read().splitlines()

setup(
    name="flawfinder-ai",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=get_requirements(),
    python_requires=">=3.9",
    entry_points={
        'console_scripts': [
            'flawfinder=app.main:app',
        ],
    },
    # Metadata
    author="FlawFinder Team",
    author_email="contact@flawfinder.ai",
    description="AI-powered business workflow analysis tool",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flawfinder-ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
