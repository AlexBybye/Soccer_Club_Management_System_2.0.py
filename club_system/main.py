# 程序主入口
from datetime import datetime
from models.club import Club
from models.emplyee import Employee, Player, Role
from services.storage import ClubStorage
from utils.security import generate_secure_key, hash_key, verify_key


class ClubSystem:
    def __init__(self):
        self.current_club = None

    def start(self):
        """主菜单入口"""
        while True:
            print("\n=== 俱乐部管理系统 ===")
            print("1. 创建新俱乐部")
            print("2. 登录现有俱乐部")
            print("3. 退出系统")

            choice = input("请选择操作: ")

            try:
                if choice == '1':
                    self.create_club_flow()
                elif choice == '2':
                    self.login_flow()
                elif choice == '3':
                    print("感谢使用，再见！")
                    break
                else:
                    print("无效输入，请重新选择")
            except Exception as e:
                print(f"发生错误：{e}")

    def create_club_flow(self):
        """创建俱乐部流程"""
        try:
            name = input("俱乐部名称: ")
            funds = float(input("初始资金: "))

            # 生成安全密钥
            raw_key = generate_secure_key()
            hashed_key = hash_key(raw_key)

            # 创建俱乐部实例
            club = Club(
                name=name,
                funds=funds,
                director_key=hashed_key
            )

            # 添加初始董事账户
            club.add_employee(Employee(
                eid="DIR-001",
                name="系统管理员",
                salary=0,
                role=Role.DIRECTOR,
                join_date=datetime.now().strftime("%Y-%m-%d")
            ))

            ClubStorage.save(club)
            print(f"\n=== 俱乐部创建成功 ===")
            print(f"董事密钥: {raw_key}（请妥善保管）")
        except ValueError as e:
            print(f"输入错误：{e}")
        except Exception as e:
            print(f"创建俱乐部失败：{e}")

    def login_flow(self):
        """登录流程"""
        name = input("俱乐部名称: ")
        input_key = input("董事密钥: ")

        club = ClubStorage.load(name)
        if not club:
            print("俱乐部不存在")
            return

        if not verify_key(club.director_key, input_key):
            print("密钥验证失败")
            return

        self.current_club = club
        self.manage_club()

    def manage_club(self):
        """俱乐部管理菜单"""
        while True:
            print(f"\n=== {self.current_club.name}管理 ===")
            print(f"当前资金: {self.current_club.funds}")
            print("1. 添加员工")
            print("2. 查看员工")
            print("3. 返回上级")

            choice = input("请选择操作: ")

            if choice == '1':
                self.add_employee()
            elif choice == '2':
                self.list_employees()
            elif choice == '3':
                break
            else:
                print("无效输入，请重新选择")

    def add_employee(self):
        """添加员工流程"""
        try:
            role = Role(input("角色 (director/coach/player/staff): "))
            eid = input("员工编号: ")
            name = input("姓名: ")
            salary = float(input("年薪: "))
            join_date = datetime.now().strftime("%Y-%m-%d")

            if role == Role.PLAYER:
                specialty = input("球员特长: ")
                employee = Player(
                    eid=eid,
                    name=name,
                    salary=salary,
                    role=role,
                    specialty=specialty,
                    join_date=join_date
                )
            else:
                employee = Employee(
                    eid=eid,
                    name=name,
                    salary=salary,
                    role=role,
                    join_date=join_date
                )

            self.current_club.add_employee(employee)
            ClubStorage.save(self.current_club)
            print("员工添加成功")

        except ValueError as e:
            print(f"输入错误: {e}")

    def list_employees(self):
        """列出员工"""
        print("\n=== 员工列表 ===")
        for emp in self.current_club.employees:
            info = f"{emp.eid} | {emp.name} | {emp.role.value}"
            if isinstance(emp, Player):
                info += f" | 特长: {emp.specialty}"
            print(info)


if __name__ == "__main__":
    system = ClubSystem()
    system.start()

# 使用说明
# 所有数据模型均使用Python dataclasses实现
#
# 业务逻辑封装在services模块
#
# 数据存储采用JSON格式，路径符合规范
#
# 安全相关操作使用utils.security模块
#
# 输入验证使用utils.validators
#
# 建议按以下顺序进行功能测试：
#
# 俱乐部创建与密钥验证
#
# 用户账户的创建与登录
#
# 员工管理系统操作
#
# 财务报告生成
#
# 训练系统模拟
#
# 每个模块都已实现基础功能，后续可根据需求逐步添加以下扩展：
#
# 权限控制系统装饰器
#
# 训练效果可视化
#
# 意见箱的加密存储
#
# API接口层
#
# 数据库迁移功能
