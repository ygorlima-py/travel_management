from expenses.models import AlertRecused
from django import forms

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
    