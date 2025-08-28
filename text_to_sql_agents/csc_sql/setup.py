from setuptools import find_packages, setup

VERSION = '0.0.1'


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def load_requirements(file_list=None):
    if file_list is None:
        file_list = ['requirements.txt']
    if isinstance(file_list, str):
        file_list = [file_list]
    requirements = []
    for file in file_list:
        with open(file, encoding="utf-8-sig") as f:
            lines = [line.strip() for line in f.readlines() if not line.startswith("#")]
            requirements.extend(lines)
    return requirements


def main():
    setup(
        name='cscsql',
        author='',
        version=VERSION,
        description="eval csc sql",
        long_description=readme(),
        long_description_content_type='text/markdown',
        keywords=["LLM", "NL2SQL", "SQL"],
        license='Apache License 2.0',
        url='https://github.com/CycloneBoy/csc_sql.git',
        download_url='',
        package_dir={"": "src"},
        python_requires=">=3.8.0",
        install_requires=load_requirements(),
        # extras_require=[],
        classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: OS Independent',
            'Natural Language :: Chinese (Simplified)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            "Topic :: Scientific/Engineering :: Artificial Intelligence",
        ],
    )


if __name__ == "__main__":
    main()
