import shutil
import os
from pathlib import Path
from datetime import datetime
from upload import upload_backup_drive

BASE_DIR = Path(__file__).parent.parent.parent
BACKUP_DIR = BASE_DIR / "backups"
ZIP_DIR = BASE_DIR / "backup_zips"

def compress_file_backup():
    ZIP_DIR.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = str(ZIP_DIR / "backup_completo")  # sem .zip aqui
    zip_file = Path(base_name + ".zip")

    if zip_file.exists():
        zip_file.unlink()

    zip_path = shutil.make_archive(
        base_name=base_name+ts,
        format="zip",
        root_dir=str(BACKUP_DIR),   # o que vai ser zipado
    )
    
    print(f"✅ Zip criado em {zip_path}")

    upload_backup_drive(local_path=zip_path, folder_id="1ahvwLpHN6oOj3QCBFVjvxxsGvICVXC1C")
    
    try:
        os.remove(zip_path)
    except FileNotFoundError:
        print("Erro ao remover arquivo")

if __name__ == "__main__":
    compress_file_backup()