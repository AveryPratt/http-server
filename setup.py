"""Setup configuration"""


from setuptools import setup


setup(
    name="katas",
    description="Echo server",
    version=0.1,
    author="Avery Pratt",
    author_email="apratt91@gmail.com",
    license="MIT",
    package_dir={'': 'src'},
    py_modules=["client", "server"],
    extras_require={
        "test": ["pytest"]
    },
)
