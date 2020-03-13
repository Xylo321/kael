"""
开发环境调试
"""
from reborn.apps import APP

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8000, debug=True)
