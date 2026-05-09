from app.view.main_window import MainWindow
from app.model.database import criar_tabelas # <-- Importação do banco

if __name__ == "__main__":
    # 1. Cria o arquivo .db e as tabelas ANTES de abrir a tela
    criar_tabelas()
    
    # 2. Instancia e inicia a interface gráfica (View)
    app = MainWindow()
    app.iniciar()