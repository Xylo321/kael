from setuptools import find_packages, setup

setup(
    name='reborn',
    version='2.0.1',
    url='',
    license='',
    maintainer='zswj123',
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
        "gevent"
    ],
    entry_points = """
    [console_scripts]
    reborn = reborn.apps:main
    delete_category_consumer = reborn.mmq.delete_category:main
    """
)
