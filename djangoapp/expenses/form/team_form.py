from django import forms
from expenses.models import Team, EnterPrise, TeamInvite
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()
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

class TeamInviteForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label='Email do Membro',
        help_text='Digite o email da pessoa que deseja convidar',
        widget=forms.EmailInput(attrs={
            'placeholder': 'membro@exemplo.com',
            
            })

    )

    class Meta:
        model = TeamInvite
        fields = ['email']

    def __init__(self, *args, team=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.team = team

    def clean_email(self):
        email = self.cleaned_data.get('email').lower().strip() # type:ignore

        if not self.team:
            raise ValidationError('Equipe não especificada')
        
        # check if exists invite to this member
        existing_invite = TeamInvite.objects.filter(
            team=self.team,
            email=email,
            accepted=False,
        ).exists()

        if existing_invite:
            raise ValidationError('Existe um convite pendente para este usuário')
        
        # check if member is already on the team
        if User.objects.filter(email=email, profile__team=self.team).exists():
            raise ValidationError('Este membro já está na equipe.')

        return email