import os
import sys

# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 将项目根目录添加到 Python 路径
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 打印 Python 路径以进行调试
print("Python Path:", sys.path)

# 使用绝对导入
from club_system.main import ClubSystem

if __name__ == "__main__":
    print("Starting Club Management System...")
    system = ClubSystem()
    system.start()