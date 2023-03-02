from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='hyperDataS',
    version='1.0.0',
    description='hyperDataS (stands for HyperDataStorage) is a library written in Python used to store/retrieve complex data',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='AbdulWahab',
    author_email='jr.abdulwahab@gmail.com',
    url='https://github.com/AbdulWahab321/HyperDS',
    packages=['src/hyperDS'],
    install_requires=[
        "pyzipper"
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3',
)
