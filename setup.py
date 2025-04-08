from pathlib import Path
import setuptools

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name="streamlit-tldraw",
    version="0.1.2",
    author="Prashant",
    author_email="prashantc592114@gmail.com",
    description="Streamlit component that integrates TLDraw, a powerful whiteboard and drawing tool directly to your streamlit apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mr-Dark-debug/streamlit-tldraw",
    #packages=setuptools.find_packages(),
    packages=['streamlit_tldraw'],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "streamlit >= 1.17.0",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "pytest",
            "wheel",
            "twine",
            "streamlit"
        ]
    }
)