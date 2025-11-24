from django import forms
from expenses.models import Team, EnterPrise

# Form to create cycle
class CreateTeam(forms.ModelForm):

    name = forms.CharField(
                max_length=100,
                required=True,
                label='Nome do Equipe',
                widget=forms.TextInput(
                )
    )

    cost_center = forms.CharField(
                max_length=50,
                required=False,
                label='Centro de custo',
                help_text='Se houver centro de custo em sua equipe, adicione-o',
                widget=forms.TextInput(
                )
    )

    enterprise = forms.ModelChoiceField(
        queryset=EnterPrise.objects.none(),
        required=True,
        label='Empresa',
    )
    

    class Meta:
        model = Team
        fields = (
            'name',
            'cost_center',
            'enterprise',
        )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)      


        print(f'DEBUG - User recebido: {user}')

        # Filter enterprises exclusive log user  
        if user:
            from expenses.models import UserEnterpriseRole
            user_enterprises = UserEnterpriseRole.objects.filter(
                user=user,
                role__name='COMPANY_ADMIN',
            ).values_list('enterprise', flat=True)

            self.fields['enterprise'].queryset = EnterPrise.objects.filter(
                id__in=user_enterprises
            )