from expenses.models import ExpenseAudit

# Here create class validation excute
class Auditing:
    def __init__(
                self,
                expense,
                request,
                action,
                note=None,
                ) -> None:
        
        self.expense = expense
        self.user = request.user
        self.action = action
        self.note = note
        self.is_checked = True
        self.create_auditing()

    def create_auditing(self) -> None:

        if self.action == "CREATED" or self.action == "DELETED":
            self.is_checked = False

        if self.action == "UPDATED":
            last_audit = self.expense.audits.order_by('-created_at').first()
            if not last_audit.is_checked:
                self.is_checked = False
            
        ExpenseAudit.objects.create(
            expense = self.expense,
            action=self.action,
            performed_by=self.user,
            status=self.expense.status,
            notes=self.note,
            is_checked=self.is_checked,
        )

        print(f'Foi salvo {self.is_checked} no banco')
