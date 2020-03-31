from setuptools import find_packages, setup

setup(
    name='reborn',
    version='1.0.0',
    url='https://github.com/zswj123/reborn',
    license='',
    maintainer='zswj123',
    maintainer_email='l2se@sina.cn',
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
    """
)
