import customtkinter as ctk
import control
from tkinter import ttk
from model import model_lead

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LeadForm(ctk.CTkToplevel):
    def __init__(self, master, on_save):
        super().__init__(master)
        self.on_save = on_save
        self.title("Adicionar Lead")
        self.geometry("380x420")
        self.resizable(False, False)

        self.entries = {}
        campos = [("name", "Nome"), ("email", "E-mail"), ("company", "Empresa")]
        for chave, rotulo in campos:
            ctk.CTkLabel(self, text=rotulo, anchor="w").pack(fill="x", padx=30, pady=(15, 0))
            entry = ctk.CTkEntry(self, placeholder_text=rotulo)
            entry.pack(fill="x", padx=30, pady=(3, 0))
            self.entries[chave] = entry

        ctk.CTkLabel(self, text="Etapa de vendas", anchor="w").pack(fill="x", padx=30, pady=(15, 0))
        self.step_box = ctk.CTkComboBox(self, values=["novo", "contato", "proposta", "negociação", "fechado"])
        self.step_box.pack(fill="x", padx=30, pady=(3, 0))
        self.step_box.set("novo")

        self.error_label = ctk.CTkLabel(self, text="", text_color="#ff6b6b")
        self.error_label.pack(pady=(12,0))

        botoes = ctk.CTkFrame(self, fg_color="transparent")
        botoes.pack(fill="x", padx=30, pady=15)

        ctk.CTkButton(botoes, text="Cancelar", fg_color="gray30", hover_color="gray40",
                      command=self.destroy).pack(side="left", expand=True, fill="x", padx=(0, 5))
        ctk.CTkButton(botoes, text="Salvar", command=self.save).pack(
            side="left", expand=True, fill="x", padx=(5, 0)
        )

        self.after(200, self.focus_form)

    def focus_form(self):
        self.lift()
        self.focus_force()
        self.grab_set()

    def save(self):
        dados = {chave: entry.get().strip() for chave, entry in self.entries.items()}
        dados["step"] = self.step_box.get().strip() or "novo"

        if not dados["name"]:
            self.error_label.configure(text="O nome é obrigatório.")
            return
        if dados["email"] and "@" not in dados["email"]:
            self.error_label.configure(text="E-mail inválido.")
            return

        self.on_save(dados)
        self.destroy()


class MiniCrm(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mini CRM de Leads")
        self.geometry("900x500")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=190, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.build_sidebar()
        self.build_main()
        self.refresh()

    def build_sidebar(self):
        ctk.CTkLabel(self.sidebar, text="Mini CRM",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=25, padx=20)

        ctk.CTkButton(self.sidebar, text="Adicionar Lead", command=self.add_lead).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(self.sidebar, text="Atualizar Lead").pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(self.sidebar, text="Deletar Lead", fg_color="#c0392b", hover_color="#962d22").pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(self.sidebar, text="Exportar CSV", fg_color="#2e8b57", hover_color="#236b43").pack(fill="x", padx=20, pady=6)

    def build_main(self):
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.main, height=36,
            placeholder_text="Buscar por nome, e-mail ou empresa...")
        self.search_entry.grid(row=0, column=0, sticky="ew", pady=(0, 12))

        self.list_frame = ctk.CTkFrame(self.main)
        self.list_frame.grid(row=1, column=0, sticky="nsew")

        colunas = ("idx", "name","email", "company", "step", "created" )
        titulos = ("##", "Nome", "E-mail", "Empresa", "Etapa", "Criado em")

        self.tree = ttk.Treeview(self.list_frame, columns=colunas, show="headings")
        for col, titulo in zip(colunas, titulos):
            self.tree.heading(col, text=titulo)
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh())

    def refresh(self):
        query = self.search_entry.get().strip()

        if query:
            resultados = control.read_leads_search(query)
        else:
            resultados = list(enumerate(control.read_leads()))

        self.tree.delete(*self.tree.get_children())
        for i, lead in resultados:
            self.tree.insert("", "end", iid=str(i), values=(
                f"{i:02d}", lead["name"], lead["email"],
                lead["company"], lead["step"], lead["created"]))

    def add_lead(self):
        def salvar(dados):
            lead = model_lead(dados["name"], dados["email"], dados["company"], dados["step"])
            control.create_lead(lead)
            self.refresh()

        LeadForm(self, on_save=salvar)

if __name__ == "__main__":
    MiniCrm().mainloop()