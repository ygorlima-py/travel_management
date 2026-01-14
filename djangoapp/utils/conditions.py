from expenses.models import Cycle

class Conditions:
    def __init__(self, expense) -> None:
        self.expense = expense
        self.owner_cycle = self.expense.owner_expenses
        self.verify_status = self._verify_status()
        self.verify_date = self._verify_date()

    def _verify_status(self):
        cycle = Cycle.objects.filter(
            owner_id=self.owner_cycle,
            is_open=True,
            save_expense_auto=True,
            ).first()
        
        return cycle
    
    def _verify_date(self):
        cycle = self.verify_status

        if cycle is None:
            return None
        
        # date() converte datetime para date
        expense_date = self.expense.date.date()
        
        if cycle.initial_date <= expense_date <= cycle.end_date:
            return cycle.pk
        
        else:
            return None

    def verify(self):
        return self.verify_date
    