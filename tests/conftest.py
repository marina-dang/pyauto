import sys
import os

def pytest_configure():
    # 获取项目根目录绝对路径
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)