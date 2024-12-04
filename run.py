from app import create_app
from app.services.scheduler_service import schedule_planilha

app = create_app()

try:
    schedule_planilha()
except Exception as e:
    print(f"Erro na atualização automática: {e}")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5050)
