from setuptools import setup, find_packages

setup(
    name="ml-titanic",
    version="1.0.0",
    description="Projet MLOps complet - Prédiction de survie Titanic",
    author="Votre Nom",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "scikit-learn>=1.3.0",
        "pandas>=2.0.3",
        "numpy>=1.24.3",
        "mlflow>=2.7.1",
        "fastapi>=0.103.1",
        "loguru>=0.7.0",
    ],
)
