from flask import Blueprint, jsonify
from app.services.process_file import process_backup_file
import pandas as pd
from app.controllers.email_controller import check_email
from datetime import datetime

bp = Blueprint('backup', __name__)

@bp.route('/backup/check', methods=['GET'])
def fetch_email():
    return check_email()

@bp.route('/backup/status', methods=['GET'])
def get_backup_status():
    try:
        # Processar o arquivo e obter dados
        result = process_backup_file()

        if "error" in result:
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | Error: {result}\n")
            return jsonify({"error": result["error"]}), 400

        # Substituir NaN, -inf e inf nos detalhes
        for record in result['details']:
            for key, value in record.items():
                if pd.isna(value) or value in [float('inf'), float('-inf')]:
                    record[key] = None
        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Erro ao processar o backup: {str(e)}"}), 500
