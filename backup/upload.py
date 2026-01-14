import os
from auth import get_oauth_credentials
from googleapiclient.discovery import build  # Cria o "cliente" pra falar com Google Drive
from googleapiclient.http import MediaFileUpload  

def upload_backup_drive(local_path: str, folder_id: str):

    creds = get_oauth_credentials()

    service = build("drive", "v3", credentials=creds)

    file_metadata = {
        "name": os.path.basename(local_path),
        "parents": [folder_id]
    }

    media = MediaFileUpload(local_path, resumable=True)

    created = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id,name,webViewLink",
    ).execute()

    return created
