from club_system.models.club import Club
from club_system.models.employee import Role
from typing import Dict, List
class FinanceSystem:
    @staticmethod
    def calculate_financials(club: Club) -> Dict:
        total_salary = sum(e.salary for e in club.employees)
        return {
            "total_income": club.funds,
            "total_expenses": total_salary,
            "net_profit": club.funds - total_salary,
            "salary_breakdown": {
                "players": sum(e.salary for e in club.employees if e.role == Role.PLAYER),
                "coaches": sum(e.salary for e in club.employees if e.role == Role.COACH)
            }
        }

    def generate_salary_recommendations(self, club: Club) -> List[Dict]:
        recommendations = []
        market_avg = 50000  # 示例值

        for emp in club.employees:
            if emp.salary < market_avg * 0.8:
                recommendations.append({
                    "eid": emp.eid,
                    "name": emp.name,
                    "current": emp.salary,
                    "recommended": market_avg,
                    "reason": "低于市场平均水平"
                })

        return recommendations