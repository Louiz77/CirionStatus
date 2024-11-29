from flask import jsonify
from app.models.email_service import EmailService

def check_email():
    email_service = EmailService()
    try:
        email_service = EmailService()
        resultado = email_service.process_emails()
        emails = email_service.fetch_emails_from_sender()
        if not emails:
            return jsonify({"message": "Nenhum novo e-mail encontrado."}), 404

        return jsonify({"message": "Arquivo baixado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
