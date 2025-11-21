from django import forms
from utils.validation import Validation # type: ignore
from expenses.models import EnterPrise, Plan

# Form to create cycle
class EnterpriseRegisterForm(forms.ModelForm):
    
    name = forms.CharField(
                max_length=50,
                required=True,
                label='Nome da Empresa',
    )
    
    cnpj = forms.CharField(
                required=True,
                label='CNPJ: ',
            )

    plan_type = forms.ModelChoiceField(
        queryset=Plan.objects.all(),
        required=True,
        label='* Selecione o plano',
        help_text='Selecione o Plano de assinatura',
    )
    
    class Meta:
        model = EnterPrise
        fields = [
            'name', 'cnpj', 'plan_type',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)      

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        cnpj = cleaned_data.get('cnpj')
        plan_type = cleaned_data.get('plan_type')
        

        if not name:
            self.add_error('name', 'O nome da empresa é obrigatório.')
        if not cnpj:
            self.add_error('cnpj', 'O CNPJ é obrigatório.')
        if not plan_type:
            self.add_error('plan_type', 'O plano é obrigatório.')

        return cleaned_data
    
        
    
