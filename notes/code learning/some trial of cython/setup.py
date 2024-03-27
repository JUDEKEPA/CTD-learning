from setuptools import setup, Extension
from Cython.Build import cythonize

# Define the extension module
extensions = [
    Extension(
        name="phase_record",  # Name of the module
        sources=["/Users/zhengdiliu/SEU/LCM/CTD-learning/notes/code learning/some trial of cython/phase_record.pyx"],  # Path to the pyx file
        language='c',  # Specify the language, optional
    )
]

# Use cythonize on the extensions
setup(
    ext_modules=cythonize(extensions, language_level=3),
)
