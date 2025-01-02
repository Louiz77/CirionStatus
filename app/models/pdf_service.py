import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from app.services.chart_service import ChartService
from app.services.registrar_log import logger
class BackupReportGenerator:
    def __init__(self, data_folder):
        self.data_folder = data_folder
        self.chart_service = ChartService()

    def get_latest_files(self, n=5):
        """
        Recupera os N arquivos CSV mais recentes do diretório
        """
        files = [f for f in os.listdir(self.data_folder) if f.endswith('.CSV')]
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(self.data_folder, x)), reverse=True)
        return files[:n]

    def extract_date_from_filename(self, filename):
        """
        Extrai a data de geração do arquivo a partir do nome do arquivo
        """
        try:
            parts = filename.split('_')
            date_part = '_'.join(parts[7:-6])  # Extrai a data
            file_date = datetime.strptime(date_part, "%d_%m_%Y")
            return file_date
        except Exception as e:
            logger(f"Erro ao extrair a data do arquivo {filename}: {e}")
            return None

    def load_csv_data(self, file_path, file_date):
        """
        Carrega os dados do CSV e adiciona a data de geração.
        """
        try:
            df = pd.read_csv(
                file_path,
                delimiter=',',
                encoding='utf-8',
                skiprows=4,  # Ignorar as 4 primeiras linhas
                on_bad_lines='skip',
                names=[
                    "Nome do Job", "Nome do Servidor", "Status do Backup",
                    "Inicio do Backup", "Final do Backup", "Volume Protegido (GB)",
                    "Tipo de Backup", "Nome do Agendamento"
                ]
            )
            df['Data de Geração'] = file_date
            logger(f"{file_path} Arquivo Processado!")
            status_count = df["Status do Backup"].value_counts().to_dict()
            summary = {
                "Successful": status_count.get('Successful', 0),
                "Error": status_count.get('Failed', 0),
                "Partially": status_count.get('Partially Successful', 0)

            }
            return df
        except Exception as e:
            logger(f"Erro ao processar {file_path}: {e}")
            return pd.DataFrame()

    def generate_summary(self, dataframes):
        """
        Gera um resumo consolidado dos últimos arquivos de backup.
        """
        summaries = []
        for df in dataframes:
            summary = {
                "Data": df['Data de Geração'].iloc[0],
                "Successful": (df['Status do Backup'] == 'Successful').sum(),
                "Error": (df['Status do Backup'] == 'Failed').sum(),
                "Partially Successful": (df['Status do Backup'] == 'Partially Successful').sum(),
            }
            summaries.append(summary)
        return pd.DataFrame(summaries)

    def generate_pdf_report(self, summary_df, output_path):
        """
        Gera um relatório PDF a partir do resumo consolidado.
        """
        data_atual = datetime.now().strftime("%d/%m/%Y")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=25)

        pdf.cell(200, 10, txt="Relatório de Status de Backup - Comparativo", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.ln(10)

        # Adicionar resumo geral
        for index, row in summary_df.iterrows():
            pdf.cell(200, 10, txt=f"Data: {row['Data']:%d/%m/%Y}", ln=True)
            pdf.cell(200, 10, txt=f"Backups com Sucesso: {row['Successful']}", ln=True)
            pdf.cell(200, 10, txt=f"Erros nos Backups: {row['Error']}", ln=True)
            pdf.cell(200, 10, txt=f"Backups Parciais: {row['Partially Successful']}", ln=True)
            pdf.ln(10)

            # Adicionar gráficos de barras diários
            bar_chart_path = f"./charts/bar_chart_{row['Data']:%d_%m_%Y}.png"
            if os.path.exists(bar_chart_path):
                pdf.image(bar_chart_path, x=10, y=pdf.get_y(), w=190)
                pdf.ln(60)
            pdf.add_page()

        # Adicionar gráfico comparativo geral
        comparative_chart_path = "./charts/comparative_chart.png"
        if os.path.exists(comparative_chart_path):
            pdf.set_font("Arial", size=25)
            pdf.cell(200, 10, txt="Comparativo Geral dos Backups", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            pdf.image(comparative_chart_path, x=10, y=50, w=190)

        pdf.add_page()
        pdf.cell(200, 10, txt=f"Relatório gerado em: {data_atual}", ln=True, align="L")
        pdf.output(output_path)

        return output_path

    def process_and_generate_report(self, output_path):
        """
        Processa os arquivos CSV, gera um comparativo e cria um PDF.
        """
        files = self.get_latest_files()
        if not files:
            logger("Nenhum arquivo encontrado na pasta especificada.")
            return

        dataframes = []
        for file in files:
            file_path = os.path.join(self.data_folder, file)
            file_date = self.extract_date_from_filename(file)
            if file_date:
                df = self.load_csv_data(file_path, file_date)
                if not df.empty:
                    dataframes.append(df)

        if not dataframes:
            logger("Nenhum dado válido encontrado para gerar o relatório.")
            return

        summary_df = self.generate_summary(dataframes)

        # Gera gráficos
        self.chart_service.generate_bar_chart(summary_df)
        self.chart_service.generate_comparative_chart(summary_df)

        self.generate_pdf_report(summary_df, output_path)
