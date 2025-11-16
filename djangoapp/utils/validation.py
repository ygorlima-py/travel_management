from expenses.models import Cycle, Expenses

class Validation:
    def __init__(
            self, 
            initial_date=None,
            end_date=None,
            initial_km=None,
            end_km=None
            ) -> None:
        
        self.initial_date = initial_date
        self.end_date = end_date
        self.initial_km = initial_km
        self.end_km = end_km
        
        self.validate_date = self._validate_date()
        self.validate_km = self._validate_km()

    def _validate_date(self):
        errors = []

        if self.end_date and self.initial_date is not None:
            if self.end_date < self.initial_date:
                errors.append('A data final não pode ser menor que a inicial') 
            
        return errors
    
    def _validate_km(self):
        errors = []

        if self.end_km and self.initial_km is not None:
            if self.end_km < self.initial_km:
                errors.append('A kilometragem final deve ser maior que a inicial')

        elif self.end_km is None and self.initial_km is not None: 
            errors.append('Adicione a Kilometragem Final')

        elif self.end_km is not None and self.initial_km is None: 
            errors.append('Adicione a Kilometragem Inicial')

        return errors
    
    