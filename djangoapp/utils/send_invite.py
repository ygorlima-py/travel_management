from expenses.models import TeamInvite
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMessage

class SendInvite:
    def __init__(self, email, team_id) -> None:
        self.email = email
        self.team_id = team_id

    def create_url(self):
        self.invite = TeamInvite.objects.filter(
            email=self.email,
            team_id=self.team_id,
            ).first()
        
        token = self.invite.token # type: ignore
        url = reverse('expense:accept_invite', args=[token])
        link = f'{settings.SITE_URL}{url}'

        return link
    
    def create_template(self):
        link = self.create_url()

        # Render html:
        html_content = render_to_string(
            template_name='expenses/email/invite_template.html', 
            context={
                'invite': self.invite,
                'link': link,
            }
        )
        return html_content

    def send_invite(self):
        invite_html = self.create_template()

        email = EmailMessage(
            subject=f'Convite para entrar na equipe {self.invite.team.name}',
            body=invite_html,
            to=[self.email]
        )

        email.content_subtype = "html"
        email.send()

        return True

