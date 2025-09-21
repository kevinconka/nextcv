from skbuild import setup  # This line replaces 'from setuptools import setup'

setup(
    name="nextcv",
    description="Python-first computer vision library with C++ bdingings for speed.",
    use_scm_version=True,  # ← dynamic versioning
    setup_requires=["setuptools-scm"],  # ensures scm runs before build
    packages=["nextcv"],
    python_requires=">=3.6",
)
