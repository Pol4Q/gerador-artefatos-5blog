import sqlite3
import os

# O banco será criado na raiz do projeto (mesmo nível do main.py)
DB_NAME = 'banco_5blog.db'

def conectar():
    """Cria a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    # Habilita o suporte a chaves estrangeiras (vem desativado por padrão)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    """Executa o DDL para criar as tabelas estruturais do sistema."""
    try:
        conn = conectar()
        cursor = conn.cursor()

        # Tabela de Demandas (DFD)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS demanda (
                id_demanda INTEGER PRIMARY KEY AUTOINCREMENT,
                uasg TEXT NOT NULL,
                setor_requisitante TEXT NOT NULL,
                objeto TEXT NOT NULL,
                justificativa TEXT NOT NULL,
                data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Tabela de Militares (Para a equipe de planejamento)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS militar (
                id_militar INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                posto_graduacao TEXT NOT NULL,
                funcao TEXT NOT NULL,
                cpf TEXT UNIQUE NOT NULL
            )
        ''')

        # Tabela de Itens (Materiais/Serviços da Demanda)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS item (
                id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                id_demanda INTEGER NOT NULL,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                quantidade INTEGER NOT NULL CHECK (quantidade > 0),
                FOREIGN KEY (id_demanda) REFERENCES demanda(id_demanda) ON DELETE CASCADE
            )
        ''')

        # Tabela Associativa (Equipe de Planejamento)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipe_planejamento (
                id_demanda INTEGER,
                id_militar INTEGER,
                papel TEXT NOT NULL,
                PRIMARY KEY (id_demanda, id_militar),
                FOREIGN KEY (id_demanda) REFERENCES demanda(id_demanda) ON DELETE CASCADE,
                FOREIGN KEY (id_militar) REFERENCES militar(id_militar) ON DELETE RESTRICT
            )
        ''')

        conn.commit()
        print("SISTEMA: Banco de dados inicializado com sucesso.")

    except sqlite3.Error as e:
        print(f"ERRO CRÍTICO no banco de dados: {e}")
    
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def salvar_demanda_bd(uasg, setor, objeto, justificativa, lista_itens):
    """
    Realiza o INSERT da Demanda e dos Itens vinculados no banco de dados.
    Recebe os dados principais e uma lista de dicionários contendo os itens.
    """
    conn = conectar()
    cursor = conn.cursor()
    
    try:
        # 1. Inserir a Demanda principal
        cursor.execute('''
            INSERT INTO demanda (uasg, setor_requisitante, objeto, justificativa)
            VALUES (?, ?, ?, ?)
        ''', (uasg, setor, objeto, justificativa))
        
        # Recuperar o ID numérico (id_demanda) que o SQLite acabou de gerar
        id_demanda = cursor.lastrowid
        
        # 2. Inserir cada item da lista vinculado ao ID da Demanda
        for item in lista_itens:
            # Pelo seu print, os itens têm 'descricao' e 'quantidade'. 
            # O 'tipo' podemos receber da tela ou fixar como 'Material' por padrão neste momento.
            tipo_item = item.get('tipo', 'Material') 
            
            cursor.execute('''
                INSERT INTO item (id_demanda, descricao, tipo, quantidade)
                VALUES (?, ?, ?, ?)
            ''', (id_demanda, item['descricao'], tipo_item, item['quantidade']))
            
        # Confirma a transação (salva definitivamente no arquivo .db)
        conn.commit()
        print(f"SISTEMA: Demanda #{id_demanda} e seus itens salvos no banco com sucesso!")
        return id_demanda
        
    except sqlite3.Error as e:
        # Se der qualquer erro (ex: faltou um campo), desfaz tudo para não corromper o banco
        conn.rollback()
        print(f"ERRO ao salvar dados da demanda: {e}")
        return None
        
    finally:
        conn.close()