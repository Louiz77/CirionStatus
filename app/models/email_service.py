import requests
import os
from msal import ConfidentialClientApplication
from ..config import Config
import base64
from datetime import datetime

class EmailService:
    def __init__(self):
        self.client = ConfidentialClientApplication(
            Config.CLIENT_ID,
            authority=f"https://login.microsoftonline.com/{Config.TENANT_ID}",
            client_credential=Config.CLIENT_SECRET
        )

    def get_access_token(self):
        try:
            result = self.client.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
            if "access_token" in result:
                print("Token de acesso obtido com sucesso.")
                return result["access_token"]
            else:
                raise Exception(f"Erro ao obter token: {result.get('error_description', 'Erro desconhecido')}")
        except Exception as e:
            print(e)
            raise Exception("Erro ao obter token de acesso.")

    def fetch_emails_from_sender(self):
        """
        Busca emails na caixa de entrada e filtra pelo remetente manualmente.
        """
        try:
            token = self.get_access_token()
            headers = {"Authorization": f"Bearer {token}"}

            # Solicita os emails ordenados por data
            url = f"{Config.BASE_URL}/users/{Config.EMAIL_ADDRESS}/messages?$orderby=receivedDateTime desc"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                emails = response.json().get("value", [])
                with open("report.log", "a") as my_file:
                    my_file.write(f"-{datetime.now()} | Emails: {emails}\n")
                    print(f"Total de emails retornados: {len(emails)}")

                # Filtrar emails pelo remetente
                filtered_emails = [
                    email for email in emails
                    if email.get("from", {}).get("emailAddress", {}).get("address") == "operacaobkp@ciriontechnologies.com"
                ]
                print(f"Total de emails do remetente operacaobkp@ciriontechnologies.com: {len(filtered_emails)}")
                with open("report.log", "a") as my_file:
                    my_file.write(f"-{datetime.now()} | Emails filtrados: {filtered_emails}\n")
                    print(f"Total de emails retornados: {len(emails)}")
                return filtered_emails

            else:
                with open("report.log", "a") as my_file:
                    my_file.write(f"-{datetime.now()} | Erro ao buscar emails: {response.status_code}, {response.text}\n")
                print(f"Erro ao buscar emails: {response.status_code}, {response.text}")
                return []

        except Exception as e:
            with open("report.log", "a") as my_file:
                my_file.write(f"-{datetime.now()} | Erro ao buscar emails: {e}\n")
            print(f"Erro ao buscar emails: {e}")
            raise

    def download_attachments_from_email(self, message_id):
        """
        Faz o download de anexos de e-mails e decodifica Base64, se necessário.
        """
        try:
            token = self.get_access_token()
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(
                f"{Config.BASE_URL}/users/{Config.EMAIL_ADDRESS}/messages/{message_id}/attachments",
                headers=headers
            )

            if response.status_code == 200:
                attachments = response.json().get("value", [])

                for attachment in attachments:
                    # Verifica se o anexo é do tipo arquivo
                    if attachment["@odata.type"] == "#microsoft.graph.fileAttachment":
                        file_name = attachment["name"]
                        file_content = attachment["contentBytes"]

                        # Decodifica o conteúdo Base64
                        decoded_content = base64.b64decode(file_content)

                        # Salva o arquivo no diretório de destino
                        file_path = os.path.join(Config.DATA_FOLDER, file_name)
                        os.makedirs(Config.DATA_FOLDER, exist_ok=True)

                        with open(file_path, "wb") as f:
                            f.write(decoded_content)

                        print(f"Arquivo salvo em: {file_path}")
                        return file_path

            else:
                print(f"Erro ao baixar anexos: {response.status_code}, {response.text}")
                raise Exception("Erro ao baixar anexos.")

        except Exception as e:
            print(f"Erro ao processar anexo: {e}")
            raise Exception("Erro ao baixar e salvar o anexo.")

    def process_emails(self):
        """
        Busca emails do remetente específico e baixa os anexos.
        """
        try:
            emails = self.fetch_emails_from_sender()

            if not emails:
                print(f"Nenhum email encontrado do remetente")
                return {"message": f"Nenhum email encontrado"}

            # Itera pelos emails e faz o download dos anexos
            for email in emails:
                print(f"Processando email: {email.get('subject')} - ID: {email['id']}")
                attachment_path = self.download_attachments_from_email(email["id"])
                if attachment_path:
                    print(f"Anexo salvo em: {attachment_path}")
                    return {"message": f"Anexo salvo em {attachment_path}"}

            return {"message": "Nenhum anexo encontrado para download."}

        except Exception as e:
            print(f"Erro ao processar emails: {e}")
            return {"error": f"Erro ao processar emails: {e}"}
