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
        "PyMySQL",
        "flask-session",
        "redis",
        "pika",
        "requests",
        "lxml",
        "cssselect",
        "html2text",
        "selenium",
        "cryptography",
        "opencv-python",# 这个库很难装
        "ffmpeg-python",
        "filetype",
        "pillow",
        "mingmq"
    ],
    entry_points = """
    [console_scripts]
    reborn = reborn.apps:main
    """
)
