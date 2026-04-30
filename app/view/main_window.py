import customtkinter as ctk
from datetime import datetime
import re

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.lista_itens_dfd = []

        # ==========================================
        # CONFIGURAÇÕES BÁSICAS
        # ==========================================
        self.title("5º B Log - Gerador de Artefatos por 2º Ten Guilherme PAULICHEN")
        self.geometry("1000x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- BARRA LATERAL ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="5º B LOG - GERADOR", font=ctk.CTkFont(size=16, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))

        self.btn_dfd = ctk.CTkButton(self.sidebar_frame, text="Gerar DFD", command=self.mostrar_dfd)
        self.btn_dfd.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        # --- ÁREA PRINCIPAL ---
        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

        self.mostrar_dfd()

    # ==========================================
    # FUNÇÕES DE MÁSCARA E FORMATAÇÃO AUTOMÁTICA
    # ==========================================
    def formatar_telefone(self, event):
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down'): return
        texto = re.sub(r'\D', '', self.entry_telefone.get())
        if len(texto) > 11: texto = texto[:11]
        mascara = ""
        for i, char in enumerate(texto):
            if i == 0: mascara += "("
            mascara += char
            if i == 1: mascara += ") "
            if i == 2: mascara += " "
            if i == 6: mascara += "-"
        if self.entry_telefone.get() != mascara:
            self.entry_telefone.delete(0, "end")
            self.entry_telefone.insert(0, mascara)

    def formatar_idt(self, event):
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down'): return
        texto = re.sub(r'\D', '', self.entry_idt.get())
        if len(texto) > 10: texto = texto[:10]
        mascara = ""
        for i, char in enumerate(texto):
            mascara += char
            if i == 2 or i == 5: mascara += "."
            if i == 8: mascara += "-"
        if self.entry_idt.get() != mascara:
            self.entry_idt.delete(0, "end")
            self.entry_idt.insert(0, mascara)

    def formatar_cpf(self, event, entry_widget):
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down'): return
        texto = re.sub(r'\D', '', entry_widget.get())
        if len(texto) > 11: texto = texto[:11]
        mascara = ""
        for i, char in enumerate(texto):
            mascara += char
            if i == 2 or i == 5: mascara += "."
            if i == 8: mascara += "-"
        if entry_widget.get() != mascara:
            entry_widget.delete(0, "end")
            entry_widget.insert(0, mascara)

    def formatar_quantidade(self, event):
        if event.keysym in ('BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down'): return
        texto = re.sub(r'\D', '', self.entry_qtd_item.get())
        if self.entry_qtd_item.get() != texto:
            self.entry_qtd_item.delete(0, "end")
            self.entry_qtd_item.insert(0, texto)

    def formatar_maiusculo(self, event):
        texto_atual = self.entry_nome_guerra.get()
        texto_maiusculo = texto_atual.upper()
        if texto_atual != texto_maiusculo:
            pos = self.entry_nome_guerra.index("insert") # Salva a posição do cursor
            self.entry_nome_guerra.delete(0, "end")
            self.entry_nome_guerra.insert(0, texto_maiusculo)
            self.entry_nome_guerra.icursor(pos) # Restaura o cursor para não pular para o final

    # ==========================================
    # CONSTRUÇÃO DA TELA DO DFD
    # ==========================================
    def mostrar_dfd(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.main_frame, text="Documento de Formalização de Demanda (DFD)", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, columnspan=2, padx=20, pady=(10, 30), sticky="w")

        # --- SEÇÃO 0: CABEÇALHO (DADOS DO REQUISITANTE) ---
        ctk.CTkLabel(self.main_frame, text="Dados do Setor Requisitante", font=ctk.CTkFont(size=16, weight="bold")).grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="w")
        
        self.entry_setor = ctk.CTkEntry(self.main_frame, placeholder_text="Setor requisitante (ex: Setor de Aprovisionamento)")
        self.entry_setor.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.entry_responsavel = ctk.CTkEntry(self.main_frame, placeholder_text="Responsável pela demanda (Nome Completo)")
        self.entry_responsavel.grid(row=2, column=1, padx=20, pady=(0, 10), sticky="ew")

        self.entry_idt = ctk.CTkEntry(self.main_frame, placeholder_text="Identidade (Idt)")
        self.entry_idt.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.entry_idt.bind("<KeyRelease>", self.formatar_idt) # Bind da Máscara IDT

        self.entry_email = ctk.CTkEntry(self.main_frame, placeholder_text="E-mail de contato")
        self.entry_email.grid(row=3, column=1, padx=20, pady=(0, 10), sticky="ew")

        self.entry_telefone = ctk.CTkEntry(self.main_frame, placeholder_text="Telefone")
        self.entry_telefone.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.entry_telefone.bind("<KeyRelease>", self.formatar_telefone) # Bind da Máscara Telefone

        # --- SEÇÃO 1: OBJETO E JUSTIFICATIVA ---
        ctk.CTkLabel(self.main_frame, text="Objeto e Justificativa", font=ctk.CTkFont(size=16, weight="bold")).grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="w")
        
        self.entry_objeto_geral = ctk.CTkEntry(self.main_frame, placeholder_text="Objeto da futura contratação (título)")
        self.entry_objeto_geral.grid(row=6, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        self.textbox_justificativa = ctk.CTkTextbox(self.main_frame, height=80)
        self.textbox_justificativa.grid(row=7, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        # --- SEÇÃO 2: TIPO E PRIORIDADE ---
        opcoes_tipo = ["Material", "Serviço não continuado", "Serviço continuado SEM dedicação exclusiva de mão de obra", "Serviço continuado COM dedicação exclusiva de mão de obra"]
        self.option_tipo = ctk.CTkOptionMenu(self.main_frame, values=opcoes_tipo)
        self.option_tipo.grid(row=8, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.option_prioridade = ctk.CTkOptionMenu(self.main_frame, values=["Baixo", "Médio", "Alto"])
        self.option_prioridade.grid(row=8, column=1, padx=20, pady=(0, 20), sticky="ew")

        # --- SEÇÃO 3: TABELA DE ITENS ---
        ctk.CTkLabel(self.main_frame, text="Itens a serem adquiridos", font=ctk.CTkFont(size=16, weight="bold")).grid(row=9, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="w")
        
        self.entry_desc_item = ctk.CTkEntry(self.main_frame, placeholder_text="Descrição do Item")
        self.entry_desc_item.grid(row=10, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        self.entry_qtd_item = ctk.CTkEntry(self.main_frame, placeholder_text="Qtd", width=80)
        self.entry_qtd_item.grid(row=10, column=1, padx=20, pady=(0, 10), sticky="w")
        self.entry_qtd_item.bind("<KeyRelease>", self.formatar_quantidade) # Bind da Máscara Quantidade

        self.btn_add_item = ctk.CTkButton(self.main_frame, text="Adicionar Item", command=self.adicionar_item_lista)
        self.btn_add_item.grid(row=11, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        self.txt_lista_visual = ctk.CTkTextbox(self.main_frame, height=80, state="disabled")
        self.txt_lista_visual.grid(row=12, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        # --- SEÇÃO 4: EQUIPE DE PLANEJAMENTO ---
        ctk.CTkLabel(self.main_frame, text="Equipe de planejamento", font=ctk.CTkFont(size=16, weight="bold")).grid(row=13, column=0, columnspan=2, padx=20, pady=(10, 10), sticky="w")
        
        self.entry_nome_chefe = ctk.CTkEntry(self.main_frame, placeholder_text="Nome do chefe da equipe de planejamento")
        self.entry_nome_chefe.grid(row=14, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.entry_cpf_chefe = ctk.CTkEntry(self.main_frame, placeholder_text="CPF")
        self.entry_cpf_chefe.grid(row=14, column=1, padx=20, pady=(0, 5), sticky="ew")
        self.entry_cpf_chefe.bind("<KeyRelease>", lambda e: self.formatar_cpf(e, self.entry_cpf_chefe)) # Bind Máscara CPF Chefe

        self.entry_nome_tec = ctk.CTkEntry(self.main_frame, placeholder_text="Nome do auxiliar técnico")
        self.entry_nome_tec.grid(row=15, column=0, padx=20, pady=(0, 5), sticky="ew")
        self.entry_cpf_tec = ctk.CTkEntry(self.main_frame, placeholder_text="CPF")
        self.entry_cpf_tec.grid(row=15, column=1, padx=20, pady=(0, 5), sticky="ew")
        self.entry_cpf_tec.bind("<KeyRelease>", lambda e: self.formatar_cpf(e, self.entry_cpf_tec)) # Bind Máscara CPF Téc

        self.entry_nome_adm = ctk.CTkEntry(self.main_frame, placeholder_text="Nome do auxiliar administrativo")
        self.entry_nome_adm.grid(row=16, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.entry_cpf_adm = ctk.CTkEntry(self.main_frame, placeholder_text="CPF")
        self.entry_cpf_adm.grid(row=16, column=1, padx=20, pady=(0, 10), sticky="ew")
        self.entry_cpf_adm.bind("<KeyRelease>", lambda e: self.formatar_cpf(e, self.entry_cpf_adm)) # Bind Máscara CPF Adm

        # --- SEÇÃO 5: ASSINATURA ---
        ctk.CTkLabel(self.main_frame, text="Dados do chefe do setor requisitante (assinatura)", font=ctk.CTkFont(size=16, weight="bold")).grid(row=17, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="w")
        
        self.entry_nome_guerra = ctk.CTkEntry(self.main_frame, placeholder_text="NOME COMPLETO")
        self.entry_nome_guerra.grid(row=18, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.entry_nome_guerra.bind("<KeyRelease>", self.formatar_maiusculo) # Bind Maiúsculo Automático

        lista_postos = ["Cel", "Ten Cel", "Maj", "Cap", "1º Ten", "2º Ten", "Asp", "S Ten", "1º Sgt", "2º Sgt", "3º Sgt", "Cb"]
        self.option_postograd = ctk.CTkOptionMenu(self.main_frame, values=lista_postos)
        self.option_postograd.set("Cap") # Default
        self.option_postograd.grid(row=18, column=1, padx=20, pady=(0, 20), sticky="ew")

        self.btn_gerar = ctk.CTkButton(self.main_frame, text="GERAR DFD", fg_color="#28a745", hover_color="#218838", height=50, command=self.acao_gerar_dfd)
        self.btn_gerar.grid(row=19, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

    def adicionar_item_lista(self):
        desc = self.entry_desc_item.get()
        qtd = self.entry_qtd_item.get()
        if desc and qtd:
            self.lista_itens_dfd.append({"descricao": desc, "quantidade": qtd})
            self.txt_lista_visual.configure(state="normal")
            self.txt_lista_visual.insert("end", f"• {desc} ({qtd})\n")
            self.txt_lista_visual.configure(state="disabled")
            self.entry_desc_item.delete(0, 'end')
            self.entry_qtd_item.delete(0, 'end')

    def acao_gerar_dfd(self):
        hoje = datetime.now()
        meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
        
        # Lógica para pegar o nome de guerra se o campo estiver vazio
        nome_guerra = self.entry_nome_guerra.get().upper()
        if not nome_guerra and self.entry_responsavel.get():
            nome_guerra = self.entry_responsavel.get().split()[-1].upper()

        dados = {
            "setor": self.entry_setor.get(),
            "responsavel": self.entry_responsavel.get(),
            "idt": self.entry_idt.get(),
            "email": self.entry_email.get(),
            "telefone": self.entry_telefone.get(),
            "objeto": self.entry_objeto_geral.get(),
            "tipo": self.option_tipo.get(),
            "prioridade": self.option_prioridade.get(),
            "justificativa": self.textbox_justificativa.get("1.0", "end-1c"),
            "dia": hoje.strftime("%d"),
            "mes": meses[hoje.month - 1],
            "ano": hoje.strftime("%Y"),
            "nome_guerra": nome_guerra,
            "postograd": self.option_postograd.get(),
            "nome_chefe": self.entry_nome_chefe.get(), "cpf_chefe": self.entry_cpf_chefe.get(),
            "nome_tec": self.entry_nome_tec.get(), "cpf_tec": self.entry_cpf_tec.get(),
            "nome_adm": self.entry_nome_adm.get(), "cpf_adm": self.entry_cpf_adm.get(),
            "itens": self.lista_itens_dfd
        }
        
        objeto_limpo = re.sub(r'[^A-Za-z0-9]', '_', self.entry_objeto_geral.get())[:15]
        nome_arquivo = f"DFD_{objeto_limpo}_{hoje.strftime('%Hh%M%S')}.docx"
        
        try:
            from app.controller.documento_controller import gerar_dfd
            gerar_dfd(dados, nome_arquivo)
            self.btn_gerar.configure(text="DOCUMENTO GERADO!", fg_color="#155724")
            self.lista_itens_dfd = []
        except Exception as e:
            print(f"Erro: {e}")

    def iniciar(self):
        self.mainloop()