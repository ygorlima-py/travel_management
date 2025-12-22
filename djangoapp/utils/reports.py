from io import BytesIO
from openpyxl import Workbook
from django.db.models import Prefetch
from expenses.models import ExpenseAudit

class GenerateReports:
    def __init__(self, queryset) -> None:
        self.queryset = queryset
        self.related_keys = ['owner_expenses','category','state_uf',
                            'status', 'cycle']
    
    def generate_excel(self):
        wb = Workbook(write_only=True)
        sheet = wb.create_sheet(title='despesas')
        sheet.append([
                    'Número da despesa', 'Empresa', 'Equipe', 'Solicitante', 'Ciclo',
                    'Data da despesa', 'Data de lançamento',
                    'Categoria da despesa', 'Fornecedor da despesa',
                    'Cidade', 'Estado', 'Numero da NF', 
                    'Quantidade', 'Valor', 'Descriminação da despesa',
                    'Status', 'Aprovado/Recusado por', 'Data Aprovação/Recusa', 
                    'Observação',
                    ])
        
        queryset_optimized = self.queryset.select_related(*self.related_keys).prefetch_related(
            Prefetch(
                'audits',
                queryset=ExpenseAudit.objects.filter(
                    action__in=['APPROVED', 'REJECTED']
                ).select_related('performed_by').order_by('-created_at'),
                to_attr='approval_audits'
            )
        ).order_by('-created_at')
        
        for row in queryset_optimized:
            _id = row.pk
            enterprise = row.enterprise.name if row.enterprise else '-'
            team = row.owner_expenses.profile.team.name if row.owner_expenses.profile.team else '-'
            name = f'{row.owner_expenses.first_name} {row.owner_expenses.last_name}' 
            cycle = row.cycle.name if row.cycle else '-'
            date = row.date.strftime('%d/%m/%Y %H:%M') if row.date else '-'
            created_at = row.created_at.strftime('%d/%m/%Y %H:%M')
            category = row.category.name
            supply = row.supply
            city = row.city
            state = row.state_uf.uf_name
            nf = row.nf if row.nf else ''
            amount = row.amount
            value = row.value
            description = row.description
            status = row.status.name

            last_audit = row.approval_audits[0] if row.approval_audits else None

            performed_by = (
                f'{last_audit.performed_by.first_name} {last_audit.performed_by.last_name}'
                if last_audit and last_audit.performed_by
                else '-'
            )
            date_audit = (
                last_audit.created_at.strftime('%d/%m/%Y %H:%M')
                if last_audit and last_audit.created_at 
                else '-'
                )
            note = (
                    last_audit.notes.message 
                    if last_audit and last_audit.notes and last_audit.notes.message
                    else '-'
                    )

            expense = [_id, enterprise, team, name, cycle, date, created_at, 
                        category, supply, city, state, nf, amount, value,
                        description, status, performed_by, date_audit, note
                        ]

            sheet.append(expense)

        stream = BytesIO()
        wb.save(stream)

        stream.seek(0)
        return stream
        