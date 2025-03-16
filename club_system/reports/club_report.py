from datetime import datetime
from typing import Dict, Any
from club_system.models.club import Club
from club_system.models.employee import Player
class ClubReporter:
    @staticmethod
    def generate_overview(club: Club) -> str:
        """生成俱乐部概况报告"""
        report = [
            f"俱乐部名称: {club.name}",
            f"成立时间: {club.establish_date}",
            f"当前资金: ￥{club.funds:,.2f}",
            f"员工总数: {len(club.employees)} 人",
            "=" * 40
        ]
        return '\n'.join(report)

    @staticmethod
    def generate_team_analysis(club: Club) -> Dict[str, Any]:
        """生成球队能力分析报告"""
        analysis = {
            "total_ability": 0,
            "average_age": 0,
            "position_distribution": {},
            "injury_status": {
                "injured": 0,
                "healthy": 0
            }
        }

        age_total = 0
        for emp in club.employees:
            if isinstance(emp, Player):
                analysis["total_ability"] += emp.ability
                age_total += (datetime.now().year - int(emp.join_date[:4]))

                pos = emp.position if emp.position else "未指定"
                analysis["position_distribution"][pos] = analysis["position_distribution"].get(pos, 0) + 1

                if emp.injured:
                    analysis["injury_status"]["injured"] += 1
                else:
                    analysis["injury_status"]["healthy"] += 1

        if len(club.employees) > 0:
            analysis["average_age"] = age_total / len(club.employees)

        return analysis

    @classmethod
    def generate_full_report(cls, club: Club) -> str:
        """生成完整俱乐部报告"""
        overview = cls.generate_overview(club)
        analysis = cls.generate_team_analysis(club)

        report = [
            overview,
            "\n球队能力分析:",
            f"总能力值: {analysis['total_ability']}",
            f"平均年龄: {analysis['average_age']:.1f} 岁",
            "\n位置分布:"
        ]

        for pos, count in analysis["position_distribution"].items():
            report.append(f"- {pos}: {count}人")

        report.extend([
            "\n伤病情况:",
            f"受伤球员: {analysis['injury_status']['injured']}人",
            f"健康球员: {analysis['injury_status']['healthy']}人",
            f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        ])

        return '\n'.join(report)