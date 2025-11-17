from django.db.models import Sum

class Calculation:
    def __init__(self, cycle, expenses) -> None:
        self.cycle = cycle
        self.expenses = expenses
        self.distance = self._distance()
        self.total_fuel = self._total_fuel()
        self.fuel_consumption = self._fuel_consumption()
        self.amount_expenses = self._amount_expenses()
        self.amount_expenses_approved = self._amount_approved_expenses()
        self.total_value = self._total_value()
        
    def _distance(self):
        initial_km = self.cycle.initial_km
        end_km = self.cycle.end_km
        return end_km - initial_km
    
    def _total_fuel(self):
        total_fuel = self.expenses.filter(category__name='COMBUSTÍVEL').aggregate(total=Sum('amount'))
        round_total = total_fuel['total']
        if round_total is None:
            return None
        return round(round_total, 2)
    
    def _fuel_consumption(self):
        total_fuel = self.total_fuel
        if total_fuel is None:
            return None
        else:
            fuel_consumption = self.distance / total_fuel
            return round(fuel_consumption, 2)
        
    def _amount_expenses(self):
        return self.expenses.count()
    
    def _amount_approved_expenses(self):
        total_expenses_approved = self.expenses.filter(status__name='APROVADO').count()
        return total_expenses_approved
    
    def _total_value(self):
        total_value = self.expenses.aggregate(total=Sum('value'))
        if total_value['total'] is None:
            return 0
        return total_value['total']

    def all(self):
        return dict(
            distance=self.distance,
            total_fuel=self.total_fuel,
            fuel_consumption=self.fuel_consumption,
            amount_expenses=self.amount_expenses,
            amount_expenses_approved=self.amount_expenses_approved,
            total_value=self.total_value,
        )
    


