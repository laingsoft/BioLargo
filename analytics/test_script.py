from accounts.models import Company
from .base_analysis import EquationTool

exp = [1, 2]
equations = ["log('StockCFU [CFU/mL]') / log('RemainingCFU [CFU/mL]') * 100"]


def test():
    company = Company.objects.get(pk=1)
    tool = EquationTool(company=company, experiments=exp, equations=equations)
    return tool.evaluate()
