from club_system.services.finance import FinanceSystem
from datetime import datetime
from club_system.models.club import Club
class SalaryReporter:
    @staticmethod
    def generate_report(club) -> str:
        financials = FinanceSystem().calculate_financials(club)
        recommendations = FinanceSystem().generate_salary_recommendations(club)

        report = [
            f"薪资报告 - {datetime.now().strftime('%Y-%m-%d')}",
            "=" * 40,
            f"总资金: {financials['total_income']}",
            f"总薪资支出: {financials['total_expenses']}",
            f"净收益: {financials['net_profit']}",
            "\n薪资构成:",
            f"- 球员: {financials['salary_breakdown']['players']}",
            f"- 教练: {financials['salary_breakdown']['coaches']}",
            "\n薪资建议:"
        ]

        for rec in recommendations:
            report.append(
                f"{rec['name']} ({rec['eid']}): {rec['current']} → {rec['recommended']}"
            )

        return '\n'.join(report)