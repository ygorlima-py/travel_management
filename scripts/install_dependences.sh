#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

# Create Environment
python3 -m venv venv

# Activate environment
. venv/bin/activate 

echo " ✅ Ambiente virtual criado e acionado"

pip install -r requirements.txt

