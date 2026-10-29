import customtkinter as ctk
import control
from model import model_lead
from tkinter import ttk, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class LeadForm(ctk.CTkToplevel):
    def __init__(self, master, on_save, titulo="Adicionar Lead", lead=None):
        super().__init__(master)
        self.on_save = on_save
        self.lead = lead or {}
        self.title(titulo)
        self.geometry("380x420")
        self.resizable(False, False)

        self.entries = {}
        campos = [("name", "Nome"), ("email", "E-mail"), ("company", "Empresa")]
        for chave, rotulo in campos:
            ctk.CTkLabel(self, text=rotulo, anchor="w").pack(fill="x", padx=30, pady=(15, 0))
            entry = ctk.CTkEntry(self, placeholder_text=rotulo)
            entry.pack(fill="x", padx=30, pady=(3, 0))
            if self.lead.get(chave):
                entry.insert(0, self.lead[chave])
            self.entries[chave] = entry

        ctk.CTkLabel(self, text="Etapa de vendas", anchor="w").pack(fill="x", padx=30, pady=(15, 0))
        self.step_box = ctk.CTkComboBox(self, values=["novo", "contato", "proposta", "negociação", "fechado"])
        self.step_box.pack(fill="x", padx=30, pady=(3, 0))
        self.step_box.set(self.lead.get("step", "novo"))

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
        ctk.CTkButton(self.sidebar, text="Atualizar Lead", fg_color="#d4a017", hover_color="#b8860b", text_color="#1a1a1a", command=self.update_lead).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(self.sidebar, text="Deletar Lead", fg_color="#c0392b", hover_color="#962d22", command=self.delete_lead).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(self.sidebar, text="Exportar CSV", fg_color="#2e8b57", hover_color="#236b43", command=self.export_leads).pack(fill="x", padx=20, pady=6)
        self.theme_menu = ctk.CTkOptionMenu(self.sidebar, values=["Dark", "Light"],
                                            command=self.change_theme)
        self.theme_menu.pack(side="bottom", fill="x", padx=20, pady=20)

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

        self.tree = ttk.Treeview(self.list_frame, columns=colunas, show="headings", style="CRM.Treeview")
        for col, titulo in zip(colunas, titulos):
            self.tree.heading(col, text=titulo)
            self.tree.column(col, width=100)

        barra = ctk.CTkScrollbar(self.list_frame, command=self.tree.yview)
        barra.pack(side="right", fill="y", pady=6, padx=(0, 4))
        self.tree.configure(yscrollcommand=barra.set)

        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh())

        self.style_tree()

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

    def selected_index(self):
        selecao = self.tree.selection()
        if not selecao:
            messagebox.showinfo("Mini CRM", "Selecione um lead na lista primeiro.")
            return None
        return int(selecao[0])

    def update_lead(self):
        index = self.selected_index()
        if index is None:
            return

        lead = control.read_leads()[index]

        def salvar(dados):
            control.update_lead(index, dados)
            self.refresh()

        LeadForm(self, on_save=salvar, titulo="Atualizar Lead", lead=lead)

    def delete_lead(self):
        index = self.selected_index()
        if index is None:
            return

        lead = control.read_leads()[index]
        confirmar = messagebox.askyesno(
            "Deletar lead", f"Tem certeza que deseja deletar {lead['name']}?")

        if confirmar:
            control.delete_lead(index)
            self.refresh()

    def export_leads(self):
        if not control.read_leads():
            messagebox.showwarning("Exportar CSV", "Nenhum lead para exportar.")
            return

        caminho = control.export_csv()

        if caminho is None:
            messagebox.showwarning("Exportar CSV", "Não foi possível exportar os leads.")
        else:
            messagebox.showinfo("Exportar CSV", f"Exportado para:\n{caminho}")

    def style_tree(self):
        escuro = ctk.get_appearance_mode() == "Dark"
        fundo = "#2b2b2b" if escuro else "#ffffff"
        texto = "#e6e6e6" if escuro else "#1a1a1a"
        cabecalho = "#1f538d" if escuro else "#3b8ed0"

        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("CRM.Treeview",
                         background=fundo, fieldbackground=fundo,
                         foreground=texto, rowheight=30,
                         borderwidth=0, font=("Segoe UI", 11))
        estilo.configure("CRM.Treeview.Heading",
                         background=cabecalho, foreground="white",
                         relief="flat", font=("Segoe UI", 11, "bold"))

        estilo.map("CRM.Treeview",
                   background=[("selected", "#1f6aa5")],
                   foreground=[("selected", "white")])
        estilo.map("CRM.Treeview.Heading",
                   background=[("active", cabecalho)])

    def change_theme(self, modo):
        ctk.set_appearance_mode(modo)
        self.style_tree()

if __name__ == "__main__":
    MiniCrm().mainloop()