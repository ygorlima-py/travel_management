from django import forms
from expenses.models import UserProfile, State
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



# Form to update user
class UpdateFormUser(forms.ModelForm):
    
    first_name = forms.CharField(
        required=True,
        min_length=3,
        label='*Primeiro Nome',
        help_text='Obrigatório',
        error_messages={
            'min_length': 'O nome não pode ter menos de três letras.'
        }
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
        help_text='Obrigatório',
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@dominio.com'}),
        
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
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
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

    cost_center = forms.CharField(
        required=False,
        max_length=25,
        label='Centro de Custo',
    )

    fleet_number = forms.CharField(
        required=False,
        max_length=50,
        label='Numero da Frota',
    )

    bank = forms.CharField(
                    max_length=50,
                    required=False,
                    label="Banco",
                    help_text='Digite o nome do se banco',
                    widget = forms.TextInput(attrs={'placeholder': 'ex: Banco do Brasil'}),
        )

    agency = forms.CharField(
                    max_length=10,
                    required=False,
                    label="Agência",
                    help_text='Digite o número da agência com o digito separado pelo hifém',
                    widget=forms.TextInput(attrs={'placeholder': 'ex: 1234'}),
    )

    account = forms.CharField(
                required=False,
                label="Número da conta",
                help_text='Digite o número da conta com o digito separado pelo hifém',
                widget = forms.TextInput(attrs={'placeholder': 'ex: 12345-6'}),
    )

    account_type = forms.ChoiceField(
        choices= [('', '---------')] + UserProfile.ACCOUNT_CHOICES,
        required=False,
        label='Tipo de conta',
        help_text='Selecione o tipo de conta'
    )

    class Meta:
        model = User
        fields = (
        'first_name', 
        'last_name',
        'email',
        'username'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filling in the Profile field values ​​with the existing values.
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['phone'].initial = profile.phone
            self.fields['state_uf'].initial = profile.state_uf
            self.fields['city'].initial = profile.city
            self.fields['fleet_number'].initial = profile.fleet_number
            self.fields['bank'].initial = profile.bank
            self.fields['agency'].initial = profile.agency
            self.fields['account'].initial = profile.account

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)           
        password = cleaned_data.get('password1')
        
        if password:
            user.set_password(password)

        if commit:
            user.save()

        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.phone = cleaned_data.get('phone')
        profile.state_uf = cleaned_data.get('state_uf')
        profile.city = cleaned_data.get('city')
        profile.fleet_number = cleaned_data.get('fleet_number')
        profile.bank = cleaned_data.get('bank')
        profile.agency = cleaned_data.get('agency')
        profile.account = cleaned_data.get('account')
        profile.account_type = cleaned_data.get('account_type')
        
        if commit:
            profile.save()
            return user
    
    def clean(self):
        password1 = self.cleaned_data.get('password1') 
        password2 = self.cleaned_data.get('password2') 

        if password1 or password2:

            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('As senhas não correspondem')
                )

        return super().clean()

    # Validation E-mail
    def clean_email(self):
        email = self.cleaned_data.get('email') 
        current_email = self.instance.email 

        if current_email != email:
            if User.objects.filter(email=email).exists(): 
                self.add_error( 
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email
    
    # Validation Password
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1) 

            except ValidationError as errors: 
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )
        return password1

