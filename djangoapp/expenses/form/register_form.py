from django.core.exceptions import ValidationError
from expenses.models import UserProfile, State 
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

# Form to register user                   
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
        label='*Primeiro Nome',
        help_text='Obrigatório'
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
        label='*Sobrenome',
        help_text='Obrigatório'

    )

    email = forms.EmailField(
        required=True,
        label='*E-mail',
        help_text='Obrigatório'
    )

    username = forms.CharField(
        required=True,
        min_length=3,
        label='*Usuário',
        help_text='(Obrigatório) Crie um usuário, não pode conter espaços. ' \
        'Apenas letas, numeros e simbolos $%&*@'
    )

    phone = forms.CharField(
        required=False,
        max_length=15,
        label='Celular',
    )

    state_uf = forms.ModelChoiceField(
        queryset=State.objects.all(),
        required=False,
        label='Estado',
        empty_label='Selecione o  Estado'
    )

    city = forms.CharField(
        required=False,
        max_length=50,
        label='Cidade',
    )

    fleet_number = forms.CharField(
        required=False,
        max_length=50,
        label='Numero da Frota',
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
    
    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone'),
                state_uf=self.cleaned_data.get('state_uf'),
                city=self.cleaned_data.get('city'),
                fleet_number=self.cleaned_data.get('fleet_number'),
            )    
        return user
    