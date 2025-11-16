from django.core.exceptions import ValidationError
from django import forms
from expenses.models import Expenses, UserProfile, State, AlertRecused, Cycle, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from utils.validation import Validation # type: ignore


# Form to create expense
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
            'placeholder': 'Exemplo: Ribeirão Preto'
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
        profile.cost_center = cleaned_data.get('cost_center')
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

# Form to alert    
class AlertRecusedForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
                'maxlength': 40,
                'rows': 1,
                'cols': 10,
                }),
        min_length=1,
        help_text='Máximo de 40 caractere',
        label='*Obrigatório'
        )
    
    class Meta:
        model = AlertRecused
        fields = ('message',)
    
# Form to create cycle
class CreateCycle(forms.ModelForm):
    
    name = forms.CharField(
                max_length=50,
                required=True,
                label='Nome do Ciclo',
                widget=forms.TextInput(
                    attrs={
                        'placeholder': 'Ex: Setembro',
                    }
                )
    )
    initial_date = forms.DateField(
                required=True,
                label='Defina a data Inicial do ciclo',
                widget=forms.DateInput(
                    attrs={
                        'placeholder': 'Ex: 01/09/2025',
                        'type': 'date',
                    }
                ),
    )
    end_date = forms.DateField(
                required=True,
                label='Data final do seu ciclo',
                widget=forms.DateInput(
                    attrs={
                        'placeholder': 'Ex: 30/09/2025',
                        'type': 'date',
                    }
                ),
    )
    initial_km = forms.IntegerField(
                required=False,
                label='Coloque o Km inicial do veículo neste cíclo',
                widget=forms.NumberInput(
                attrs={
                    "placeholder": "Ex: 45500",
                }
            ),
    )
    end_km = forms.IntegerField(
                required=False,
                label='Coloque o Km final do veículo neste cíclo',
                widget=forms.NumberInput(
                attrs={
                    "placeholder": "Ex: 50500",
                }
            )
    )

    save_expense_auto = forms.BooleanField(
            required=False,
            widget=forms.CheckboxInput(
                attrs={
                    'class': 'custom-chackbox',
                }
            ),
            label="Mover todas as despesas incluidas neste periodo para o ciclo",
            help_text="Selecionando esta opção todas as despesas feitas no " \
            "periodo selecionado serão salvas automaticamente neste ciclo"
    )

    class Meta:
        model = Cycle
        fields = (
            'name',
            'initial_date',
            'end_date',
            'initial_km',
            'end_km',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      

    def clean(self):
        cleaned_data = super().clean()

        initial_date = cleaned_data.get('initial_date')
        end_date = cleaned_data.get('end_date')
        initial_km = cleaned_data.get('initial_km')
        end_km = cleaned_data.get('end_km')

        validator = Validation(
            initial_date,
            end_date,
            initial_km,
            end_km,
            )

        if validator.validate_date:
            raise forms.ValidationError(validator.validate_date)
        
        if validator.validate_km:
            raise forms.ValidationError(validator.validate_km)