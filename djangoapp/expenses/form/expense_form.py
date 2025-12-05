# Form to create expense
from django import forms
from expenses.models import Expenses, State, Category

class ExpenseForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label='* Categoria',
        help_text='Selecione a categoria a qual a despesa pertence',
    )

    supply = forms.CharField(
        required=True,
        label='* Fornecedor da despesa',
        help_text='Adicione o nome ou razão social do fornecedor da despesa',
        widget=forms.TextInput(attrs={
            'placeholder': 'Exemplo: Restaurante Bom Sabor'
        })
    )

    state_uf = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=True,
        label='* Selecione o estado',
        help_text='Selecione o estado que a despesa foi realizada',
    )

    city = forms.CharField(
        required=True,
        label='* Cidade',
        help_text='Digite o nome da cidade que a despesa foi realizada',
        widget=forms.TextInput(attrs={
            'placeholder': 'Exemplo: Ribeirão Preto',
        }),
    )

    nf = forms.CharField(
        required=False,
        label='Numero da Nota Fiscal',
        help_text='Digite o numero da nota fiscal, caso não possua, ignore esse campo'
    )

    amount = forms.FloatField(
        required=True,
        label='* Quantidade',
        help_text='Digite a quantidade que foi consumida nesta despesa'
    )

    value = forms.DecimalField(
        required=True,
        label='* Valor da despesa',
        help_text='Digite o valor total desta despesa'
    )

    description = forms.CharField(
        required=True,
        label='Descrição da Despesa',
        help_text="Adicione a descrição da despesa",
        widget=forms.Textarea(attrs={
            'placeholder': 'Exemplo 2 diarias de hospedagem',
            'rows': 4,
            'cols': 10,
        })
    )

    date = forms.DateTimeField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S'],
        label='* Data da despesa',
        help_text='Adicione a data da despesa',
        )
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False,
        label="Adicione a foto da nota fiscal ou comprovante da despesa"
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        if self.instance and self.instance.pk and self.instance.date :
            self.initial['date'] = self.instance.date.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        supply = cleaned_data.get('supply')
        state_uf = cleaned_data.get('state_uf')
        city = cleaned_data.get('city')
        date = cleaned_data.get('date')
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
    
