from django.core.exceptions import ValidationError
from django import forms
from expenses.models import Expenses 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


# Form to register expenses
class ExpenseForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*'
            }
        ),
        required=False,
    )

    date = forms.DateField(
        required=True,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S'],
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
        if not amount:
            self.add_error('amount', 'A quantidade é obrigatória.')
        if not value:
            self.add_error('value', 'O valor é obrigatório.')
        if not description:
            self.add_error('description', 'A descrição é obrigatória.')
        if not picture:
            self.add_error('picture', 'A imagem da nota é obrigatória.')

        return cleaned_data

# Form to register user                   
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        label='Primeiro Nome',
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
        label='Sobrenome',

    )

    email = forms.EmailField(
        required=True,
        label='E-mail',
    )

    username = forms.CharField(
        required=True,
        min_length=3,
        label='Usuário',
        help_text='Crie um usuário, não pode conter espaços. ' \
        'Apenas letas, numeros e simbolos $%&*@'
    )




    class Meta:
        model = User # Usamos o Objeto User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )


    # The clen_email method performs validation using an attribute inherited from the UserCreationForm class
    # UserCreationForm to retrieve the email value and then validate it using
    # User.objects.filter(email=email).exists():
    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Email já cadastrado', code='invalid')
            )

        return email
    