from setuptools import find_packages, setup

setup(
    name='kael',
    version='2.0.5',
    url='',
    license='',
    maintainer='kael',
    maintainer_email='congshi.hello@gmail.com',
    description='',
    long_description='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-session",
        "redis",
        "html2text",
        "cryptography",
        "opencv-python",
        "ffmpeg-python",
        "filetype",
        "pillow",
        "PyMySQL",
        "gevent",
        "tornado",
        "paramiko"
    ],
    entry_points = """
    [console_scripts]
    kael = kael.apps:main
    delete_category_consumer = kael.mmq.delete_category:main
    delete_file_by_category_consumer = kael.mmq.delete_file_by_category:main
    wssh = kael.webssh.main:main
    """
)
