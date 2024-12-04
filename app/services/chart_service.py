import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

class ChartService:
    def __init__(self, output_folder="./charts"):
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_bar_chart(self, summary_df):
        """
        Gera gráficos de barras para cada dia.
        """
        for index, row in summary_df.iterrows():
            plt.figure(figsize=(6, 4))
            plt.bar(
                ["Successful", "Error", "Partially Successful"],
                [row["Successful"], row["Error"], row["Partially Successful"]],
                color=["#4caf50", "#f44336", "#ff9800"]
            )
            plt.title(f"Status do Backup - {row['Data']:%d/%m/%Y}")
            plt.ylabel("Quantidade")
            file_path = os.path.join(self.output_folder, f"bar_chart_{row['Data']:%d_%m_%Y}.png")
            plt.savefig(file_path)
            plt.close()

    def generate_comparative_chart(self, summary_df):
        """
        Gera um gráfico comparativo consolidado.
        """
        total_successful = summary_df["Successful"].sum()
        total_errors = summary_df["Error"].sum()
        total_partial = summary_df["Partially Successful"].sum()

        plt.figure(figsize=(6, 4))
        plt.bar(
            ["Successful", "Error", "Partially Successful"],
            [total_successful, total_errors, total_partial],
            color=["#4caf50", "#f44336", "#ff9800"]
        )
        plt.title("Comparativo geral dos últimos 5 backups")
        plt.ylabel("Quantidade")
        file_path = os.path.join(self.output_folder, "comparative_chart.png")
        plt.savefig(file_path)
        plt.close()
