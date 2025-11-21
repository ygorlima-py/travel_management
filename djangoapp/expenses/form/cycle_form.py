from django import forms
from expenses.models import Cycle
from utils.validation import Validation # type: ignore

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
        
    


        