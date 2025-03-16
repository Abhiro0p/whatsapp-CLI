from setuptools import setup, find_packages

setup(
    name="whatsapp-cli",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "selenium>=4.9.0",
        "python-dotenv>=0.19.2"
    ],
    entry_points={
        "console_scripts": [
            "whatsapp-cli=src.cli_interface:CLIInterface.start"
        ],
    }
)
