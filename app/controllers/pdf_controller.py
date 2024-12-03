from flask import jsonify, send_file
from app.models.pdf_service import BackupReportGenerator
import os
import uuid
def generate_pdf():
    try:
        id_user_uuid = str(uuid.uuid4())
        data_folder = os.path.abspath("./data")
        output_folder = os.path.abspath("./upload")
        os.makedirs(output_folder, exist_ok=True)

        output_pdf = os.path.join(output_folder, f"{id_user_uuid}_relatorio_backup.pdf")

        report_generator = BackupReportGenerator(data_folder)
        report_generator.process_and_generate_report(output_pdf)

        return send_file(
            output_pdf,
            as_attachment=True,
            download_name=f"{id_user_uuid}_relatorio_backup.pdf"
        )
    except Exception as e:
        print(f"Erro ao gerar o relatório: {e}")
        return jsonify({"error": f"Erro ao gerar o PDF: {str(e)}"}), 500
