"""
开发环境调试
"""
from reborn.apps import APP, main

if __name__ == '__main__':
    import platform
    if 'Linux' in platform.platform():
        main()
    else:
        APP.run(host='0.0.0.0', port=8000, debug=True)
