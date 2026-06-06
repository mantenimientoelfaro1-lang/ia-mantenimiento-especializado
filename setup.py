from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ia-mantenimiento-especializado",
    version="1.0.0",
    author="Mantenimiento El Faro",
    description="Sistema de IA especializada en mantenimiento técnico con autoaprendizaje",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mantenimientoelfaro1-lang/ia-mantenimiento-especializado",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.9",
    install_requires=[
        "google-cloud-aiplatform>=1.38.0",
        "google-cloud-vision>=3.4.4",
        "google-cloud-language>=2.12.1",
        "google-cloud-bigquery>=3.13.1",
        "Flask>=3.0.0",
        "pandas>=2.0.3",
        "scikit-learn>=1.3.0",
    ],
    entry_points={
        "console_scripts": [
            "ia-mantenimiento=api.app:main",
        ],
    },
)
