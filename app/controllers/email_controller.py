from flask import jsonify
from app.models.email_service import EmailService
from datetime import datetime

def check_email():
    try:
        email_service = EmailService()
        resultado = email_service.process_emails()
        print(resultado)
        with open("report.log", "a") as my_file:
            my_file.write(f"-{datetime.now()} | Error: {resultado}\n")
        emails = email_service.fetch_emails_from_sender()
        if not emails:
            return jsonify({"message": "Nenhum novo e-mail encontrado."}), 404

        return jsonify({"message": "Arquivo baixado com sucesso."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


with open("report.log", "a") as my_file:
    my_file.write(f"-{datetime.now()} | Error: {result}\n")