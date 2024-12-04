from flask import jsonify
from app.models.email_service import EmailService
from app.services.registrar_log import logger

def check_email():
    try:
        logger("Usuario requisitou ATUALIZACAO NA PLANILHA ")
        email_service = EmailService()
        resultado = email_service.process_emails()

        return jsonify({"message": "Arquivo baixado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
