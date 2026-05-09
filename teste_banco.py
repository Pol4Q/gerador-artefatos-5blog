import sqlite3

def consultar_banco():
    try:
        # Conecta ao banco de dados que acabamos de popular
        conn = sqlite3.connect('banco_5blog.db')
        cursor = conn.cursor()

        print("\n" + "="*50)
        print("🔍 CONSULTANDO DEMANDAS SALVAS")
        print("="*50)
        
        # Puxa todas as demandas
        cursor.execute("SELECT id_demanda, setor_requisitante, objeto, data_criacao FROM demanda")
        demandas = cursor.fetchall() # Pega todos os resultados
        
        if not demandas:
            print("Nenhuma demanda encontrada no banco.")
        else:
            for d in demandas:
                print(f"🔹 ID Demanda: {d[0]}")
                print(f"   Setor: {d[1]}")
                print(f"   Objeto: {d[2]}")
                print(f"   Data de Criação: {d[3]}")
                
                # Para cada demanda, puxa os itens atrelados a ela
                cursor.execute("SELECT descricao, quantidade FROM item WHERE id_demanda = ?", (d[0],))
                itens = cursor.fetchall()
                
                print("   📦 Itens vinculados:")
                for i in itens:
                    print(f"      - {i[0]} (Qtd: {i[1]})")
                print("-" * 50)

    except sqlite3.Error as e:
        print(f"Erro ao acessar o banco: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    consultar_banco()