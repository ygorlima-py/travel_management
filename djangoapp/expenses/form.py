from django.core.exceptions import ValidationError
from django import forms
from expenses.models import Expenses 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class ExpenseForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False,
    )
    class Meta:
        model = Expenses
        fields = (
            'category',
            'supply',
            'state_uf',
            'city',
            'nf',
            'date',
            'amount',
            'value',
            'description',
            'picture',
        )

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        supply = cleaned_data.get('supply')
        state_uf = cleaned_data.get('state_uf')
        city = cleaned_data.get('city')
        date = cleaned_data.get('supply')
        amount = cleaned_data.get('amount')
        value = cleaned_data.get('value')
        description = cleaned_data.get('description')
        picture = cleaned_data.get('picture')

        if not category:
            self.add_error('category', 'A categoria é obrigatória.')
        if not supply:
            self.add_error('supply', 'O fornecedor é obrigatório.')
        if not state_uf:
            self.add_error('state_uf', 'O estado é obrigatório.')
        if not city:
            self.add_error('city', 'A cidade é obrigatória.')
        if not date:
            self.add_error('date', 'A data é obrigatória.')
        if not amount:
            self.add_error('amount', 'A quantidade é obrigatória.')
        if not value:
            self.add_error('value', 'O valor é obrigatório.')
        if not description:
            self.add_error('description', 'A descrição é obrigatória.')
        if not picture:
            self.add_error('picture', 'A imagem da nota é obrigatória.')

        return cleaned_data
                