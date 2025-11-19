from io import BytesIO
from openpyxl import Workbook

class GenerateReports:
    def __init__(self, queryset) -> None:
        self.queryset = queryset
        self.related_keys = ['owner_expenses','category','state_uf',
                            'status', 'cycle']
    
    def generate_excel(self):
        wb = Workbook(write_only=True)
        sheet = wb.create_sheet(title='despesas')
        sheet.append([
                    'Usuário', 'Nome', 'Ciclo',
                    'Categoria da despesa', 'Fornecedor da despesa',
                    'Cidade', 'Estado', 'Numero da NF', 'Data e hora',
                    'Quantidade', 'Valor', 'Descriminação da despesa',
                    'Status'])
        
        for row in self.queryset.select_related(*self.related_keys):
            user = row.owner_expenses.username
            name = f'{row.owner_expenses.first_name} {row.owner_expenses.last_name}' 
            cycle = row.cycle.name if row.cycle else 'despesa sem ciclo'
            category = row.category.name
            supply = row.supply
            city = row.city
            state = row.state_uf.uf_name
            nf = row.nf if row.nf else ''
            date = row.date.replace(tzinfo=None) if row.date else ''
            amount = row.amount
            value = row.value
            description = row.description
            status = row.status.name
            
            expense = [user, name, cycle, category, supply, city, state, nf, 
                        date, amount, value, description, status]

            sheet.append(expense)

        stream = BytesIO()
        wb.save(stream)

        stream.seek(0)
        return stream
        