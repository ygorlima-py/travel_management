from expenses.models import TeamInvite
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage

class SendInvite:
    def __init__(self, email, team_id) -> None:
        self.email = email
        self.team_id = team_id

    def create_url(self):
        invite = TeamInvite.objects.filter(
            email=self.email,
            team_id=self.team_id,
            ).first()
        
        token = invite.token # type: ignore
        url = reverse('expense:accept_invite', args=[token])
        link = f'{settings.SITE_URL}{url}'

        return link
        

    def send_invite(self):
        link = self.create_url()

        email = EmailMessage(
            subject='Você foi convidado para entrar em uma equipe',
            body=f"Clique no link {link} para entrar na equipe",
            to=[self.email]
        )
        email.send()

        return True

