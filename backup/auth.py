import os
from pathlib import Path

from google.oauth2.credentials import Credentials  # Representa credenciais OAuth (token de acesso)
from google_auth_oauthlib.flow import InstalledAppFlow  # Faz o fluxo OAuth (login + permissão)
from google.auth.transport.requests import Request  # Permite atualizar (refresh) o token quando expira

SCOPES = ["https://www.googleapis.com/auth/drive.file"]

BASE_DIR = Path(__file__).parent.parent / "secrets"

CREDENTIALS_FILE = BASE_DIR / "credentials.json"

TOKEN_FILE = BASE_DIR / "token.json"

def get_oauth_credentials() -> Credentials:

    """
    Essa função garante uma coisa:
    - se você já logou antes, ela reaproveita o token salvo (token.json)
    - se o token expirou, ela atualiza automaticamente
    - se nunca logou, ela abre o fluxo de login (OAuth) e salva o token
    """

    creds = None

    # 1) Se já existe o token é que ja foi autorizado
    # Carregamos este token para evitar logar de novo
    if Path(TOKEN_FILE).exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 2) Se não temos credenciais ou estão invalidas entramos aqui
    if not creds or not creds.valid:
        
        # 2.1) Se o token existe mas expirou, e tem refresh_token
        # Pedimos um token novo automaticamente sem fazer login novamente
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        
        # 2.2) Se não token valido realizamos o login
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES,
            )
    
            flow.redirect_uri = "http://localhost:8080"  # <- ADICIONE ESTA LINHA
            auth_url, _ = flow.authorization_url(prompt="consent")
            print("🔗 Abra este link no navegador ")
            print(auth_url)
            print(" Cole a URL da autorização aqui: ")
            code = input().strip()

            # Extrai o código da URL
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(code)
            code = parse_qs(parsed.query).get('code', [None])[0]
            
            if not code:
                raise ValueError("Código não encontrado na URL")
            
            flow.fetch_token(code=code)
            creds = flow.credentials

        with open(TOKEN_FILE, "w", encoding="utf-8") as token:
            token.write(creds.to_json())

    return creds


if __name__ == "__main__":
    get_oauth_credentials()