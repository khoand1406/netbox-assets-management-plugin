from setuptools import setup, find_packages

setup(
    name="assets-management-plugin",
    version="0.1.0",
    description="NetBox plugin for asset and asset group management",
    author="Khoa Nguyen",
    author_email="nguyenkhoa14022002@gmail.com",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Framework :: Django :: 5.1",
        'Natural Language :: English',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    python_requires=">=3.12",
    
)