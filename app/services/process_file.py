import pandas as pd
import os
import csv
import re
from datetime import datetime

def get_latest_file(folder):
    """
    Retorna o arquivo mais recente na pasta, com base na data extraída do nome do arquivo.
    """
    try:
        # Listar todos os arquivos CSV no diretório
        files = [f for f in os.listdir(folder) if f.endswith('.CSV')]
        
        if not files:
            return {"error": "Nenhum arquivo de backup encontrado"}

        def extract_date_from_filename(filename):
            """
            Extrai a data do nome do arquivo no formato OpsCenter_ITFACIL_-_Resultado_Analitico_de_Backup_DD_MM_YYYY_...
            """
            match = re.search(r'(\d{2}_\d{2}_\d{4})', filename)
            if match:
                return datetime.strptime(match.group(1), "%d_%m_%Y")
            return None

        # Ordenar arquivos pela data extraída
        files.sort(
            key=lambda f: extract_date_from_filename(f),
            reverse=True  # Ordem decrescente
        )

        latest_file = os.path.join(folder, files[0])
        return latest_file

    except Exception as e:
        return {"error": f"Erro ao obter o último arquivo: {str(e)}"}

def process_backup_file():
    folder = './data'
    files = sorted([f for f in os.listdir(folder) if f.endswith('.CSV')], reverse=True)

    if not files:
        return {"error": "Nenhum arquivo de backup encontrado"}

    latest_file = get_latest_file(folder)
    print(f"Processando arquivo: {latest_file}")

    try:
        # Detectar o delimitador automaticamente
        with open(latest_file, 'r', encoding='utf-8') as f:
            sample = f.read(2048)
            sniffer = csv.Sniffer()
            delimiter = sniffer.sniff(sample).delimiter
            print(f"Delimitador detectado: {delimiter}")

        # Carregar o arquivo ignorando as 4 primeiras linhas
        try:
            df = pd.read_csv(
                latest_file,
                delimiter=delimiter,
                encoding='utf-8',
                skiprows=4,  # Ignorar as 4 primeiras linhas
                on_bad_lines='skip',
                names=[
                    "Nome do Job", "Nome do Servidor", "Status do Backup",
                    "Inicio do Backup", "Final do Backup", "Volume Protegido (GB)",
                    "Tipo de Backup", "Nome do Agendamento"
                ]
            )
        except pd.errors.ParserError as e:
            print(f"Erro ao processar o arquivo: {str(e)}")
            return {"error": "Arquivo contém linhas mal formatadas e não pôde ser processado completamente"}

        # Processar resumo (contagem de status)
        status_count = df["Status do Backup"].value_counts().to_dict()
        summary = {
            "Successful": status_count.get('Successful', 0),
            "Error": status_count.get('Error', 0),
            "Partially": status_count.get('Partially Successful', 0)

        }

        # Processar detalhes
        details = df.to_dict(orient='records')

        date_process = df["Nome do Job"]
        for x in date_process:
            if "Report generated on" in x:
                date = x
        print(date)
        return {"summary": summary, "details": details, "date": date}

    except Exception as e:
        return {"error": f"Erro ao processar o arquivo: {str(e)}"}
