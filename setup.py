from setuptools import setup, find_packages

setup(
    name="imagi-matrix",
    version="0.0.1",
    description="All Opencv related manipulations",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Linux/WINDOWS",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pandas==2.1.3",
        "pytest==7.4.3",
        "opencv-python==4.8.1.78",
        "loguru==0.7.2",
        "Pillow==9.5.0",
        "pydantic==2.4.2"
    ],
)
