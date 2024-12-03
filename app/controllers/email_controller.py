from flask import jsonify
from app.models.email_service import EmailService

def check_email():
    try:
        email_service = EmailService()
        resultado = email_service.process_emails()

        return jsonify({"message": "Arquivo baixado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
