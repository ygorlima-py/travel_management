from django.core.exceptions import ValidationError
from django import forms
from expenses.models import Expenses, UserProfile, State 
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

    date = forms.DateTimeField(
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
            self.add_error('city', 'A data é obrigatória.')
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
        model = User 
        fields = (
            'first_name', 'last_name', 'email',
            'username',
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
    
        
            
