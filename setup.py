from setuptools import setup, find_packages

setup(
    name="ATLAS",
    version="0.0.1",
    packages=find_packages(),
    url="https://vivecenter.berkeley.edu/",
    license="",
    author="FHL Vive Center",
    author_email="wuxiaohua1011@berkeley.edu",
    description="PointCloud Annotation and Segmentation Tool",
    include_package_data=True,
    package_data={
            # If any package contains the following, include them:
        '': ['*.config', '*.xml', '*.ini'],
    }
)
