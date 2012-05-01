import os
from setuptools import setup, find_packages

setup(name='grokker',
      version = '0.1dev',
      description="A reformulation of Martian.",
      author="Martijn Faassen",
      author_email="faassen@startifact.com",
      license="BSD",
      packages=find_packages('grokker'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools'],
      extras_require = dict(
        test=['pytest >= 2.0'],
        ),
      entry_points="""
      # Add entry points here
      """,
      )
