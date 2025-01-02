from apscheduler.schedulers.background import BackgroundScheduler
from app.models.email_service import EmailService
from app.services.registrar_log import logger
from pytz import timezone
import os

os.environ['TZ'] = 'America/Sao_Paulo'

def atualizar_planilha_automaticamente():
    """
    Função que atualiza a planilha automaticamente.
    """
    email_service = EmailService()
    try:
        logger("Executando atualização automática da planilha...")
        resultado = email_service.process_emails()
        logger(f"Resultado da atualização: {resultado}")
    except Exception as e:
        logger(f"Erro na atualização automática: {e}")

def schedule_planilha():
    # Agendador
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=atualizar_planilha_automaticamente,
        trigger="cron",
        hour=15,         # Hora de execução
        minute=2,         # Minuto de execução
        timezone = timezone('America/Sao_Paulo')
    )
    scheduler.add_job(
        func=atualizar_planilha_automaticamente,
        trigger="cron",
        hour=15,         # Hora de execução
        minute=35,         # Minuto de execução
        timezone=timezone('America/Sao_Paulo')
    )
    scheduler.add_job(
        func=atualizar_planilha_automaticamente,
        trigger="cron",
        hour=16,         # Hora de execução
        minute=30,         # Minuto de execução
        timezone=timezone('America/Sao_Paulo')
    )
    scheduler.start()